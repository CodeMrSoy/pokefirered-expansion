// llama.cpp b6500 API. The host supplies the trusted GGUF, fixed grammar and prompt.
#include "ggml-backend.h"
#include "llama.h"
#include <chrono>
#include <cstdio>
#include <cstring>
#include <cwchar>
#include <memory>
#include <string>
#include <vector>

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#endif

#ifdef __linux__
extern "C" int LivingWorldRestrictWorker();
#endif

static void QuietLog(ggml_log_level, const char *, void *)
{
}

static bool Generate(llama_context *context, const llama_vocab *vocab,
                     const char *rules, const char *prompt, std::string &output)
{
    llama_memory_clear(llama_get_memory(context), true);
    std::vector<llama_token> tokens(256);
    const auto count = llama_tokenize(vocab, prompt, std::strlen(prompt),
        tokens.data(), tokens.size(), false, true);
    if (count <= 0)
        return false;

    auto sampler = std::unique_ptr<llama_sampler, decltype(&llama_sampler_free)>(
        llama_sampler_chain_init(llama_sampler_chain_default_params()), llama_sampler_free);
    auto *grammar = llama_sampler_init_grammar(vocab, rules, "root");
    if (!grammar)
        return false;
    llama_sampler_chain_add(sampler.get(), grammar);
    llama_sampler_chain_add(sampler.get(), llama_sampler_init_greedy());

    auto batch = llama_batch_get_one(tokens.data(), count);
    llama_token next;
    for (int i = 0; i < 48; ++i) {
        if (llama_decode(context, batch) != 0)
            return false;
        next = llama_sampler_sample(sampler.get(), context, -1);
        if (llama_vocab_is_eog(vocab, next))
            return true;
        char chunk[128];
        int length = llama_token_to_piece(vocab, next, chunk, sizeof(chunk), 0, false);
        if (length < 0 || output.size() + length > 512)
            return false;
        output.append(chunk, length);
        batch = llama_batch_get_one(&next, 1);
    }
    return false;
}

static int HexDigit(char c)
{
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    return -1;
}

static bool Unhex(const char *input, size_t length, std::string &output)
{
    if (length == 0 || length % 2 != 0 || length > 8192)
        return false;
    for (size_t i = 0; i < length; i += 2) {
        int hi = HexDigit(input[i]), lo = HexDigit(input[i + 1]);
        if (hi < 0 || lo < 0 || (hi == 0 && lo == 0))
            return false;
        output.push_back(static_cast<char>(16 * hi + lo));
    }
    return true;
}

using Clock = std::chrono::steady_clock;

static int Serve(llama_context *context, const llama_vocab *vocab, Clock::time_point startup)
{
    std::printf("ready %.3f\n", std::chrono::duration<double, std::milli>(Clock::now() - startup).count());
    std::fflush(stdout);
    // One bounded record per request, even when grammar or prompt contains newlines.
    char record[16386];
    while (std::fgets(record, sizeof(record), stdin)) {
        std::string grammar, prompt, output;
        const char *tab = std::strchr(record, '\t');
        const char *end = std::strchr(record, '\n');
        if (!end)
            return 2;
        if (end > record && end[-1] == '\r')
            --end;
        const auto start = Clock::now();
        if (tab && tab < end && Unhex(record, tab - record, grammar)
            && Unhex(tab + 1, end - tab - 1, prompt)
            && Generate(context, vocab, grammar.c_str(), prompt.c_str(), output)) {
            std::printf("ok %.3f ", std::chrono::duration<double, std::milli>(Clock::now() - start).count());
            for (unsigned char value : output)
                std::printf("%02x", static_cast<unsigned>(value));
            std::putchar('\n');
        } else {
            std::puts("error inference");
        }
        std::fflush(stdout);
    }
    return std::feof(stdin) ? 0 : 2;
}

static int Run(const char *modelPath, const char *rules = nullptr, const char *prompt = nullptr)
{
    const auto startup = Clock::now();
    llama_log_set(QuietLog, nullptr);
    ggml_backend_load_all();
    auto params = llama_model_default_params();
    params.n_gpu_layers = 0;
    auto model = std::unique_ptr<llama_model, decltype(&llama_model_free)>(
        llama_model_load_from_file(modelPath, params), llama_model_free);
    if (!model) {
        std::fputs("Could not load the packaged GGUF.\n", stderr);
        return 2;
    }

    auto config = llama_context_default_params();
    config.n_ctx = 512;
    config.n_batch = 256;
    // Keep Linux generation inside a single restricted thread.
#ifdef __linux__
    config.n_threads = config.n_threads_batch = 1;
#else
    config.n_threads = config.n_threads_batch = 4;
#endif
    auto context = std::unique_ptr<llama_context, decltype(&llama_free)>(
        llama_init_from_model(model.get(), config), llama_free);
    if (!context)
        return 2;

#ifdef __linux__
    if (LivingWorldRestrictWorker() != 0) {
        std::perror("Could not enable Linux worker isolation");
        return 125;
    }
    std::fputs("LQW isolation active\n", stderr);
#endif

    const auto *vocab = llama_model_get_vocab(model.get());
    if (!rules)
        return Serve(context.get(), vocab, startup);
    std::string output;
    if (!Generate(context.get(), vocab, rules, prompt, output))
        return 2;
    return std::fwrite(output.data(), 1, output.size(), stdout) == output.size() ? 0 : 2;
}

#ifdef _WIN32
static std::string Utf8(const wchar_t *source)
{
    const int length = WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, source, -1, nullptr, 0, nullptr, nullptr);
    std::string result(length > 0 ? length : 1, '\0');
    if (length > 0)
        WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, source, -1, result.data(), length, nullptr, nullptr);
    return result;
}

int wmain(int argc, wchar_t **argv)
{
    if (argc == 3 && std::wcscmp(argv[2], L"--serve") == 0)
        return Run(Utf8(argv[1]).c_str());
    if (argc != 4)
        return 2;
    return Run(Utf8(argv[1]).c_str(), Utf8(argv[2]).c_str(), Utf8(argv[3]).c_str());
}
#else
int main(int argc, char **argv)
{
    if (argc == 3 && std::strcmp(argv[2], "--serve") == 0)
        return Run(argv[1]);
    if (argc != 4)
        return 2;
    return Run(argv[1], argv[2], argv[3]);
}
#endif

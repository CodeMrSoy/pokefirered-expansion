// llama.cpp b6500 API. The host supplies the trusted GGUF, fixed grammar and prompt.
#include "ggml-backend.h"
#include "llama.h"
#include <cstdio>
#include <cstring>
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

static int Generate(const char *modelPath, const char *rules, const char *prompt)
{
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
    std::vector<llama_token> tokens(256);
    const auto count = llama_tokenize(vocab, prompt, std::strlen(prompt),
        tokens.data(), tokens.size(), false, true);
    if (count <= 0)
        return 2;

    auto sampler = std::unique_ptr<llama_sampler, decltype(&llama_sampler_free)>(
        llama_sampler_chain_init(llama_sampler_chain_default_params()), llama_sampler_free);
    auto *grammar = llama_sampler_init_grammar(vocab, rules, "root");
    if (!grammar)
        return 2;
    llama_sampler_chain_add(sampler.get(), grammar);
    llama_sampler_chain_add(sampler.get(), llama_sampler_init_greedy());

    auto batch = llama_batch_get_one(tokens.data(), count);
    llama_token next;
    for (int i = 0; i < 64; ++i) {
        if (llama_decode(context.get(), batch) != 0)
            return 2;
        next = llama_sampler_sample(sampler.get(), context.get(), -1);
        if (llama_vocab_is_eog(vocab, next))
            return 0;
        char chunk[128];
        int length = llama_token_to_piece(vocab, next, chunk, sizeof(chunk), 0, false);
        if (length < 0)
            return 2;
        std::fwrite(chunk, 1, length, stdout);
        batch = llama_batch_get_one(&next, 1);
    }
    return 2;
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
    if (argc != 4)
        return 2;
    return Generate(Utf8(argv[1]).c_str(), Utf8(argv[2]).c_str(), Utf8(argv[3]).c_str());
}
#else
int main(int argc, char **argv)
{
    if (argc != 4)
        return 2;
    return Generate(argv[1], argv[2], argv[3]);
}
#endif

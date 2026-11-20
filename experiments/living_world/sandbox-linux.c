#define _GNU_SOURCE
#include <errno.h>
#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <stddef.h>
#include <sys/prctl.h>
#include <sys/syscall.h>
#include <unistd.h>

#if !defined(__x86_64__)
#error This isolation module targets Linux x86-64
#endif

#define ALLOW(num) \
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, SYS_##num, 0, 1), \
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW)

// Call after the trusted GGUF is mapped and before using the prompt. Inference
// retains only stdio pipes and in-memory model state. Apply to all threads.
int LivingWorldRestrictWorker(void)
{
    struct sock_filter filter[] = {
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, arch)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        ALLOW(read), ALLOW(write), ALLOW(writev), ALLOW(close),
        ALLOW(fstat), ALLOW(lseek),
        ALLOW(mmap), ALLOW(mprotect), ALLOW(munmap), ALLOW(madvise),
        ALLOW(mremap), ALLOW(brk),
        ALLOW(futex), ALLOW(set_robust_list), ALLOW(rseq),
        ALLOW(getpid), ALLOW(gettid), ALLOW(getrandom),
        ALLOW(clock_gettime), ALLOW(clock_nanosleep), ALLOW(nanosleep),
        ALLOW(sched_yield), ALLOW(sched_getaffinity), ALLOW(sched_getparam),
        ALLOW(sched_getscheduler), ALLOW(getcpu),
        ALLOW(rt_sigaction), ALLOW(rt_sigprocmask), ALLOW(rt_sigreturn),
        ALLOW(exit), ALLOW(exit_group),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | EPERM),
    };
    struct sock_fprog program = { sizeof(filter) / sizeof(filter[0]), filter };

    if (syscall(SYS_close_range, 3U, ~0U, 0) != 0)
        return -1;
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0)
        return -1;
    return syscall(SYS_seccomp, SECCOMP_SET_MODE_FILTER, SECCOMP_FILTER_FLAG_TSYNC, &program) == 0 ? 0 : -1;
}

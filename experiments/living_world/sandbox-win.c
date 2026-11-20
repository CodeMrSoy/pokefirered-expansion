#define _UNICODE
#define _WIN32_WINNT 0x0a00
#include <windows.h>
#include <aclapi.h>
#include <userenv.h>
#include <stdio.h>
#include <stdlib.h>
#include <wchar.h>

#ifndef PROC_THREAD_ATTRIBUTE_CHILD_PROCESS_POLICY
#define PROC_THREAD_ATTRIBUTE_CHILD_PROCESS_POLICY 0x0002000e
#endif
#ifndef PROCESS_CREATION_CHILD_PROCESS_RESTRICTED
#define PROCESS_CREATION_CHILD_PROCESS_RESTRICTED 1
#endif

static const wchar_t profile[] = L"LivingQuantumWorld.Inference.1";

static DWORD AllowReadAndExecute(wchar_t *directory, PSID sid)
{
    PACL existing = NULL, replacement = NULL;
    PSECURITY_DESCRIPTOR descriptor = NULL;
    EXPLICIT_ACCESSW entry = {0};
    DWORD result = GetNamedSecurityInfoW(directory, SE_FILE_OBJECT,
        DACL_SECURITY_INFORMATION, NULL, NULL, &existing, NULL, &descriptor);
    if (result != ERROR_SUCCESS)
        return result;

    entry.grfAccessPermissions = FILE_GENERIC_READ | FILE_GENERIC_EXECUTE;
    entry.grfAccessMode = SET_ACCESS;
    entry.grfInheritance = SUB_CONTAINERS_AND_OBJECTS_INHERIT;
    BuildTrusteeWithSidW(&entry.Trustee, sid);
    result = SetEntriesInAclW(1, &entry, existing, &replacement);
    if (result == ERROR_SUCCESS)
        result = SetNamedSecurityInfoW(directory, SE_FILE_OBJECT,
            DACL_SECURITY_INFORMATION, NULL, NULL, replacement, NULL);
    if (replacement)
        LocalFree(replacement);
    LocalFree(descriptor);
    return result;
}

// Reuse the command line prepared by the trusted Python host. Its first
// argument is the wrapper's path, which is passed as argv[0] to the worker.
int wmain(int argc, wchar_t **argv)
{
    wchar_t directory[MAX_PATH * 2];
    wchar_t worker[MAX_PATH * 2];
    wchar_t *command = _wcsdup(GetCommandLineW());
    wchar_t *split;
    PSID sid = NULL;
    SECURITY_CAPABILITIES capabilities = {0};
    DWORD childPolicy = PROCESS_CREATION_CHILD_PROCESS_RESTRICTED;
    SIZE_T attributeBytes = 0;
    STARTUPINFOEXW startup = {0};
    PROCESS_INFORMATION process = {0};
    JOBOBJECT_EXTENDED_LIMIT_INFORMATION limits = {0};
    HANDLE job = NULL;
    HANDLE pipes[3] = {0};
    DWORD handles[] = { STD_INPUT_HANDLE, STD_OUTPUT_HANDLE, STD_ERROR_HANDLE };
    const char *stage = "resolve launcher path";
    DWORD status = 125;
    DWORD error = ERROR_INVALID_PARAMETER;
    HRESULT hr;
    BOOL initialized = FALSE;
    BOOL probe = argc == 3 && wcscmp(argv[1], L"--probe") == 0;

    DWORD pathLength = GetModuleFileNameW(NULL, directory, ARRAYSIZE(directory));
    if (!command || !pathLength || pathLength == ARRAYSIZE(directory))
        goto done;
    split = wcsrchr(directory, L'\\');
    if (!split)
        goto done;
    *split = L'\0';
    if (swprintf(worker, ARRAYSIZE(worker), L"%ls\\%ls", directory,
            probe ? L"sandbox-probe.exe" : L"offline-worker.exe") < 0)
        goto done;

    // Profile creation is scoped to this user. Reuse its SID on later launches.
    stage = "CreateAppContainerProfile";
    hr = CreateAppContainerProfile(profile, profile, profile, NULL, 0, &sid);
    if (hr == HRESULT_FROM_WIN32(ERROR_ALREADY_EXISTS)) {
        stage = "DeriveAppContainerSidFromAppContainerName";
        hr = DeriveAppContainerSidFromAppContainerName(profile, &sid);
    }
    if (FAILED(hr)) {
        error = (DWORD)hr;
        goto done;
    }
    stage = "grant packaged model read/execute access";
    error = AllowReadAndExecute(directory, sid);
    if (error != ERROR_SUCCESS)
        goto done;
    capabilities.AppContainerSid = sid; // No network or other capabilities.

    stage = "duplicate standard handles";
    for (size_t i = 0; i < ARRAYSIZE(pipes); ++i)
        if (!DuplicateHandle(GetCurrentProcess(), GetStdHandle(handles[i]),
                GetCurrentProcess(), &pipes[i], 0, TRUE, DUPLICATE_SAME_ACCESS))
            goto win_error;

    stage = "initialize process attributes";
    InitializeProcThreadAttributeList(NULL, 3, 0, &attributeBytes);
    startup.lpAttributeList = HeapAlloc(GetProcessHeap(), 0, attributeBytes);
    if (!startup.lpAttributeList
        || !InitializeProcThreadAttributeList(startup.lpAttributeList, 3, 0, &attributeBytes))
        goto win_error;
    initialized = TRUE;
    stage = "set AppContainer and handle attributes";
    if (!UpdateProcThreadAttribute(startup.lpAttributeList, 0, PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES,
            &capabilities, sizeof(capabilities), NULL, NULL)
        || !UpdateProcThreadAttribute(startup.lpAttributeList, 0, PROC_THREAD_ATTRIBUTE_CHILD_PROCESS_POLICY,
            &childPolicy, sizeof(childPolicy), NULL, NULL)
        || !UpdateProcThreadAttribute(startup.lpAttributeList, 0, PROC_THREAD_ATTRIBUTE_HANDLE_LIST,
            pipes, sizeof(pipes), NULL, NULL))
        goto win_error;

    stage = "configure worker job";
    job = CreateJobObjectW(NULL, NULL);
    limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
                                          | JOB_OBJECT_LIMIT_ACTIVE_PROCESS;
    limits.BasicLimitInformation.ActiveProcessLimit = 1;
    if (!job || !SetInformationJobObject(job, JobObjectExtendedLimitInformation, &limits, sizeof(limits)))
        goto win_error;

    startup.StartupInfo.cb = sizeof(startup);
    startup.StartupInfo.dwFlags = STARTF_USESTDHANDLES;
    startup.StartupInfo.hStdInput = pipes[0];
    startup.StartupInfo.hStdOutput = pipes[1];
    startup.StartupInfo.hStdError = pipes[2];

    // Let the worker inherit the caller's console. CREATE_NO_WINDOW can
    // fail while Windows initializes a console executable in isolation.
    SetErrorMode(GetErrorMode() | SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX);
    stage = "CreateProcessW";
    if (!CreateProcessW(worker, command, NULL, NULL, TRUE,
            EXTENDED_STARTUPINFO_PRESENT | CREATE_SUSPENDED,
            NULL, directory, &startup.StartupInfo, &process))
        goto win_error;
    stage = "AssignProcessToJobObject";
    if (!AssignProcessToJobObject(job, process.hProcess))
        goto win_error;
    stage = "ResumeThread";
    if (ResumeThread(process.hThread) == (DWORD)-1)
        goto win_error;
    stage = "wait for the isolated worker";
    if (WaitForSingleObject(process.hProcess, INFINITE) != WAIT_OBJECT_0
        || !GetExitCodeProcess(process.hProcess, &status))
        goto win_error;
    goto done;

win_error:
    error = GetLastError();
    if (process.hProcess)
        TerminateProcess(process.hProcess, 125);
done:
    if (status == 125)
        fprintf(stderr, "Windows inference isolation failed at %s (0x%08lx).\n", stage, (unsigned long)error);
    if (job)
        CloseHandle(job);
    if (process.hProcess)
        CloseHandle(process.hProcess);
    if (process.hThread)
        CloseHandle(process.hThread);
    for (size_t i = 0; i < ARRAYSIZE(pipes); ++i)
        if (pipes[i])
            CloseHandle(pipes[i]);
    if (initialized)
        DeleteProcThreadAttributeList(startup.lpAttributeList);
    if (startup.lpAttributeList)
        HeapFree(GetProcessHeap(), 0, startup.lpAttributeList);
    if (sid)
        FreeSid(sid);
    free(command);
    return status;
}

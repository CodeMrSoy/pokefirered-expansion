#include <stdio.h>
#ifdef _WIN32
#define _UNICODE
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>

// A nonblocking connect may remain pending even when an eventual completion
// will be denied. Only an explicit access error counts as a restriction.
static int ProbeInternet(void)
{
    struct sockaddr_in address = {0};
    address.sin_family = AF_INET;
    address.sin_port = htons(443);
    if (InetPtonW(AF_INET, L"1.1.1.1", &address.sin_addr) != 1)
        return WSAEINVAL;
    SOCKET net = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (net == INVALID_SOCKET)
        return WSAGetLastError();

    WSAEVENT event = WSACreateEvent();
    int error = 0;
    if (event == WSA_INVALID_EVENT || WSAEventSelect(net, event, FD_CONNECT) == SOCKET_ERROR) {
        error = WSAGetLastError();
    } else if (connect(net, (struct sockaddr *)&address, sizeof(address)) == SOCKET_ERROR) {
        error = WSAGetLastError();
        if (error == WSAEWOULDBLOCK) {
            DWORD wait = WSAWaitForMultipleEvents(1, &event, FALSE, 4000, FALSE);
            if (wait == WSA_WAIT_TIMEOUT) {
                error = WSAETIMEDOUT;
            } else if (wait != WSA_WAIT_EVENT_0) {
                error = WSAGetLastError();
            } else {
                WSANETWORKEVENTS events = {0};
                if (WSAEnumNetworkEvents(net, event, &events) == SOCKET_ERROR)
                    error = WSAGetLastError();
                else if (events.lNetworkEvents & FD_CONNECT)
                    error = events.iErrorCode[FD_CONNECT_BIT];
            }
        }
    }
    closesocket(net);
    if (event != WSA_INVALID_EVENT)
        WSACloseEvent(event);
    return error;
}

int wmain(int argc, wchar_t **argv)
{
    WSADATA data;
    STARTUPINFOW startup = { .cb = sizeof(startup) };
    PROCESS_INFORMATION child = {0};
    wchar_t shell[MAX_PATH];
    wchar_t command[] = L"cmd.exe /d /c exit 0";
    HANDLE file;
    BOOL readDenied, writeDenied, processDenied;

    if (argc != 3 || WSAStartup(MAKEWORD(2, 2), &data))
        return 2;
    file = CreateFileW(argv[2], GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    readDenied = file == INVALID_HANDLE_VALUE && GetLastError() == ERROR_ACCESS_DENIED;
    if (file != INVALID_HANDLE_VALUE)
        CloseHandle(file);
    file = CreateFileW(argv[2], GENERIC_WRITE, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    writeDenied = file == INVALID_HANDLE_VALUE && GetLastError() == ERROR_ACCESS_DENIED;
    if (file != INVALID_HANDLE_VALUE)
        CloseHandle(file);

    UINT length = GetSystemDirectoryW(shell, ARRAYSIZE(shell));
    if (!length || length + 9 >= ARRAYSIZE(shell))
        return 2;
    wcscat(shell, L"\\cmd.exe");
    BOOL started = CreateProcessW(shell, command, NULL, NULL, FALSE,
        CREATE_NO_WINDOW, NULL, NULL, &startup, &child);
    DWORD processError = started ? ERROR_SUCCESS : GetLastError();
    processDenied = processError == ERROR_ACCESS_DENIED || processError == 367;
    if (started) {
        WaitForSingleObject(child.hProcess, 1000);
        CloseHandle(child.hThread);
        CloseHandle(child.hProcess);
    }

    int netError = ProbeInternet();
    BOOL netDenied = netError == WSAEACCES;
    printf("Internet connection: %s (Winsock %d)\n",
        netDenied ? "access denied" : netError ? "inconclusive" : "connected", netError);
    WSACleanup();
    printf("Read denied=%d, write denied=%d, process denied=%d, internet denied=%d\n",
        readDenied, writeDenied, processDenied, netDenied);
    return !(readDenied && writeDenied && processDenied && netDenied);
}
#else
#include <errno.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <unistd.h>

extern int LivingWorldRestrictWorker(void);

int main(int argc, char **argv)
{
    if (argc != 2)
        return 2;
    if (LivingWorldRestrictWorker() != 0) {
        perror("Could not enable Linux worker isolation");
        return 125;
    }
    int fd = open(argv[1], O_RDONLY);
    int read_denied = fd == -1 && errno == EPERM;
    if (fd >= 0)
        close(fd);
    fd = open(argv[1], O_WRONLY);
    int write_denied = fd == -1 && errno == EPERM;
    if (fd >= 0)
        close(fd);
    fd = socket(AF_INET, SOCK_STREAM, 0);
    int net_denied = fd == -1 && errno == EPERM;
    if (fd >= 0)
        close(fd);
    char *args[] = {"/bin/true", NULL};
    execv(args[0], args);
    int exec_denied = errno == EPERM;
    printf("Read denied=%d, write denied=%d, exec denied=%d, socket denied=%d\n",
        read_denied, write_denied, exec_denied, net_denied);
    return !(read_denied && write_denied && exec_denied && net_denied);
}
#endif

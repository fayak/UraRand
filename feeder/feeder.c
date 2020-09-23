#include <err.h>
#include <linux/random.h>
#include <stdio.h>
#include <string.h>
#include <sys/fcntl.h>
#include <sys/ioctl.h>

int main(void) {
    struct {
        int entropy_count;
        int buf_size;
        char buf[32];
    } entropy;

    int randfd;
    if ((randfd = open("/dev/random", O_WRONLY)) < 0)
        err(1, "/dev/random");

    int count = 0;
    while ((count = fread(entropy.buf, 1, sizeof(entropy.buf), stdin)) > 0)
    {
        entropy.entropy_count = count * 8;
        entropy.buf_size = count;
        if(ioctl(randfd, RNDADDENTROPY, &entropy) < 0)
            err(1, "ioctl RNDADDENTROPY");
    }

    return 0;
}

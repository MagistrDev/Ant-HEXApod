#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include <time.h>

#define BUF_SIZE 10

int main(int argc, char const *argv[])
{
    int fd = -1;
    ssize_t fr = 0;
    char buf[BUF_SIZE + 1];
    if (argc < 2)
    {
        printf("No read file\n");
        return(1);
    }
    time_t now;
    bzero((void*)buf, BUF_SIZE + 1);
    if (!(fd = open(argv[1], O_RDWR | O_NONBLOCK)))
        printf("no open file\n");
    while (1)
        if ((fr = read(fd, buf, BUF_SIZE)) > 0)
        {
            time(&now);
            printf("%s\tread - '%s'\n", ctime(&now), buf);
            bzero((void*)buf, BUF_SIZE + 1);
        }
    return 0;
}

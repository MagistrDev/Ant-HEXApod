#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>

int main(int argc, char const *argv[])
{
    int fd = -1;
    ssize_t fr = 0;
    char buf[100];
    
    bzero((void*)buf, 100);
    if (!(fd = open("test_file", O_RDWR | O_NONBLOCK)))
        printf("no open file\n");
    while (1)
        if ((fr = read(fd, buf, 10)) > 0)
        {
            printf("\tread\t-\t'%s'\n", buf);
            bzero((void*)buf, 10);
        }
    return 0;
}
//2

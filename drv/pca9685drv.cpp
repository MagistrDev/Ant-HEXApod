#include "pca9685drv.h"


int *ptr

int init() {
    return 1;
}

void bla()
{
  int *pptr

  pptr = 0x545645654
}


int main(void) {

  ptr = (int*)0;
    ptr++;
  bla();
    return 2;
  }

  unsigned char buffer[2] = {0x35, 7};
  while (1){
    buffer[1] = ((buffer[1] == 7) ? 1 : 7);
    status = write(fd, buffer, 2);
    if (status == -1) {
        printf("Failed to write register 0x0C.\n");
        return 3;
    }
    printf("%i\n",buffer[0]);
    usleep(500000);
  }
  close(fd);
}



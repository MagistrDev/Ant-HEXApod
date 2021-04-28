#include "pca9685drv.h"


int main(void) {
  int fd = open("/dev/i2c-1", O_RDWR | O_NONBLOCK);
  if (fd == -1) {
    printf("Failed to open /dev/i2c-1\n");
    return 1;
  }

  int status = ioctl(fd, I2C_SLAVE, 0x41);
  if (status == -1) {
    printf("Failed to acquire bus access and/or talk to slave.\n");
    return 2;
  }

  unsigned char buffer[1] = {0};
  while (1){
    buffer[0] = (buffer[0] == 7) ? 0 : 1;
    status = write(fd, buffer, 1);
    if (status == -1) {
        printf("Failed to write register 0x0C.\n");
        return 3;
    }
    printf("%i\n",buffer[0]);
    usleep(500000);
  }

//   status = read(fd, buffer, 1);
//   if (status == -1) {
//     printf("Failed to read from register 0x0C.\n");
//     return 4;
//   }

//   printf("WHO_AM_I = 0x%X\n", (int)buffer[0]);

  close(fd);
}



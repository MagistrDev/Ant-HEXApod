#include "pca9685drv.h"

#include <linux/module.h>
#include <linux/init.h>

int main(void) {
  int fd = open("/dev/i2c-1", O_RDWR | O_NONBLOCK);
  if (fd == -1) {
    printf("Failed to open /dev/i2c-1\n");
    return 1;
  }
  printf("%x\n",I2C_SLAVE);
  int status = ioctl(fd, I2C_SLAVE, 0x41);
  if (status == -1) {
    printf("Failed to acquire bus access and/or talk to slave.\n");
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

//   status = read(fd, buffer, 1);
//   if (status == -1) {
//     printf("Failed to read from register 0x0C.\n");
//     return 4;
//   }

//   printf("WHO_AM_I = 0x%X\n", (int)buffer[0]);

  close(fd);
}

#ifndef _PCA9685_DRV_H_
#define _PCA9685_DRV_H_

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

// Default address:
#define PCA9685_ADDRESS    = 0x40

typedef enum {
    LINK_COXA,
    LINK_FEMUR,
    LINK_TIBIA
} link_id_t;

typedef struct {
    
    // Current link state
    float angle;
    
    // Link configuration
    uint32_t length;
    int32_t  zero_rotate;
    int32_t  min_angle;
    int32_t  max_angle;
    
} link_info_t;

typedef struct {
    int     x;
    int     y;
    int     z;
    /* data */
} point_3d_t;


typedef struct {
    
    point_3d_t position;
    // path_3d_t  movement_path;
    
    link_info_t links[3];
    
} limb_info_t;

// Registers/etc:
#define MODE1              = 0x00
#define MODE2              = 0x01
#define SUBADR1            = 0x02
#define SUBADR2            = 0x03
#define SUBADR3            = 0x04
#define PRESCALE           = 0xFE
#define LED0_ON_L          = 0x06
#define LED0_ON_H          = 0x07
#define LED0_OFF_L         = 0x08
#define LED0_OFF_H         = 0x09
#define ALL_LED_ON_L       = 0xFA
#define ALL_LED_ON_H       = 0xFB
#define ALL_LED_OFF_L      = 0xFC
#define ALL_LED_OFF_H      = 0xFD
 
// Bits:
#define RESTART            = 0x80
#define SLEEP              = 0x10
#define ALLCALL            = 0x01
#define INVRT              = 0x10
#define OUTDRV             = 0x04
 
//  Channels
#define CHANNEL00          = 0x00
#define CHANNEL01          = 0x01
#define CHANNEL02          = 0x02
#define CHANNEL03          = 0x03
#define CHANNEL04          = 0x04
#define CHANNEL05          = 0x05
#define CHANNEL06          = 0x06
#define CHANNEL07          = 0x07
#define CHANNEL08          = 0x08
#define CHANNEL09          = 0x09
#define CHANNEL10          = 0x0A
#define CHANNEL11          = 0x0B
#define CHANNEL12          = 0x0C
#define CHANNEL13          = 0x0D
#define CHANNEL14          = 0x0E
#define CHANNEL15          = 0x0F

class i2c_bus
{
private:
    /* data */
    _
public:
    i2c_bus(int addres);
    ~i2c_bus();
};

i2c_bus::i2c_bus(/* args */)
{
}

i2c_bus::~i2c_bus()
{
}


class PCA9685
{
private:
    /* data */
    char    _adress;
public:
    PCA9685(/* args */);
    PCA9685();
};

pca9685drv::pca9685drv(/* args */)
{
}

pca9685drv::~pca9685drv()
{
}


#endif
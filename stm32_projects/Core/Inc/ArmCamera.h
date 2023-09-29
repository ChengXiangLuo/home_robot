#ifndef __ARMCAMERA_H
#define __ARMCAMERA_H
#include "main.h"
#define zero_pwm 50
#define full_pwm 250

void ArmCam_init(void);
void joint1_cmd(int16_t angle);
void joint2_cmd(int16_t angle);

#endif

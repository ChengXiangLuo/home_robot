#ifndef __CARMOTOR_H__
#define __CARMOTOR_H__
#include "main.h"
#define k_V2PWM 130

void CarMotor_init(void);
void Frontal_Right_run2forward(uint16_t pwm);
void Frontal_Right_run2back(uint16_t pwm);
void Frontal_left_run2forward(uint16_t pwm);
void Frontal_left_run2back(uint16_t pwm);
void back_Right_run2forward(uint16_t pwm);
void back_Right_run2back(uint16_t pwm);
void back_left_run2forward(uint16_t pwm);
void back_left_run2back(uint16_t pwm);
void carMove2F(float v);
void carMove2B(float v);
void carMove2R(float v);
void carMove2L(float v);
void carRotate2L(float v);
void carRotate2R(float v);
void carStop(void);

#endif

/**
  ******************************************************************************
  * @file           : CarMotor.c
  * @brief          : ����pwm���Ƶ������ת���ٶ�
  ******************************************************************************
  * @attention		������stm32f103c8t6��tim3:ͨ��1~4 tim4:ͨ��1~4
  ******************************************************************************
  */
#include "CarMotor.h"
#include "tim.h"

/**
 * @brief  pwm��ʱ����ʼ��
 * @param  ��
 * @retval ��
 */
void CarMotor_init(void)
{
	HAL_TIM_PWM_Start(&htim3,TIM_CHANNEL_1);
	HAL_TIM_PWM_Start(&htim3,TIM_CHANNEL_2);
	
	HAL_TIM_PWM_Start(&htim3,TIM_CHANNEL_3);
	HAL_TIM_PWM_Start(&htim3,TIM_CHANNEL_4);
	
	HAL_TIM_PWM_Start(&htim4,TIM_CHANNEL_1);
	HAL_TIM_PWM_Start(&htim4,TIM_CHANNEL_2);
	
	HAL_TIM_PWM_Start(&htim4,TIM_CHANNEL_3);
	HAL_TIM_PWM_Start(&htim4,TIM_CHANNEL_4);
}

/**
 * @brief		�趨Pwm
 * @param	
 * @retval
 */
void back_Right_run2forward(uint16_t pwm)
{
	__HAL_TIM_SetCompare(&htim3,TIM_CHANNEL_3,0);
	__HAL_TIM_SetCompare(&htim3,TIM_CHANNEL_4,pwm);
}

void back_Right_run2back(uint16_t pwm)
{
	__HAL_TIM_SetCompare(&htim3,TIM_CHANNEL_3,pwm);
	__HAL_TIM_SetCompare(&htim3,TIM_CHANNEL_4,0);
}

void back_left_run2forward(uint16_t pwm)
{
	__HAL_TIM_SetCompare(&htim3,TIM_CHANNEL_1,0);
	__HAL_TIM_SetCompare(&htim3,TIM_CHANNEL_2,pwm);
}

void back_left_run2back(uint16_t pwm)
{
	__HAL_TIM_SetCompare(&htim3,TIM_CHANNEL_1,pwm);
	__HAL_TIM_SetCompare(&htim3,TIM_CHANNEL_2,0);
}

void Frontal_left_run2forward(uint16_t pwm)
{
	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_3,0);
	__HAL_TIM_SetCompare(&htim4 ,TIM_CHANNEL_4,pwm);
}

void Frontal_left_run2back(uint16_t pwm)
{
	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_3,pwm);
	__HAL_TIM_SetCompare(&htim4 ,TIM_CHANNEL_4,0);
}

void Frontal_Right_run2forward(uint16_t pwm)
{
	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_1,0);
	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_2,pwm);
}

void Frontal_Right_run2back(uint16_t pwm)
{
	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_1,pwm);
	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_2,0);
}

void carMove2F(float v)
{
	uint8_t pwm = v*k_V2PWM;
	Frontal_left_run2forward(pwm);
	Frontal_Right_run2forward(pwm);
	back_left_run2forward(pwm);
	back_Right_run2forward(pwm);
}

void carMove2B(float v)
{
	uint8_t pwm = (-1)*v*k_V2PWM;
	Frontal_left_run2back(pwm);
	Frontal_Right_run2back(pwm);
	back_left_run2back(pwm);
	back_Right_run2back(pwm);
}

void carMove2R(float v)
{
	uint8_t pwm = (-1)*v*k_V2PWM;
	Frontal_left_run2back(pwm);
	Frontal_Right_run2forward(pwm);
	back_left_run2forward(pwm);
	back_Right_run2back(pwm);
}

void carMove2L(float v)
{
	uint8_t pwm = v*k_V2PWM;
	Frontal_left_run2forward(pwm);
	Frontal_Right_run2back(pwm);
	back_Right_run2back(pwm);
	back_Right_run2forward(pwm);
}

void carRotate2R(float v)
{
	uint8_t pwm = (-1)*v*k_V2PWM;
	Frontal_left_run2forward(pwm);	
	Frontal_Right_run2back(pwm);
	back_left_run2forward(pwm);
	back_Right_run2back(pwm);	
}

void carRotate2L(float v)
{
	uint8_t pwm = v*k_V2PWM;
	Frontal_left_run2back(pwm);
	Frontal_Right_run2forward(pwm);
	back_Right_run2back(pwm);
	back_Right_run2forward(pwm);
}

void carStop(void)
{
	__HAL_TIM_SetCompare(&htim3,TIM_CHANNEL_3,0);
	__HAL_TIM_SetCompare(&htim3,TIM_CHANNEL_4,0);
	__HAL_TIM_SetCompare(&htim3,TIM_CHANNEL_1,0);
	__HAL_TIM_SetCompare(&htim3,TIM_CHANNEL_2,0);
	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_3,0);
	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_4,0);
	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_1,0);
	__HAL_TIM_SetCompare(&htim4,TIM_CHANNEL_2,0);
}

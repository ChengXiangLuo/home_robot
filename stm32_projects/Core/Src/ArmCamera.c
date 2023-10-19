/**
  ******************************************************************************
  * @file           : ArmCamera.c
  * @brief          : 控制两个舵机，以控制摄像头的位置
  ******************************************************************************
  * @attention
  ******************************************************************************
  */
#include "ArmCamera.h"
#include "main.h"
#include "tim.h"


/**
 * @brief 舵机初始化
 * @param 无
 * @retval 无
 */
void ArmCam_init(void)
{
	HAL_TIM_PWM_Start(&htim2,TIM_CHANNEL_1);
	HAL_TIM_PWM_Start(&htim2,TIM_CHANNEL_2);
	
	joint1_cmd(90);
	joint2_cmd(0);
}	

/**
 * @brief 控制舵机1
 * @param angle:角度
 * @retval 无
 */
void joint1_cmd(int16_t angle)
{
	int16_t pwm=0;
	if(angle>0 && angle<150)
	{
		pwm = angle*180/(full_pwm-zero_pwm)+zero_pwm;
		__HAL_TIM_SetCompare(&htim2,TIM_CHANNEL_1,pwm);
	}
}

/**
 * @brief 控制舵机2
 * @param angle:角度
 * @retval 无
 */
void joint2_cmd(int16_t angle)
{
	int16_t pwm=0;
	if(angle>0 && angle<150)
	{
		pwm = angle*180/(full_pwm-zero_pwm)+zero_pwm;
		__HAL_TIM_SetCompare(&htim2,TIM_CHANNEL_2,pwm);
	}
}

/**
 * @brief 控制舵机旋转角度增量
 * @param Anv1：舵机1  Anv2：舵机2
 * @retval 无
 */
void arm_AngV_cmd(int Anv_1, int Anv_2)
{
	static int pre_angv1,pre_angv2;
	pre_angv1+=Anv_1;
	pre_angv2+=Anv_2;
	if(pre_angv1<0)
	{
		pre_angv1 = 0;
	}else if(pre_angv1>150)
	{
		pre_angv1 = 150;
	}else if(pre_angv2<0)
	{
		pre_angv2 = 0;
	}else if(pre_angv2>150)
	{
		pre_angv2 = 150;
	}
	
	joint1_cmd(pre_angv1);
	joint2_cmd(pre_angv2);
	
}

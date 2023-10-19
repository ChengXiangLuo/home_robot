/**
  ******************************************************************************
  * @file           : ArmCamera.c
  * @brief          : ��������������Կ�������ͷ��λ��
  ******************************************************************************
  * @attention
  ******************************************************************************
  */
#include "ArmCamera.h"
#include "main.h"
#include "tim.h"


/**
 * @brief �����ʼ��
 * @param ��
 * @retval ��
 */
void ArmCam_init(void)
{
	HAL_TIM_PWM_Start(&htim2,TIM_CHANNEL_1);
	HAL_TIM_PWM_Start(&htim2,TIM_CHANNEL_2);
	
	joint1_cmd(90);
	joint2_cmd(0);
}	

/**
 * @brief ���ƶ��1
 * @param angle:�Ƕ�
 * @retval ��
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
 * @brief ���ƶ��2
 * @param angle:�Ƕ�
 * @retval ��
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
 * @brief ���ƶ����ת�Ƕ�����
 * @param Anv1�����1  Anv2�����2
 * @retval ��
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

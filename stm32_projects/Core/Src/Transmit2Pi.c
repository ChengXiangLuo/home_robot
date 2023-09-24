/**
  ******************************************************************************
  * @file           : Transmit2Pi.c
  * @brief          : ��ݮ�ɺ�STM32���ڴ���
  ******************************************************************************
  * @attention
  ******************************************************************************
  */
#include "Transmit2Pi.h"
#include "stdio.h"
#include "CarMotor.h"
#include "ArmCamera.h"

uint8_t aRxBuffer;
uint8_t RxBuffer[30];//���ջ���



/**
 * @brief  С��ת���ɰ�λ����������С������0.1����Χ��7.0
 * @param  num:Ҫת��������
 * @retval decimalValue:��λ����λΪ1������������λΪ�����������λΪС����(����-1.1 -> 1 001 0001)
 */
uint8_t velocity_f2b(float num)
{
    uint8_t binary[8] = {0};
    uint8_t decimalValue = 0;

    if (num < 0)
    {
        binary[7] = 1;
        num = -num;
    }

    int integerPart = (int)num;
    int fractionalPart = (int)((num - integerPart) * 100 + 1) / 10;

    for (int i = 4; i <= 6; i++)
    {
        binary[i] = integerPart % 2;
        integerPart = integerPart / 2;
    }
    for (int i = 0; i <= 3; i++)
    {
        binary[i] = fractionalPart % 2;
        fractionalPart = fractionalPart / 2;
    }
		for (int i = 7; i >= 0; i--)
    {
        decimalValue = decimalValue * 2 + binary[i];
    }
		
		return decimalValue;
}

/**
 * @brief 	��λ��������תʮ���ƣ�
 * @param 	bin:����������(��: 1 001 0001 -> -1.1)
 * @retval	decimalValue: ʮ������
 */
float velocity_b2f(uint8_t bin)
{
	uint8_t sign;
	uint8_t integer;
	uint8_t decimal;
	float decimalValue;
	
	sign = (bin&0x80)>>7;
	integer = (bin&0x70)>>4;
	decimal = bin&0x0f;
	
	decimalValue = integer + decimal*0.1;
	
	if(sign==1)
		decimalValue *= -1;
	
	return decimalValue;
}

/**
 * @brief �ж��յ��ĽǶ��Ƿ�Ϸ�
 * @param bin���Ƕ�
 * @retval 
 */
uint16_t angle_b2d(uint8_t bin)
{
	if(bin>180)
	{
		return 0;
	}else{
	return bin;}
}


/**
 * @brief 	�򿪴����ж�
 * @param 	��
 * @retval	��
 */
void transmit2pi_uart_init(void)
{
	HAL_UART_Receive_IT(&huart1, (uint8_t *)&aRxBuffer, 1);
}

/**
 * @brief 	��������ݮ�ɴ��ڷ���������
 * @param 	data �յ�������(��ʽ {0x01 0x00 0x00 0x00 0x00} )
 * @retval	��
 */
void dataFromPi_process(uint8_t *data)
{
	char tx_text[20];
	float velocity_x, velocity_y, velocity_z;
	float joint1_angle,joint2_angle;
	
	uint8_t k=0;
	while(RxBuffer[k++]!='{');
					
	//��һλΪ0x01 ����ٶȴ���
	if(data[k]==0x01)
	{
		velocity_x = velocity_b2f(data[k+1]);
		velocity_y = velocity_b2f(data[k+2]);
		velocity_z = velocity_b2f(data[k+3]);
		sprintf(tx_text,"x:%.2f,y:%.2f,z:%.2f\r\n",velocity_x,velocity_y,velocity_z);
		u1_printf((uint8_t *)tx_text);	
		if(velocity_z==0)
		{
			if(velocity_x==0)
			{
				if(velocity_y>0)
				{
					carMove2L(velocity_y);
				}
				else if(velocity_y<0)
				{
					carMove2R(velocity_y);
				}
				else
				{
					carStop();
				}
			}
			else
			{
				if(velocity_x>0)
				{
					carMove2F(velocity_x);
				}
				else
				{
					carMove2B(velocity_x);
				}
			}
		}
		else
		{
			if(velocity_z>0)
			{
				carRotate2L(velocity_z);
			}
			else
			{
				carRotate2R(velocity_z);
			}
		}
	} 
	//��һλΪ0x02 �������
	else if(data[k]==0x02)
	{
		joint1_angle = angle_b2d(data[k+1]);
		joint2_angle = angle_b2d(data[k+2]);
		sprintf(tx_text,"j1:%.2f,j2:%.2f\r\n",joint1_angle,joint2_angle);
		u1_printf((uint8_t *)tx_text);
		
		joint1_cmd(joint1_angle);		
		joint2_cmd(joint2_angle);
	}
}

/**
 * @brief 	���ڻص�����������ݮ�ɴ��ڣ�������ݮ�ɷ��͵�����
 * @param 	���ָ�� *huart
 * @retval	��
 */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    static uint8_t Uart1_Rx_Cnt = 0;
		

	
    if (huart == &huart1)
    {
        RxBuffer[++Uart1_Rx_Cnt] = aRxBuffer;   
			
				if(RxBuffer[Uart1_Rx_Cnt] == 0x7D)//�յ���������
				{
					dataFromPi_process(RxBuffer);
					
					//��������ͽ��ջ���
          memset(RxBuffer, 0x00, sizeof(RxBuffer)); 
					Uart1_Rx_Cnt = 0;
				}

				
				HAL_UART_Receive_IT(&huart1, (uint8_t *)&aRxBuffer, 1);
    }
}


/**
  ******************************************************************************
  * @file           : Transmit2Pi.c
  * @brief          : 树莓派和STM32串口处理
  ******************************************************************************
  * @attention
  ******************************************************************************
  */
#include "Transmit2Pi.h"
#include "stdio.h"
#include "CarMotor.h"
#include "ArmCamera.h"
uint8_t aRxBuffer;
uint8_t RxBuffer[30];//接收缓存

uint8_t aRxBuffer_u2;
uint8_t RxBuffer_u2[30];//uart2接收缓存

uint8_t hmi_is_OK = 0; //判断串口屏是否加载完成
uint8_t Page_temp = 0; //串口屏此时页面 
/**
 * @brief  小数转换成八位二进制数，小数精度0.1，范围±7.0
 * @param  num:要转化的数字
 * @retval decimalValue:八位，首位为1则负数，接着三位为整数，后边四位为小数。(例：-1.1 -> 1 001 0001)
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
 * @brief 	八位二进制数转十进制，
 * @param 	bin:二进制数。(例: 1 001 0001 -> -1.1)
 * @retval	decimalValue: 十进制数
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
 * @brief 判断收到的角度是否合法
 * @param bin：角度
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
 * @brief 	打开串口中断
 * @param 	无
 * @retval	无
 */
void my_uart_init(void)
{
	HAL_UART_Receive_IT(&huart1, (uint8_t *)&aRxBuffer, 1);
	HAL_UART_Receive_IT(&huart2, (uint8_t *)&aRxBuffer_u2, 1);
	//给串口屏发初始化命令，防止上电时串口杂波影响
	u2_printf("\x00\xff\xff\xff");
}

/**
 * @brief 	处理从树莓派串口发来的数据
 * @param 	data 收到的数据(格式 {0x01 0x00 0x00 0x00 0x00} )
 * @retval	无
 */
void dataFromPi_process(uint8_t *data)
{
//	char tx_text[20];
	float velocity_x, velocity_y, velocity_z;
	float joint1_angV,joint2_angV;
	
	uint8_t k=0;
	while(RxBuffer[k++]!='{');
					
	//第一位为0x01 电机速度处理
	if(data[k]==0x01)
	{
		velocity_x = velocity_b2f(data[k+1]);
		velocity_y = velocity_b2f(data[k+2]);
		velocity_z = velocity_b2f(data[k+3]);
//		sprintf(tx_text,"x:%.2f,y:%.2f,z:%.2f\r\n",velocity_x,velocity_y,velocity_z);
//		u1_printf((uint8_t *)tx_text);	
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
	//第一位为0x02 舵机处理
	else if(data[k]==0x02)
	{
		joint1_angV = (int)velocity_b2f(data[k+1]);
		joint2_angV = (int)velocity_b2f(data[k+2]);
//		sprintf(tx_text,"j1:%.2f,j2:%.2f\r\n",joint1_angV,joint2_angV);
//		u1_printf((uint8_t *)tx_text);
		arm_AngV_cmd(joint1_angV,joint2_angV);

	}
	else if(data[k]==0x03)
	{
		u2_printf("page features\xff\xff\xff");
		Page_temp=0;
	}
}

/**
 * @brief 处理串口屏发来的数据
 * @param data：格式 {0x00},00返回，01电脑控制，02语音聊天，03监护，04看诊
 * @retval 无
 */
void dataFromHMI_process(uint8_t *data)
{
	uint8_t k=0;
	while(RxBuffer_u2[k++]!='{');
	if(data[k]==0x00)
	{
		Page_temp=0;
		u2_printf("page features\xff\xff\xff");
	}
	else if(data[k]==0x01)
	{
		Page_temp=1;
		u2_printf("page page_PCctl\xff\xff\xff");
	}
	else if(data[k]==0x02)
	{
		Page_temp=2;
		u2_printf("page page_Talk\xff\xff\xff");
	}
	else if(data[k]==0x03)
	{
		Page_temp=3;
		u2_printf("page page_Watch\xff\xff\xff");
	}
	else if(data[k]==0x04)
	{
		Page_temp=4;
		u2_printf("page page_Doctor\xff\xff\xff");
	}
}

/**
 * @brief 	串口回调函数，处理树莓派发送的数据和串口的数据
 * @param 	句柄指针 *huart
 * @retval	无
 */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    static uint8_t Uart1_Rx_Cnt = 0;
		static uint8_t Uart2_Rx_Cnt = 0;
		// 树莓派
    if (huart == &huart1)
    {
        RxBuffer[++Uart1_Rx_Cnt] = aRxBuffer;   
			
				if(RxBuffer[Uart1_Rx_Cnt] == 0x7D)//收到结束符号
				{
					dataFromPi_process(RxBuffer);
					
					//清零计数和接收缓存
          memset(RxBuffer, 0x00, sizeof(RxBuffer)); 
					Uart1_Rx_Cnt = 0;
				}
				
				HAL_UART_Receive_IT(&huart1, (uint8_t *)&aRxBuffer, 1);
    }
		// 串口屏
		else if (huart == &huart2)
    {
        RxBuffer_u2[++Uart2_Rx_Cnt] = aRxBuffer_u2;   
				if(RxBuffer_u2[Uart2_Rx_Cnt] == 0x7D)//收到结束符号
				{
					dataFromHMI_process(RxBuffer_u2);
					
					//清零计数和接收缓存
          memset(RxBuffer_u2, 0x00, sizeof(RxBuffer_u2)); 
					Uart2_Rx_Cnt = 0;
				}

				HAL_UART_Receive_IT(&huart2, (uint8_t *)&aRxBuffer_u2, 1);
    }
}



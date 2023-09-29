#ifndef __TRANSMIT2PI_H__
#define __TRANSMIT2PI_H__
#include "main.h"
#include "usart.h"
#include "string.h"
#define PageFeatures 	0
#define PagePcCtl 		1
#define PageTalk 			2
#define PageWatch 		3
#define PageDoctor 		4

extern uint8_t Page_temp;

void my_uart_init(void);

#endif

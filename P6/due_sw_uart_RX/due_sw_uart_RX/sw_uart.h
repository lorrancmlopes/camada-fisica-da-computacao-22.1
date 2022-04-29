#ifndef SW_UART_HEADER
#define SW_UART_HEADER

#include <Arduino.h>

struct due_sw_uart {
	int pin_rx;
	int baudrate;
	int stopbits;
	int paritybit;
  int databits;
};

typedef struct due_sw_uart due_sw_uart;

#define SW_UART_SUCCESS 		0
#define SW_UART_ERROR_FRAMING 	112
#define SW_UART_ERROR_PARITY  	2
#define SW_UART_NO_PARITY 		0
#define SW_UART_ODD_PARITY 		1
#define SW_UART_EVEN_PARITY 	2


void sw_uart_setup(due_sw_uart *uart, int rx,  int stopbits, int databits, int paritybit);
int  sw_uart_receive_byte(due_sw_uart *uart, char* data);

void _sw_uart_wait_half_T(due_sw_uart *uart);
void _sw_uart_wait_T(due_sw_uart *uart);

#endif

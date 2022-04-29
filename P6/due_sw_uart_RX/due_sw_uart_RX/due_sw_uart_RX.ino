#include "sw_uart.h" //importa a biblioteca

due_sw_uart uart;   

void setup() {  // funçao que não retorna nada
  Serial.begin(9600); 
  sw_uart_setup(&uart, 12, 1, 8, SW_UART_EVEN_PARITY); //(due_sw_uart *uart, rx, stopbits, databits,  paritybit)
}

void loop() {
 receive_byte();
 delay(5);
}

void receive_byte() {
  char data;
  int code = sw_uart_receive_byte(&uart, &data);
  if(code == SW_UART_SUCCESS) {
     Serial.print(data);
  } else if(code == SW_UART_ERROR_PARITY) {
    Serial.println("\nPARITY ERROR");
  } else {
    Serial.println("\nOTHER");
    Serial.print(code);
  }
}

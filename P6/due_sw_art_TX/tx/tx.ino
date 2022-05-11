#include <Arduino.h>
int pino=3;
void setup(){
  pinMode(pino, OUTPUT);
}

int bitdoCaracter(int posicao){
  int bits[8] = {0,1,1,1,0,0,1,1};
  
}

void loop(){
  //start bit
  digitalWrite(pino, HIGH);
  delay(2000);
  digitalWrite(pino, LOW);
  for(int i = 0; i < 2187; i++)
  {
      asm("NOP");
  }
  //data bits: testando s: 0x73   01110011
  digitalWrite(pino, HIGH);
  for(int i = 0; i < 2187; i++) // 1
  {
      asm("NOP");
  }
  digitalWrite(pino, HIGH); //0
  for(int i = 0; i < 2187; i++)
  {
      asm("NOP");
  }
  digitalWrite(pino, LOW); // 0
  for(int i = 0; i < 2187; i++)
  {
      asm("NOP");
  }
  digitalWrite(pino, LOW); //0
  for(int i = 0; i < 2187; i++)
  {
      asm("NOP");
  }
  digitalWrite(pino, HIGH); //0
  for(int i = 0; i < 2187; i++)
  {
      asm("NOP");
  }
  digitalWrite(pino, HIGH); //0
  for(int i = 0; i < 2187; i++)
  {
      asm("NOP");
  }
  digitalWrite(pino, HIGH); //1
  for(int i = 0; i < 2187; i++)
  {
      asm("NOP");
  }
  digitalWrite(pino, LOW); //0
  for(int i = 0; i < 2187; i++)
  {
      asm("NOP");
  }
  digitalWrite(pino, HIGH); //1 (PARIDADE: cinco 1's então 1/HIGH)
  for(int i = 0; i < 2187; i++)
  {
      asm("NOP");
  }
  digitalWrite(pino, HIGH); //1 (PARADA: 1/HIGH)
  for(int i = 0; i < 2187; i++)
  {
      asm("NOP");
  }

}

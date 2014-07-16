#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#include <Servo.h> 

const boolean debug = false;

volatile unsigned char counter = 48; 
volatile unsigned char result = 0; 
volatile int state = LOW;
volatile int left, right, forward;
volatile unsigned char currentState = 'S';

int wallDistance = 70;
long duration, cm;
int temp =0;
int decide =0;

char ChannelA_motor1 = 2;
char ChannelB_motor1 = 12;
char enable1 = 11;
//char enable2 = 12;
char ChannelC_motor2 = 5;
char ChannelD_motor2 = 4;
const int pingPin = 7;

char Direction = 'S';
char Speed= 255;
Servo myservo;  
int pos = 0;    // variable to store the servo position 

void Move(char Direction, char Speed)
{
  switch(Direction){
    case  'R':
      GoRight(Speed);
      break;
    case  'L':
      GoLeft(Speed);
      break;
    case  'F':
      GoForward(Speed);
      break;
    case  'B':
      GoBackword(Speed);
      break;
    case 'S':
      StopMotor();
  }
}
void start_Motors(char max_speed)
{
  char i;
  for(i=60;i<max_speed;i+=100)
  {
    OCR2A = i;
    delay(50);        //delay in starting up 
  }
}
void start_Motors_LR(char max_speed = 80)
{
  char i;
  for(i=60;i<max_speed;i+=5)
  {
    OCR2A = i;
    delay(50);        //delay in starting up 
  }
}

void GoRight(char Speed)
{
  //Serial.print("I am Right, you are wrong \n");w
  digitalWrite(ChannelA_motor1, HIGH);
  digitalWrite(ChannelB_motor1, LOW);
  digitalWrite(ChannelC_motor2, LOW);
  digitalWrite(ChannelD_motor2, HIGH);
  start_Motors_LR();
}

void GoLeft(char Speed)
{
  //Serial.print("I am Left, you are gazar \n");

  digitalWrite(ChannelA_motor1, LOW);
  digitalWrite(ChannelB_motor1, HIGH);
  digitalWrite(ChannelC_motor2, HIGH);
  digitalWrite(ChannelD_motor2, LOW);
  start_Motors_LR();
  /*
  analogWrite(ChannelA_motor1, 0);
  analogWrite(ChannelB_motor1, Speed);
  analogWrite(ChannelC_motor2, Speed);
  analogWrite(ChannelD_motor2, 0);
  */
}

void GoForward(char Speed)
{
  //Serial.print("Keep moving F1orward NEMO \n");
  digitalWrite(ChannelA_motor1, HIGH);
  digitalWrite(ChannelB_motor1, LOW);
  digitalWrite(ChannelC_motor2, HIGH);
  digitalWrite(ChannelD_motor2, LOW);
  start_Motors(Speed);
  
}

void GoBackword(char Speed)
{
  //Serial.print("Keep moving Backward NEMO \n");
  digitalWrite(ChannelA_motor1, LOW);
  digitalWrite(ChannelB_motor1, HIGH);
  digitalWrite(ChannelC_motor2, LOW);
  digitalWrite(ChannelD_motor2, HIGH);
}

void StopMotor()
{
  //Serial.print("I not moving \n");
  digitalWrite(ChannelA_motor1, LOW);
  digitalWrite(ChannelB_motor1, LOW);
  digitalWrite(ChannelC_motor2, LOW);
  digitalWrite(ChannelD_motor2, LOW);
  
}

void setup() {
  pinMode(13,OUTPUT);
  sbi(UCSR0A, U2X0);
  sbi(UCSR0B, RXCIE0); 
  sbi(UCSR0B, RXEN0); 
  sbi(UCSR0B, TXEN0);
  UCSR0C = B00000110;
  UBRR0H = B0;//115200 baud
  UBRR0L = B00010000;
  
   // initialize the digital pin as an output.
  pinMode(ChannelA_motor1, OUTPUT);
  pinMode(ChannelB_motor1, OUTPUT);
  pinMode(ChannelC_motor2, OUTPUT);
  pinMode(ChannelD_motor2, OUTPUT); 
  pinMode(enable1, OUTPUT);  
  digitalWrite(enable1, HIGH);   // turn the LED on (HIGH is the voltage level)
  //pinMode(enable2, OUTPUT);  
  //digitalWrite(enable2, HIGH);
  //TCCR2A = _BV(COM2A1) | _BV(COM2B1) | _BV(WGM21) | _BV(WGM20);
  //TCCR2B = _BV(CS22);
  TCCR2A = _BV(COM2A1) | _BV(COM2B1) | _BV(WGM20) | _BV(WGM21);  //Fast pwm mode 
  TCCR2B = _BV(CS22) | _BV(CS21) | _BV(CS20);                               //prescale value 
  OCR2A = 50;
  uart_send(TCCR2A);
  myservo.attach(6);
  uart_send(TCCR2A);

}

void loop() 
{
   for(pos = 0; pos < 181; pos += 3)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    //Serial.print(pos);
    //Serial.println();
    delay(15);                       // waits 15ms for the servo to reach the position 
    ////////////////////////////////////////////////
   
    pinMode(pingPin, OUTPUT);
    digitalWrite(pingPin, LOW);
    delayMicroseconds(2);
    digitalWrite(pingPin, HIGH);
    delayMicroseconds(5);
    digitalWrite(pingPin, LOW);
    pinMode(pingPin, INPUT);
    duration = pulseIn(pingPin, HIGH);
    cm = microsecondsToCentimeters(duration);
    
     if(pos>0 && pos <20){
       //temp += cm;
         if(cm < wallDistance){
           right = 0;
           if(currentState == 'R'){Move('S',Speed);}
           
           if(debug) uart_send('I');
         }
         else {
           right = 1;
           if(debug) uart_send('R');
           //temp =0;
         }
     }
     if(pos>80 && pos <120){
       //temp += cm;
         if(cm < wallDistance){
           forward = 0;
           if(currentState == 'F'){Move('S',Speed);}
           if(debug) uart_send('I');
           //temp =0;
         }
         else {
           forward =1;
           if(debug) uart_send('F');
           //temp =0;
         }
     }
     if(pos>160 && pos <180){
       //temp += cm;
         if(cm < wallDistance){
           left = 0;
           if(currentState == 'L'){Move('S',Speed);}
           if(debug) uart_send('I');
           //temp =0;
         }
         else {
           left =1;
           if(debug) uart_send('L');
          // temp =0;
         }
     }
      
    
     
     
  }
  /////////////////////////backward loop///////////////////////////////////
  for(pos = 180; pos >0; pos -= 3)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    //Serial.print(pos);
    //Serial.println();
    delay(15);                       // waits 15ms for the servo to reach the position 
    ////////////////////////////////////////////////
   
    pinMode(pingPin, OUTPUT);
    digitalWrite(pingPin, LOW);
    delayMicroseconds(2);
    digitalWrite(pingPin, HIGH);
    delayMicroseconds(5);
    digitalWrite(pingPin, LOW);
    pinMode(pingPin, INPUT);
    duration = pulseIn(pingPin, HIGH);
    cm = microsecondsToCentimeters(duration);
    if(pos<180 && pos >160){
       //temp += cm;
         if(cm < wallDistance){
           left = 0;
           if(currentState == 'L'){Move('S',Speed);}
           if(debug) uart_send('I');
         }
         else {
           left = 1;
           if(debug) uart_send('L');
           //temp =0;
         }
     }
     if(pos<120 && pos >80){
       //temp += cm;
         if(cm < wallDistance){
           forward = 0;
           if(currentState == 'F'){Move('S',Speed);}
           if(debug) uart_send('I');
           //temp =0;
         }
         else {
           forward =1;
           if(debug) uart_send('F');
           //temp =0;
         }
     }
     if(pos<20 && pos >0){
       //temp += cm;
         if(cm < wallDistance){
           right = 0;
           if(currentState == 'R'){Move('S',Speed);}
           if(debug) uart_send('I');
           //temp =0;
         }
         else {
           right =1;
           if(debug) uart_send('R');
          // temp =0;
         }
     }
     
  }
}

long microsecondsToCentimeters(long microseconds)
{
  return microseconds / 29 / 2;
}

ISR(USART_RX_vect)  {
  if(state == HIGH){
    state = LOW;
    digitalWrite(13, LOW);
  }
  else if(state == LOW){
    state = HIGH;
    digitalWrite(13, HIGH);
  }
  counter++;
  result = UDR0; 
  if(result == 'd' && right == 1 ){
    //move left
     currentState = 'R';
     Move('R',Speed);
     //delay(50000);
     //Move('S',Speed);
     //currentState = 'S';
     uart_send('D');
  }
  else if(result == 'a' && left == 1 ){
    //move right
    currentState = 'L';
    Move('L',Speed);
    //delay(50000);
     //Move('S',Speed);
     //currentState = 'S';
    uart_send('A');
  }
  //else if(result == 'w' && forward == 1 ){
  else if(result == 'w' && forward == 1 ){
    //move frward
     currentState = 'F';
     Move('F',Speed);
     uart_send('W');
  }
  else if(result == 's' ){
    //move frward
     currentState = 'S';
     Move('S',Speed);
     uart_send('S');
  }
  else if(result == 'c' ){
     uart_send('C');
     uart_send(0);
  }
  else {
    //stop
    currentState = 'S';
    Move('S',Speed);
    uart_send('S');
  }
}


void uart_send(unsigned char dat) {
  while(! (UCSR0A & ( 1 << UDRE0))  );  // until dararegister is NOT empty 
  UDR0 = dat;                           
}

/*unsigned char uart_read() {
  while(!  (UCSR0A & (1 << RXC0)) );  // until Receive complete is NOT complete 
  return UDR0;
}*/

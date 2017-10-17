#include "mbed.h"

#define SERIAL_BUFFER_SIZE 16

Serial pc(USBTX, USBRX);
DigitalOut led1(LED1);
char buf[SERIAL_BUFFER_SIZE];
int serialCount = 0;
bool serialData = false;

float testarr0[] = {
-0.068,
-0.034,
0.001, 
0.035, 
0.069, 
0.101, 
0.129, 
0.154, 
0.174, 
0.188, 
0.197, 
0.2,   
0.197, 
0.188, 
0.174, 
0.154, 
0.129, 
0.101, 
0.069, 
0.035, 
0.001, 
-0.034,
-0.068,
-0.099,
-0.128,
-0.153,
-0.173,
-0.187,
-0.196,
-0.2,  
-0.196,
-0.187,
-0.173,
-0.153,
-0.128
};

float testarr1[] = {
 -0.128,
 -0.153,
-0.173, 
-0.187, 
-0.196, 
-0.2,  0
-0.196, 
-0.187, 
-0.173, 
-0.153, 
-0.128, 
-0.099, 
-0.068, 
-0.034, 
0.001,  
0.035,  
0.069,  
0.101,  
0.129,  
0.154,  
0.174,  
 0.188, 
 0.197, 
 0.2,   
 0.197, 
 0.188, 
 0.174, 
 0.154, 
 0.129, 
 0.101, 
 0.069, 
 0.035, 
 0.001, 
 -0.034,
 -0.068
};

float testarr2[] = {
 0.197,
 0.188,
0.174,
0.154,
0.129,
.101,
0.069,
0.035,
0.001,
-0.034,
-0.068,
-0.099,
-0.128,
-0.153,
-0.173,
-0.187,
-0.196,
-0.2,
-0.196,
-0.187,
-0.173,
-0.153,
-0.128,
-0.1,
-0.068,
-0.034,
-0.0,
0.035,
0.069,
0.101,
0.129,
0.154,
0.174,
 0.188,
 0.197
};

float trianglearr0[] = {0.1, 0.1, -0.2};
float trianglearr1[] = {0.1, -0.2, 0.1};
float trianglearr2[] = {-0.2, 0.1, 0.1};

float squarearr0[] = {0.1, 0.175, -0.1, -0.173};
float squarearr1[] = {0.1, -0.173, -0.1, 0.174};
float squarearr2[] = {-0.2, 0, 0.2, 0};




/** Interface to contro a standard DC motor 
 *
 * with an H-bridge using a PwmOut and 2 DigitalOuts
 */
class Motor {
	public:
		Motor(PinName pwm, PinName fwd, PinName rev);
      void speed(float speed);

	protected:
		PwmOut _pwm;
		DigitalOut _fwd;
		DigitalOut _rev;

};

Motor::Motor(PinName pwm, PinName fwd, PinName rev):
	_pwm(pwm), _fwd(fwd), _rev(rev) {
	
	_pwm.period(0.01);
	_pwm = 0.0;
	_fwd = 0;
	_rev = 0;
}

void Motor::speed(float speed) {
   _fwd = (speed > 0.0);
   _rev = (speed < 0.0);
   _pwm = abs(speed);
}

void serialInterrupt(){
    while(pc.readable()) {
        buf[serialCount] = pc.getc();
        serialCount++;
        if (serialCount >= SERIAL_BUFFER_SIZE) {
            memset(buf, 0, SERIAL_BUFFER_SIZE);
            serialCount = 0;
        }
        
    }
    if (buf[serialCount - 1] == '\n') {
        serialData = true;
        serialCount = 0;
    }
}
// main() runs in its own thread in the OS
int main() {
   Motor motor0(P2_3, P0_21, P0_20);
   Motor motor1(P2_2, P0_15, P0_16);
   Motor motor2(P2_1, P0_24, P0_25); 

   while (true) {
      for (int i=0; i<35; ++i) {
         motor0.speed(testarr0[i]);
         motor1.speed(testarr1[i]);
         motor2.speed(testarr2[i]);
         wait(0.1);
      }
      motor0.speed(0);
      motor1.speed(0);
      motor2.speed(0);
      wait(4);

      for (int i=0; i<3; ++i) {
         motor0.speed(trianglearr0[i]);
         motor1.speed(trianglearr1[i]);
         motor2.speed(trianglearr2[i]);
         wait(1);
      }
      motor0.speed(0);
      motor1.speed(0);
      motor2.speed(0);
      wait(4);

      for (int i=0; i<4; ++i) {
         motor0.speed(squarearr0[i]);
         motor1.speed(squarearr1[i]);
         motor2.speed(squarearr2[i]);
         wait(1);
      }
      motor0.speed(0);
      motor1.speed(0);
      motor2.speed(0);
      wait(4);
   }

   
   /* pc.attach(&serialInterrupt); */
	/* while (true) { */
   /*    if (serialData) { */
   /*       char temp[16]; */
   /*       memcpy(temp, buf, 16); */
   /*       memset(buf, 0, 16); */
   /*       serialData = false; */
   /*    } */
   /* } */
}

	/* PinName pwm = P2_3; */
	/* PinName dir1 = P0_21; */
	/* PinName dir2 = P0_20; */







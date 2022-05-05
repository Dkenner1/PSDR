
#include <LiquidCrystal_I2C.h>

// Base freq values are assumed to start at kilohertz to save on data size
const unsigned long mega = 1000;
const unsigned long giga = 1000000;
const unsigned long pico = 1000000000;
const float Vref = 5;
const float steps = 1023.0;
const float minV = 0.5;
const short scrnLen = 16;

LiquidCrystal_I2C lcd(0x27, scrnLen,2);  // set the LCD address to 0x27 for a 16 chars and 2 line display
double slope = 21.5;                     // Slope is in mV
double intercept = -86;
unsigned long freq;
double sampleArr[ARR_SIZE];
void setup(){
  // Init serial connection
  Serial.begin(9600);
  // Init LCD
  lcd.init();         
  lcd.backlight();
  freq = 1*giga;
  printFreqLCD(freq);
}

void loop(){
  for(int i=0; i<ARR_SIZE; i++){
    sampleArr[i] = readLogrithmicDetector(A3);
  }
  double dbm = avg(sampleArr);
  if(Serial.available() > 0){
    freq = getSerialNum();
    printFreqLCD(freq);
  }
  printPwrLCD(dbm);
  delay(1000);
}



unsigned long getSerialNum(){
  String s = Serial.readString();
  for(int i=0; i<s.length()-1; i++){
    if(!isDigit(s.charAt(i))){
      return 0;
    }
  }
  return s.toInt();
}

void clearLCDLine(int line){
  for(short i=0; i<scrnLen; i++){
    lcd.setCursor(i,line);
    lcd.print(" ");
  }
}

void printFreqLCD(unsigned long f){
    clearLCDLine(0);
    lcd.setCursor(0,0);
    lcd.print("Freq: " + freqToString(f));
}

void printPwrLCD(double dbm){
    clearLCDLine(1);
    lcd.setCursor(0,1);
    lcd.print("dbm:" + String(dbm, 1) + ",");
    lcd.setCursor(11,1);
    lcd.print(mWattToString(dbmToMilWatts(dbm)));
    Serial.println("dbm:" + String(dbm, 1) + "," + mWattToString(dbmToMilWatts(dbm)));
}

String freqToString(unsigned long f){
  String out;
  if(f < mega)
    return "Invalid";
  Serial.println("Freq is: " + String(f));
  Serial.println("Freq calc is: " +  String((double)f/giga, 3));
  if(f>=giga)
    out = String((double)f/giga, 3)+"GHz";
  else
    out = String((double)f/mega, 3)+"MHz";

  return out;
}

double readLogrithmicDetector(int pin){
  return (adc(pin)/slope) + intercept;
}

double dbmToMilWatts(double dbm){
  return pow(10, dbm/10);
}

String mWattToString(double mW){ 
  if(mW > 1)
    return String(mW, 0) + "mW";
  if(mW*mega > 1)
    return String(mW*mega, 0) + "uW";
  if(mW*giga > 1)
    return String(mW*giga, 0) + "nW";
  
  return String(mW*pico, 0) + "pW";  
}

double adc(int pin){ 
  //return ((Vref / steps) * 100) * 1000; 
  return  ((Vref / steps) * analogRead(pin))*1000; // Multiply by 1000 to keep units in mV
}

double avg(double arr[]){ 
  double sum = 0;
  for(int i=0; i<ARR_SIZE; i++){
    sum += arr[i];
  }
  return  sum/ARR_SIZE;
}


#include <string.h>
#include <wiringPi.h>

#define FLASHTIME 200   //in microseconds
#define NUMROWS 16
#define NUMCOLS 112


struct Display{
  uint8_t numRows = NUMROWS;
  uint8_t numCols = NUMCOLS;    // numCols = numBoards * numColsPerBoard
  uint8_t numBoards = 4;
  uint8_t numColsPerBoard = 28;
  uint16_t shown[NUMCOLS];    // datatype is uint16_t because numRows = 16 

  //object for rows
  struct Rows{
    uint8_t SER = 32;
    uint8_t OE = 33;
    uint8_t RCLK = 25;
    uint8_t SRCLK = 26;
    uint8_t SRCLR = 27;
    void disable() {
      digitalWrite(OE, HIGH); // disable
    }
    void enable(){
      digitalWrite(OE, LOW); // enable
    }
    void clear(){
      digitalWrite(SRCLR, LOW); // clear
      digitalWrite(SRCLR, HIGH); // clear
    }
    void incrementSR(){
      digitalWrite(SRCLK, HIGH);
      digitalWrite(SRCLK, LOW);
    }
    void incrementR(){
      digitalWrite(RCLK, HIGH);
      digitalWrite(RCLK, LOW);
    }
    void setIdle(){
      digitalWrite(SER, LOW);
    }
  } rows;

  //object for columns
  struct Columns{
    uint8_t SER = 23;
    uint8_t OE = 19;
    uint8_t RCLK = 18;
    uint8_t SRCLK = 17;
    uint8_t SRCLR = 16;
    void disable() {
      digitalWrite(OE, HIGH); // disable
    }
    void enable(){
      digitalWrite(OE, LOW); // enable
    }
    void clear(){
      digitalWrite(SRCLR, LOW); // clear
      digitalWrite(SRCLR, HIGH); // clear
    }
    void incrementSR(){
      digitalWrite(SRCLK, HIGH);
      digitalWrite(SRCLK, LOW);
    }
    void incrementR(){
      digitalWrite(RCLK, HIGH);
      digitalWrite(RCLK, LOW);
    }
    void setIdle(){
      digitalWrite(SER, LOW);
    }
  } cols;

  //toggle a specific column
  void toggleColumn(short c, bool state){
    cols.disable();
    cols.clear();
    c = c%numColsPerBoard;
    for(int8_t i = 3; i >=0; i--){
      short c_offset = i*8;
      for(int8_t j = 7; j >= 0; j--){ // writes +POS (83) (ON)
        if((j+c_offset == c) && state){
          digitalWrite(cols.SER, HIGH);
        }
        else{
          digitalWrite(cols.SER, LOW);
        }
        cols.incrementSR();
      }
      for(int8_t j = 7; j >= 0; j--){ // writes -GND (81) (OFF)
        if((j+c_offset == c) && !state){
          digitalWrite(cols.SER, HIGH);
        }
        else{
          digitalWrite(cols.SER, LOW);
        }
        cols.incrementSR();
      }
    }
    cols.incrementR();
    cols.setIdle();
  }

  //toggle a specific row
  void toggleRow(short r, short c, short state){
    rows.disable();
    rows.clear();
    int8_t board = c/numColsPerBoard;
    for(int8_t b = board; b>=0; b--){
      for(int8_t i = 1; i >=0; i--){
        short r_offset = i*8;
        for(int8_t j = 7; j >= 0; j--){ // writes +POS (83) (OFF)
          if((j+r_offset == r) && !state && (b == board)){
            digitalWrite(rows.SER, HIGH);
          }
          else{
            digitalWrite(rows.SER, LOW);
          }
          rows.incrementSR();
        }
        for(int8_t j = 7; j >= 0; j--){ // writes -GND (81) (ON)
          if((j+r_offset == r) && state && (b == board)){
            digitalWrite(rows.SER, HIGH);
          }
          else{
            digitalWrite(rows.SER, LOW);
          }
          rows.incrementSR();
        }
      }
    }
    rows.incrementR();
    rows.setIdle();
  }
  
  //turn on/off register outputs quickly
  void flash(uint8_t flashtime = FLASHTIME){    // turn on rows and colums for FLASHTIME microseconds 
    rows.enable();
    cols.enable();
    delayMicroseconds(flashtime);
    cols.disable();
    rows.disable();
  }

  //write a single dot to the display
  void writeDot(uint8_t c, uint8_t r, bool state){ // one dot at a time
    toggleRow(r, c, state);
    toggleColumn(c, state);
    flash();
    shown[c] = (shown[c] & (~(1 << r))) | (state << r);
  }
  
/*
  void writeByCol(uint16_t col, uint8_t x, uint8_t yS, uint8_t yF){ 
    for(uint8_t r = yS; r < min(numRows, yF); r++){ // do each row 
      bool newDot = ((col >> r-yS) & 1);
      if(newDot != ((shown[x] >> r) & 1)){
        writeDot(x, r, newDot);
      }
    }
  }
*/

  //write an array to the display
  void write(uint16_t * array, uint8_t colLimit = NUMCOLS, uint8_t rowLimit = NUMROWS, uint8_t x = 0, uint8_t y = 0, uint8_t delayTime = 1, bool byCol = true){ 
    if (byCol) {
      for(uint8_t c = x; c < numCols && c-x < colLimit; c++){ // For each column
        for(uint8_t r = y; r < numRows && r-y < rowLimit; r++){ // do each row 
          bool newDot = ((array[c-x] >> r-y) & 1);
          if(newDot != ((shown[c] >> r) & 1)){
            writeDot(c, r, newDot);
            delay(delayTime);
          }
        }
      }
    } else {
      for(uint8_t r = y; r < numRows && r-y < rowLimit; r++){ // For each Row
        for(uint8_t c = x; c < numCols && c-x < colLimit; c++){ // do each column
          bool newDot = ((array[c-x] >> r-y) & 1);
          if(newDot != ((shown[c] >> r) & 1)){
            writeDot(c, r, newDot);
            delay(delayTime);
          }
        }
      }
    }
  }
  
  //turn all dots off
  void allOff(bool full = true, uint16_t delayTime = 2, bool byCol = false){
    if(full){
      for(uint8_t j = 0; j<numRows; j++){
        for(uint8_t i = 0; i<numCols; i++){
          writeDot(i, j,0);
          delay(delayTime);
        } 
      }
    } else {
      uint16_t zeros[NUMCOLS] = {0};
      write(zeros, NUMCOLS, NUMROWS, 0, 0, delayTime, byCol);
    }
    for(uint8_t i = 0; i<numCols; i++){
      shown[i] = 0;
    }
  }

  //turn all dots on
  void allOn(bool full = true, uint16_t delayTime = 2, bool byCol = false){
    if(full){
      for(uint8_t j = 0; j<numRows; j++){
        for(uint8_t i = 0; i<numCols; i++){
          writeDot(i,j,1);
          delay(delayTime);
        } 
      }
    } else {
      uint16_t zeros[NUMCOLS] = {pow(2,NUMROWS)-1};
      write(zeros, NUMCOLS, NUMROWS, 0, 0, delayTime, byCol);
    }
    for(uint8_t i = 0; i<numCols; i++){
      shown[i] = 65535;
    }
  }

  //invert all dots
  void allInvert(uint16_t delayTime = 2){
    for(uint8_t j = 0; j<numRows; j++){
      for(uint8_t i = 0; i<numCols; i++){
        if(((shown[i] >> j) & 1)){
          writeDot(i,j,0);
        } else {
          writeDot(i,j,1);
        }
        delay(delayTime);
      } 
    }
    for(uint8_t i = 0; i<numCols; i++){
      shown[i] = 65535 - shown[i];
    }
  }

} display;


//output shown[] display to the serial terminal
void serialPrintDisplay(uint16_t * array = display.shown){
  for(uint8_t r = 0; r<16; r++){
    Serial.print('|');
    for(uint16_t c = 0; c<112; c++){
      if((array[c] >> r) & 1){
        Serial.print('#');
      } else {
        Serial.print(' ');
      }
    }
    Serial.println('|');
  }
}

//begin serial communication
void userSerialConnection(bool echo = false){
  while(true){
    String userInput = Serial.readStringUntil('\n');
    if (userInput.length() >= 4){
      if(userInput.charAt(0) == '{'){
        //{}
        uint16_t newDisplay[display.numCols] = {0};
        userInput = userInput.substring(userInput.indexOf('{')+1, userInput.indexOf('}'));
        char *ptr = strtok ((char *)userInput.c_str(), ",");         // get first token
        uint16_t loc = 0;
        while (ptr != NULL && loc < display.numCols){
          if(echo){Serial.printf("%s,",ptr);}
          newDisplay[loc++] = atoi(ptr);
          ptr = strtok(NULL, ",");
        }  
        if(echo){Serial.println();}
        display.write(newDisplay, loc);
      } else if(userInput.charAt(0) == '('){
        if(userInput.charAt(1)== '{'){
          uint16_t loc = 0;
          uint8_t params[5] = {0,0,0,0,1};
          String pString = userInput.substring(userInput.indexOf('}')+1, userInput.indexOf(')'));
          char *ptr = strtok ((char *)pString.c_str(), ",");
          //({}, colLimit, rowLimit, x, y, delay)
          while (ptr != NULL && loc < 5){
            if(echo){Serial.printf("%s,",ptr);}
            params[loc++] = atoi(ptr);
            ptr = strtok(NULL, ",");
          } 
          uint16_t aloc = 0;
          uint16_t newDisplay[params[0]] = {0};
          String aString = userInput.substring(userInput.indexOf('{')+1, userInput.indexOf('}'));
          ptr = strtok ((char *)aString.c_str(), ",");
          while (ptr != NULL && aloc < params[0]){
            if(echo){Serial.printf("%s,",ptr);}
            newDisplay[aloc++] = atoi(ptr);
            ptr = strtok(NULL, ",");
          } 
          if(echo){Serial.println();}
          if(loc >= 2 && loc <= 5){display.write(newDisplay, params[0], params[1], params[2], params[3], params[4]);} 
        } else {
          //(x, y, state)
          uint8_t dot[3] = {0};
          userInput = userInput.substring(userInput.indexOf('(')+1, userInput.indexOf(')'));
          char *ptr = strtok ((char *)userInput.c_str(), ",");         // get first token
          uint16_t loc = 0;
          while (ptr != NULL && loc < 3){
            if(echo){Serial.printf("%s,",ptr);}
            dot[loc++] = atoi(ptr);
            ptr = strtok(NULL, ",");
          } 
          if(echo){Serial.println();}
          if(loc == 3){display.writeDot(dot[0], dot[1], dot[2]);} 
        }
      } else if (userInput == "allOff" || userInput == "clear") {
        display.allOff();
      } else if (userInput == "allOn") {
        display.allOn();
      } else if (userInput == "invert" || userInput == "inverse") {
        display.allInvert();
      } else if (userInput == "print") {
        serialPrintDisplay();
      } else if (userInput == "exit") {
        break;  
      } 
      Serial.println("ready");
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(display.cols.SER, OUTPUT);
  pinMode(display.cols.OE, OUTPUT);
  pinMode(display.cols.RCLK, OUTPUT);
  pinMode(display.cols.SRCLK, OUTPUT);
  pinMode(display.cols.SRCLR, OUTPUT);
  display.cols.disable();
  display.cols.clear();
  pinMode(display.rows.SER, OUTPUT);
  pinMode(display.rows.OE, OUTPUT);
  pinMode(display.rows.RCLK, OUTPUT);
  pinMode(display.rows.SRCLK, OUTPUT);
  pinMode(display.rows.SRCLR, OUTPUT);
  display.rows.disable();
  display.rows.clear();
  display.allOff();
  Serial.println("ready");
}


void loop() {
  userSerialConnection();
}

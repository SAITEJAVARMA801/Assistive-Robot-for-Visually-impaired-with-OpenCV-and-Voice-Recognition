

#include <Arduino.h>

// L298N pins
#define ENA 5   // PWM for left motor
#define IN1 8
#define IN2 9

#define ENB 6   // PWM for right motor
#define IN3 10
#define IN4 11

const long BAUD = 115200;
String inputLine = "";

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopMotors();

  Serial.begin(BAUD);
  while (!Serial) {} // Wait for USB serial
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (inputLine.length() > 0) {
        processCommand(inputLine);
        inputLine = "";
      }
    } else {
      inputLine += c;
      if (inputLine.length() > 200) inputLine = ""; // prevent overflow
    }
  }
}

// --- Motor Control ---
void stopMotors() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void forward(int ms, int spd) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, spd);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, spd);

  delay(ms);
  stopMotors();
}

void backward(int ms, int spd) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, spd);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, spd);

  delay(ms);
  stopMotors();
}

void leftTurn(int ms, int spd) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, spd);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, spd);

  delay(ms);
  stopMotors();
}

void rightTurn(int ms, int spd) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, spd);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, spd);

  delay(ms);
  stopMotors();
}

// --- Command Parser (JSON-like) ---
void processCommand(String cmd) {
  cmd.trim();
  if (cmd.indexOf("\"cmd\"") == -1) return;

  int ms = getValue(cmd, "ms", 300);
  int spd = getValue(cmd, "spd", 200);

  if (cmd.indexOf("FWD") != -1) {
    forward(ms, spd);
  } else if (cmd.indexOf("BACK") != -1) {
    backward(ms, spd);
  } else if (cmd.indexOf("LEFT") != -1) {
    leftTurn(ms, spd);
  } else if (cmd.indexOf("RIGHT") != -1) {
    rightTurn(ms, spd);
  } else if (cmd.indexOf("STOP") != -1) {
    stopMotors();
  }
}

int getValue(String src, const char *key, int defaultVal) {
  String kq = String("\"") + key + "\"";
  int pos = src.indexOf(kq);
  if (pos == -1) return defaultVal;

  int colon = src.indexOf(':', pos);
  if (colon == -1) return defaultVal;

  int start = colon + 1;
  while (start < src.length() && (src[start] == ' ')) start++;
  int end = start;
  while (end < src.length() && isDigit(src[end])) end++;

  if (end > start) {
    return src.substring(start, end).toInt();
  }
  return defaultVal;
}

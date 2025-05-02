#define COMMON_ANODE true // Set to true for common anode RGB LEDs

const int redPin = 6;
const int greenPin = 5;
const int bluePin = 3;
const int spacer = 5;

void setup() {
  Serial.begin(9600);
  Serial.println("Enter R,G,B,Brightness (0-255)");
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n');
    inputString.trim(); // Remove whitespace

    // Flush any junk after newline (leftovers)
    while (Serial.available()) Serial.read();

    // Parse CSV values
    int comma1 = inputString.indexOf(',');
    int comma2 = inputString.indexOf(',', comma1 + 1);
    int comma3 = inputString.indexOf(',', comma2 + 1);

    if (comma1 > 0 && comma2 > comma1 && comma3 > comma2) {
      int red = inputString.substring(0, comma1).toInt();
      int green = inputString.substring(comma1 + 1, comma2).toInt();
      int blue = inputString.substring(comma2 + 1, comma3).toInt();
      int brightness = inputString.substring(comma3 + 1).toInt();

      // Validate values
      if (red <= 255 && green <= 255 && blue <= 255 && brightness <= 255 &&
          red >= 0 && green >= 0 && blue >= 0 && brightness >= 0) {

        Serial.print("Setting R="); Serial.print(red);
        Serial.print(", G="); Serial.print(green);
        Serial.print(", B="); Serial.print(blue);
        Serial.print(", Brightness="); Serial.println(brightness);

        int scaledRed = map(red, 0, 255, 0, brightness);
        int scaledGreen = map(green, 0, 255, 0, brightness);
        int scaledBlue = map(blue, 0, 255, 0, brightness);

        do {
          analogWrite(redPin, COMMON_ANODE ? 255 - scaledRed : scaledRed);
          analogWrite(greenPin, COMMON_ANODE ? 255 - scaledGreen : scaledGreen);
          analogWrite(bluePin, COMMON_ANODE ? 255 - scaledBlue : scaledBlue);
          delay(spacer);

          analogWrite(redPin, 0);
          analogWrite(greenPin, 0);
          analogWrite(bluePin, 0);
          delay(spacer);
        } while (Serial.available() == 0); // Wait for new input
      } else {
        Serial.println("❌ Values must be between 0 and 255.");
        flushSerial();
      }
    } else {
      Serial.println("❌ Invalid format. Use R,G,B,Brightness.");
      flushSerial();
    }
  }
}

void flushSerial() {
  while (Serial.available()) Serial.read(); // Dump any remaining junk
}

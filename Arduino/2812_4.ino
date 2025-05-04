#include <Adafruit_NeoPixel.h>

#define LED_PIN 6     // Data pin connected to the WS2812B matrix
#define LED_COUNT 64  // Number of LEDs in the matrix (8x8 = 64)

Adafruit_NeoPixel pixels(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

const int spacer = 4; // Changed to 500 for better visibility

// Global variables to store the desired color
uint8_t targetRed = 0;
uint8_t targetGreen = 0;
uint8_t targetBlue = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Enter R,G,B,Brightness (0-255) to set the entire matrix color.");
  pixels.begin();
  pixels.show();  // Initialize all pixels to off
}

void loop() {
  static bool blinking = false;
  static unsigned long lastBlinkTime = 0;

  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n');
    inputString.trim();
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

        Serial.print("Setting all LEDs to R=");
        Serial.print(red);
        Serial.print(", G=");
        Serial.print(green);
        Serial.print(", B=");
        Serial.print(blue);
        Serial.print(", Brightness=");
        Serial.println(brightness);

        targetRed = map(red, 0, 255, 0, brightness);
        targetGreen = map(green, 0, 255, 0, brightness);
        targetBlue = map(blue, 0, 255, 0, brightness);

        for (int i = 0; i < LED_COUNT; i++) {
          pixels.setPixelColor(i, pixels.Color(targetRed, targetGreen, targetBlue));
        }
        pixels.show();
        blinking = true;
        lastBlinkTime = millis();

      } else {
        Serial.println("❌ Values must be between 0 and 255.");
        flushSerial();
        blinking = false;
      }
    } else {
      Serial.println("❌ Invalid format. Use R,G,B,Brightness.");
      flushSerial();
      blinking = false;
    }
  }

  // Handle blinking if enabled
  if (blinking) {
    if (millis() - lastBlinkTime >= spacer) {
      for (int i = 0; i < LED_COUNT; i++) {
        if (pixels.getPixelColor(i) == 0) {
          pixels.setPixelColor(i, pixels.Color(targetRed, targetGreen, targetBlue)); // Use the stored target color
        } else {
          pixels.setPixelColor(i, pixels.Color(0, 0, 0));
        }
      }
      pixels.show();
      lastBlinkTime = millis();
    }
  }
}

void flushSerial() {
  while (Serial.available()) Serial.read();
}

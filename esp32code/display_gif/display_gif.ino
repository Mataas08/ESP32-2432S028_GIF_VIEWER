#include <TFT_eSPI.h>
#include "test.h"  // Contains: test[] PROGMEM, TEST_WIDTH, TEST_HEIGHT, TEST_FRAMES

TFT_eSPI tft = TFT_eSPI();  // Display driver

const float targetFPS = 7.0;                  // Desired frames per second
const uint32_t FRAME_DELAY = 1000.0 / targetFPS;  // Auto-calculated delay per frame [ms]

uint32_t lastFrameTime = 0;      // Last time a frame was drawn
uint16_t currentFrame = 0;       // Current frame index

/**
 * Draw a single frame from the RGB565 array stored in PROGMEM.
 */
void drawFrame(const uint16_t *bitmap, uint16_t frame, int16_t w, int16_t h) {
  uint32_t offset = (uint32_t)frame * w * h;

  tft.startWrite();
  for (int16_t y = 0; y < h; y++) {
    tft.setAddrWindow(0, y, w, 1);
    for (int16_t x = 0; x < w; x++) {
      uint32_t index = offset + y * w + x;
      uint16_t color = bitmap[index];
      tft.pushColor(color);
    }
  }
  tft.endWrite();
}

void setup() {
  tft.init();
  tft.setRotation(1);
  tft.invertDisplay(true);
  tft.fillScreen(TFT_BLACK);

  drawFrame(test, currentFrame, TEST_WIDTH, TEST_HEIGHT);
  lastFrameTime = millis();  // Initialize timing
}

void loop() {
  uint32_t now = millis();

  // If it's time for the next frame
  if (now - lastFrameTime >= FRAME_DELAY) {
    currentFrame = (currentFrame + 1) % TEST_FRAMES;
    drawFrame(test, currentFrame, TEST_WIDTH, TEST_HEIGHT);
    lastFrameTime = now;
  }
}

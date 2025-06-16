# ESP32 Retro Display – Animated GIF to TFT

This project converts animated GIFs into RGB565 frame arrays and displays them as smooth animations on a 320x240 TFT display using an ESP32 and the TFT_eSPI library.

---

## 📈 Features

- Convert any `.gif` animation to RGB565 format
- Display animation at a fixed frame rate (e.g. 7 FPS)
- Uses `millis()` for non-blocking playback
- Fully compatible with PROGMEM and ESP32

---

## 🛠️ Hardware Requirements

- ESP32 development board (e.g. ESP32 DevKit v1)
- 320x240 TFT display (ILI9341, ST7789, or compatible)
- USB cable and Arduino IDE
- Jumper wires or breadboard for connections

---

## 📂 Project Structure

```
.
├── convert_gif.py        # Python script for GIF to .h conversion
├── test.gif              # Example animated GIF
├── test.h                # Generated header file (RGB565 data)
├── display_gif.ino       # Arduino sketch to play the animation
├── temp/                 # Temporary folder for PNG frames
├── LICENSE               # MIT License file
└── README.md             # This documentation
```

---

## 📚 How It Works

1. A Python script processes a GIF and outputs a single `.h` file
2. The header contains all frames as a flattened array in RGB565 format
3. The Arduino sketch loads the header and displays the frames on a TFT display using `millis()`-based timing

---

## 🚀 Quick Start

### 1. Python Side

#### Requirements:
```bash
pip install pillow numpy
```

#### Run the converter:
```bash
python convert_gif.py
```

Example use in code:
```python
convert_gif_to_header("my_animation.gif", "mygif.h", "mygif")
```

### 2. Arduino Side

#### Install Libraries:
- [TFT_eSPI](https://github.com/Bodmer/TFT_eSPI)

> Be sure to configure `User_Setup.h` for your display controller and pins.

#### Upload the Sketch:
- Open `display_gif.ino` in Arduino IDE
- Include the generated `mygif.h` file
- Upload to your ESP32 board

#### Change frame rate:
Edit the line:
```cpp
const float targetFPS = 7.0;
```
To control playback speed.

---

## 📅 Header Format

The converter generates a file like:
```c
#define MYGIF_WIDTH 320
#define MYGIF_HEIGHT 240
#define MYGIF_FRAMES 7

const uint16_t mygif[] PROGMEM = {
  // Frame 0 RGB565 values
  // Frame 1 RGB565 values
  // ...
};
```

Each frame is appended after the previous one, allowing fast indexed access on ESP32.

---

## 🚧 Future Plans

- Play real frame durations from GIF metadata
- Add button support (pause, next, previous)
- Load animation from SD card or SPIFFS
- Optimize for PSRAM / memory-constrained boards

---

## 🔒 License (MIT)

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

> You are free to use this in commercial and private projects.

---

## 😊 Author

Made with ❤️ by [Your Name]

Feel free to fork, modify, and contribute!


# the L.E.D project

1. this repo will contain massive amounts of sketch files
2. this repo's aim is to create a fun project using the TFT LCD screen
3. that's it

## contents:
- buttons.py library facilitating creation of interactable buttons
- button_calc.py program is a simple sum-only calculator which displays it's value either with the esp32 pin2 diode or in the console of the device pushing the code to esp32
- to_raw.py convert photos to .raw whych is readable by the screen. To use type in the terminal
  -     python3 to_raw.py <filename> <height> <width> 
  -     ex. python3 to_raw.py cute_cat.jpg 128 128 
- display_button is a sketch

I have just realized that this project's name should be L.C.D not L.E.D as the source of the name is from the screen type I'm playing with. Whatever.


## screen connections chart for ESP wroom-32:

|screen pin|ESP32 port|
|:-----------|-----:|
|VCC|3.3V|
|GND|GND|
|CS|GPIO 5|
|RESET|GPIO 22|
|DC|GPIO 21|
|SDI(MOSI)|GPIO 23|
|SCK|GPIO 18|
|LED|3.3V|
|SDO (MISO)|-|
|T_CLK|GPIO 25|
|T_CS|GPIO 26|
|T_DIN|GPIO 27|
|T_DO|GPIO 4|
|T_IRQ|GPIOx 34|

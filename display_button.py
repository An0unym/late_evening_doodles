from machine import Pin, SPI, idle
from ili9341 import Display, color565
from xpt2046 import Touch

BTN = (60, 120, 120, 50)
WHITE = color565(255, 255, 255)
RED = color565(255, 0, 0)
GREEN = color565(0,255,15)
state = False

# Display on its own bus (fast)
spi1 = SPI(2, baudrate=40000000, sck=Pin(18), mosi=Pin(23))
display = Display(spi1, dc=Pin(21), cs=Pin(5), rst=Pin(22))

# Touch on a separate bus (slow)
spi2 = SPI(1, baudrate=1000000, sck=Pin(25), mosi=Pin(26), miso=Pin(27))

def draw_button():
    color = GREEN if state else RED
    display.fill_rectangle(*BTN, color)
    display.draw_text8x8(BTN[0] + 20, BTN[1] + 21, "ON" if state else "OFF", RED if state else GREEN, background=color)

def on_touch(x, y):
    global state
    y = (display.height - 1) - y
    bx, by, bw, bh = BTN
    if bx <= x < bx + bw and by <= y < by + bh:
        state = not state
        draw_button()

touch = Touch(spi2, cs=Pin(4), int_pin=Pin(34), int_handler=on_touch)

try:
    while True:
        idle()
except KeyboardInterrupt:
    display.cleanup()
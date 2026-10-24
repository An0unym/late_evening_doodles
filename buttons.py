"""buttons.py - touch buttons for an ILI9341 display + XPT2046 touch (MicroPython).

Usage:
    import buttons
    buttons.init(display, touch_spi, Pin(4), Pin(34))
    buttons.create_button((60, 120), (120, 50), (255, 0, 0), "Hello", (255, 255, 255),
                          on_press=my_function)
    buttons.run()

Needs ili9341.py and xpt2046.py in /lib on the board.
"""
import time
from machine import idle
from ili9341 import color565
from xpt2046 import Touch

_display = None
_touch = None
_buttons = []
_pending = None          # last raw touch (x, y) waiting to be processed
_last_accept = 0         # time of the last accepted press
_debounce_ms = 300


def _to565(colour):
    """Accept (r, g, b) with values 0-255, or an int already made by color565()."""
    if isinstance(colour, (tuple, list)):
        return color565(colour[0], colour[1], colour[2])
    return colour


def _on_touch(x, y):
    # Runs inside the touch interrupt, so it only stores the position.
    # The real work happens later in update(), which is safer.
    global _pending
    _pending = (x, y)


class Button:
    def __init__(self, position, size, colour, text, text_colour, on_press):
        self.x, self.y = position
        self.w, self.h = size
        self.colour = _to565(colour)
        self.text = text
        self.text_colour = _to565(text_colour)
        self.on_press = on_press

    def draw(self):
        """Draw (or redraw) the button with its text centred."""
        _display.fill_rectangle(self.x, self.y, self.w, self.h, self.colour)
        text_x = self.x + (self.w - 8 * len(self.text)) // 2
        text_x = max(self.x, text_x)                    # long text starts at the left edge
        text_y = self.y + (self.h - 8) // 2
        _display.draw_text8x8(text_x, text_y, self.text,
                              self.text_colour, background=self.colour)

    def contains(self, px, py):
        """True if the point (px, py) is inside this button."""
        return self.x <= px < self.x + self.w and self.y <= py < self.y + self.h

    def set_text(self, text):
        self.text = text
        self.draw()

    def set_colour(self, colour):
        self.colour = _to565(colour)
        self.draw()


def init(display, touch_spi, touch_cs, touch_int, debounce_ms=300):
    """Set up touch handling. Call once, before creating buttons.

    display:    your ili9341 Display object
    touch_spi:  the SPI bus the touch chip is on
    touch_cs:   Pin object for T_CS
    touch_int:  Pin object for T_IRQ
    """
    global _display, _touch, _debounce_ms, _last_accept
    _display = display
    _debounce_ms = debounce_ms
    _last_accept = time.ticks_add(time.ticks_ms(), -debounce_ms)
    _touch = Touch(touch_spi, cs=touch_cs, int_pin=touch_int, int_handler=_on_touch)


def create_button(position, size, colour, text, text_colour, on_press=None):
    """Create, draw and register a button. Returns the Button object.

    position:    (x, y) of the top-left corner
    size:        (width, height) in pixels
    colour:      (r, g, b) or color565 value
    text:        label (8x8 font, so 8 pixels per character)
    text_colour: (r, g, b) or color565 value
    on_press:    optional function called as on_press(button) when pressed
    """
    if _display is None:
        raise RuntimeError("call buttons.init() before create_button()")
    button = Button(position, size, colour, text, text_colour, on_press)
    _buttons.append(button)
    button.draw()
    return button


def clear_buttons():
    """Forget all buttons (use when switching to another screen)."""
    del _buttons[:]


def update():
    """Process a pending touch. Call this often if you run your own loop."""
    global _pending, _last_accept
    if _pending is None:
        return
    x, y = _pending
    _pending = None

    now = time.ticks_ms()
    if time.ticks_diff(now, _last_accept) < _debounce_ms:
        return

    y = (_display.height - 1) - y              # touch Y runs the opposite way
    for button in reversed(_buttons):          # newest button wins if they overlap
        if button.contains(x, y):
            _last_accept = now
            if button.on_press:
                button.on_press(button)
            break


def run():
    """Blocking main loop. Press Ctrl+C to stop."""
    try:
        while True:
            update()
            idle()
    except KeyboardInterrupt:
        _display.cleanup()

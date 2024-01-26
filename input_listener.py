from typing import Optional, Tuple

from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener


class InputListener:
    def __init__(self):
        self._last_key_pressed = None
        self._last_mouse_button_pressed = None
        self._last_mouse_position = None
        self._keyboard_listener = None
        self._mouse_listener = None

    def start(self):
        self._keyboard_listener = KeyboardListener(
            on_press=self.on_press, on_release=self.on_release
        )
        self._mouse_listener = MouseListener(on_click=self.on_click)

        self._keyboard_listener.start()
        self._mouse_listener.start()

        self._keyboard_listener.join()
        self._mouse_listener.join()

    def stop(self):
        if self._keyboard_listener:
            self._keyboard_listener.stop()
        if self._mouse_listener:
            self._mouse_listener.stop()

    @property
    def last_key_pressed(self) -> Optional[str]:
        return self._last_key_pressed

    @property
    def last_mouse_button_pressed(self) -> Optional[str]:
        return self._last_mouse_button_pressed

    @property
    def last_mouse_position(self) -> Optional[Tuple[int, int]]:
        return self._last_mouse_position

    def on_press(self, key):
        if key is not Key.pause:
            self._last_key_pressed = key

    def on_release(self, key):
        if key == Key.pause:
            self.stop()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self._last_mouse_button_pressed = button
            self._last_mouse_position = (x, y)

from __future__ import annotations

import time
from typing import Optional

from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Button

from input_listener import InputListener


class ListenerX1Button(InputListener):
    def __init__(self, observer: Optional[MacroObserver] = None):
        super().__init__()
        self._observer = observer

    def on_click(self, x, y, button, pressed):
        super().on_click(x, y, button, pressed)
        if pressed and button == Button.x1:
            if self._observer:
                self._observer.handle_x1_button_click()


class MacroObserver:
    def __init__(self) -> None:
        self.macro_active = False
        self.keyboard = KeyboardController()
        self.listener = ListenerX1Button(self)

    def handle_x1_button_click(self):
        if not self.macro_active:
            self.activate_macro()
        else:
            self.deactivate_macro()

    def check_macro_trigger(self):
        last_mouse_button_pressed = self.listener.last_mouse_button_pressed
        if last_mouse_button_pressed == Button.x1:
            if not self.macro_active:
                self.activate_macro()
            else:
                self.deactivate_macro()

    def activate_macro(self):
        self.keyboard.press("f")
        self.macro_active = True
        print("Macro ativado")

    def deactivate_macro(self):
        self.keyboard.release("f")
        self.macro_active = False
        print("Macro desativado")


class InterfaceMacro:
    def __init__(self) -> None:
        self.observador = MacroObserver()

    def run(self):
        self.observador.listener.start()
        try:
            while True:
                self.observador.check_macro_trigger()
                time.sleep(0.5)
        except KeyboardInterrupt:
            self.observador.listener.stop()


if __name__ == "__main__":
    interface = InterfaceMacro()
    interface.run()

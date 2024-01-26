from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button
from pynput.mouse import Listener as MouseListener
from PySide6.QtWidgets import QApplication, QMainWindow
from window_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.macro_active = False
        self.mouse_listener = None
        self.keyboard_listener = None
        self.keyboard = KeyboardController()
        
        self.bind_key = Key.pause
        self.bind_button = Button.x1

        self.pushButton.clicked.connect(self.toggle)

        self.start_listener()

    def start_listener(self):
        self.mouse_listener = MouseListener(on_click=self.on_click)
        self.keyboard_listener = KeyboardListener(
            on_press=self.on_press, on_release=self.on_release
        )
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_listener(self):
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == self.bind_button:
                print("Botão do macro ativado")
                if not self.macro_active:
                    self.activate_macro()
                    self.activeLabel.setText("Ativado")
                else:
                    self.deactivate_macro()
                    self.activeLabel.setText("Desativado")

    def on_press(self, key):
        ...

    def on_release(self, key):
        if key == Key.scroll_lock:
            exit(0)

    def toggle(self):
        if self.activeLabel.text() == "Desativado":
            self.activeLabel.setText("Ativado")
            self.activate_macro()
            self.macro_active = True
        else:
            self.activeLabel.setText("Desativado")
            self.deactivate_macro()
            self.macro_active = False

    def activate_macro(self):
        self.keyboard.press("f")
        self.macro_active = True
        print("Macro ativado")

    def deactivate_macro(self):
        self.keyboard.release("f")
        self.macro_active = False
        print("Macro desativado")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec()

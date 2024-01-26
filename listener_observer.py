from abc import ABC, abstractmethod
from pynput.keyboard import Key, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from typing import Optional


class Subject(ABC):
    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass


class Observer(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass


class InputSubject(Subject):
    def __init__(self):
        self._observers = set()

    def attach(self, observer):
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, event):
        for observer in self._observers:
            observer.update(event)


class InputObserver(Observer):
    def update(self, event):
        print(event)


class InputListener:
    def __init__(self, subject: Optional[InputSubject] = None):
        self._subject = subject
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
        exit(0)

    def on_press(self, key):
        print(f"Tecla pressionada: {key}")
        # self._subject.notify(f"Tecla pressionada: {key}")

    def on_release(self, key):
        # self._subject.notify(f"Tecla solta: {key}")
        if key == Key.esc:
            self.stop()

    def on_click(self, x, y, button, pressed):
        if self._subject:
            if pressed:
                self._subject.notify(f"Botão {button} do mouse pressionado em ({x}, {y})")
            else:
                self._subject.notify(f"Botão {button} do mouse solto em ({x}, {y})")
        else:
            if pressed:
                print(f"Botão {button} do mouse pressionado em ({x}, {y})")
            else:
                print(f"Botão {button} do mouse solto em ({x}, {y})")


class InputListenerInterface:
    def __init__(self) -> None:
        self.subject = None
        self.observer = None
        self.listener = None

    def run(self):
        self.subject = InputSubject()
        self.observer = InputObserver()

        self.subject.attach(self.observer)

        self.listener = InputListener(self.subject)
        self.listener.start()


if __name__ == "__main__":
    input_listener = InputListenerInterface()
    input_listener.run()

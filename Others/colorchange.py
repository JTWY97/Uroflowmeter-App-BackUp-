import kivy
kivy.require('1.8.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty

class TestApp(App):
    value = NumericProperty(0)

    def build(self):
        return Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    Label:
        text: str(app.value)
        canvas.before:
            Color:
                rgba: app.value / 64., (64 - app.value) / 64., 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
    BoxLayout:
        Button:
            text: '-'
            on_press: app.minus()
            on_release: app.stopupdate()
        Button:
            text: '+'
            on_press: app.plus()
            on_release: app.stopupdate()
''')

    def plus(self):
        self.event = Clock.schedule_interval(lambda dt: setattr(self, 'value', self.value + 1), 0.1)
        self.value += 1

    def minus(self):
        self.event = Clock.schedule_interval(lambda dt: setattr(self, 'value', self.value - 1), 0.1)
        self.value -= 1

    def stopupdate(self):
        self.event.cancel()

if __name__ == '__main__':
    TestApp().run()
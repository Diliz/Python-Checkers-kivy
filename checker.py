import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class MyApp(App):

    grid = [['X', '', 'X', '', 'X', '', 'X', ''],
            ['', 'X', '', 'X', '', 'X', '', 'X'],
            ['X', '', 'X', '', 'X', '', 'X', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', 'O', '', 'O', '', 'O', '', 'O'],
            ['O', '', 'O', '', 'O', '', 'O', ''],
            ['', 'O', '', 'O', '', 'O', '', 'O']]
    layout = GridLayout(cols=8, rows=8)
    def build(self):
        color = 0
        counter = 0
        for row in self.grid:
            counter += 1
            for pawn in row:
                if counter % 2 != 0:
                    color = (0.0, 0.0, 0.0, 0.0)
                else:
                    color = (2.0, 2.0, 2.0, 1.0)
                self.layout.add_widget(Button(text=pawn, background_color=color))
                counter += 1
        return self.layout

    def updateGrid(self):
        return self.layout


if __name__ == '__main__':
    MyApp().run()

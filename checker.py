import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class MyApp(App):

    grid = [['', 'b', '', 'b', '', 'b', '', 'b', '', 'b'],
            ['b', '', 'b', '', 'b', '', 'b', '', 'b', ''],
            ['', 'b', '', 'b', '', 'b', '', 'b', '', 'b'],
            ['b', '', 'b', '', 'b', '', 'b', '', 'b', ''],
            ['', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', '', ''],
            ['', 'w', '', 'w', '', 'w', '', 'w', '', 'w'],
            ['w', '', 'w', '', 'w', '', 'w', '', 'w', ''],
            ['', 'w', '', 'w', '', 'w', '', 'w', '', 'w'],
            ['w', '', 'w', '', 'w', '', 'w', '', 'w', '']]
    layout = GridLayout(cols=10, rows=10)
    clicked = False
    def build(self):
        color = 0
        counter = 0
        for rowIndex, row in enumerate(self.grid):
            counter += 1
            for columnIndex, pawn in enumerate(row):
                if counter % 2 != 0:
                    color = (0.0, 0.0, 0.0, 0.0)
                else:
                    color = (3.0, 3.0, 3.0, 1.0)
                text = str(columnIndex) + '-' + str(rowIndex)
                self.layout.add_widget(Button(text=text, background_color=color, on_press=self.movePawn))
                counter += 1
        return self.layout

    def movePawn(self, button):
        self.clicked = not self.clicked
        if self.clicked == True:
            print('test')
        return self.layout


if __name__ == '__main__':
    MyApp().run()

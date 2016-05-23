import kivy
import copy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class Checker(App):
    victory = False
    multiple = False
    prevPawn = ''
    turn = 'w'
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
    playerScores = [20, 20]

    def build(self):
        onePawn = Pawn()
        color = 0
        counter = 0
        for rowIndex, row in enumerate(self.grid):
            counter += 1
            for columnIndex, pawn in enumerate(row):
                if counter % 2 == 0:
                    color = (0.75, 0.58, 0.36, 2.5)
                else:
                    color = (0.84, 0.70, 0.49, 2.5)
                placement = str(rowIndex) + str(columnIndex)
                newPawn = copy.deepcopy(onePawn)
                newPawn.color = pawn
                newPawn.button = Button(id=placement, background_color=color, on_press=self.movePawn, text=pawn)
                newPawn.row = rowIndex
                newPawn.column = columnIndex
                self.grid[rowIndex][columnIndex] = newPawn
                self.layout.add_widget(self.grid[rowIndex][columnIndex].button)
                counter += 1
        return self.layout

    def movePawn(self, button):
        row = int(button.id[0])
        column = int(button.id[1])
        pawn = self.grid[row][column]
        if self.victory != True:
            if self.clicked == True or self.multiple == True:
                if row == self.prevPawn.row and column == self.prevPawn.column:
                    if self.multiple:
                        self.multiple = False
                        self.changeTurn()
                    self.reinitPrev()
                    self.clicked = False
                else:
                    if pawn.color == '':
                        self.checkAndPlace(row, column)
            else:
                if pawn.color == self.turn or pawn.color == self.turn + 'd':
                    self.prevPawn = pawn
                    self.clicked = True
        return False

    def checkAndPlace(self, row, column):
        columnDiff = column - self.prevPawn.column;
        rowDiff = row - self.prevPawn.row;
        if self.prevPawn.color == self.turn:
            if rowDiff == 2 or rowDiff == -2:
                if columnDiff == - 2 or columnDiff == 2:
                    if self.turn == 'w':
                        if self.grid[int(row - (rowDiff / 2))][int(column - (columnDiff / 2))].color == 'b':
                            self.reinitPawn(self.grid[int(row - (rowDiff / 2))][int(column - (columnDiff / 2))])
                            self.playerScores[1] -= 1
                            if self.playerScores[1] <= 0:
                                self.victory = True
                                print('Le joueur Blanc Gagne!')
                        else:
                            return False
                    else:
                        if self.grid[int(row - (rowDiff / 2))][int(column - (columnDiff / 2))].color == 'w':
                            self.reinitPawn(self.grid[int(row - (rowDiff / 2))][int(column - (columnDiff / 2))])
                            self.playerScores[0] -= 1
                            if self.playerScores[0] <= 0:
                                self.victory = True
                                print('Le joueur Noir Gagne!')
                        else:
                            return False
                    self.grid[row][column].button.text, self.prevPawn.button.text = self.prevPawn.button.text, self.grid[row][column].button.text
                    self.grid[row][column].color, self.prevPawn.color = self.prevPawn.color,  self.grid[row][column].color
                    self.multiple = self.checkForMultiple(self.grid[row][column])
                    if not self.multiple:
                        self.changeTurn()
                        self.clicked = False
                    else:
                        self.prevPawn = self.grid[row][column]
                else:
                    return False
            elif rowDiff == 1 or rowDiff == -1:
                if columnDiff == -1 or columnDiff == 1:
                    if (rowDiff == -1 and self.turn == 'w') or (rowDiff == 1 and self.turn == 'b'):
                        self.grid[row][column].button.text, self.prevPawn.button.text = self.prevPawn.button.text, self.grid[row][column].button.text
                        self.grid[row][column].color, self.prevPawn.color = self.prevPawn.color, self.grid[row][column].color
                        self.changeTurn()
                        self.clicked = False
                    else:
                        print('Mouvement arrière interdit')
                        return False
                else:
                    return False
            elif self.prevPawn.queen == True:
                return False
            else:
                return False
            return False
        return False

    def checkForMultiple(self, pawn):
        if pawn.row + 1 < 9:
            if pawn.column + 1 < 9:
                if self.grid[pawn.row + 1][pawn.column + 1].color != self.turn and self.grid[pawn.row + 1][pawn.column + 1].color != '':
                    if self.grid[pawn.row + 2][pawn.column + 2].color == '':
                        return True
            if pawn.column - 1 > 0:
                if self.grid[pawn.row + 1][pawn.column - 1].color != self.turn and self.grid[pawn.row + 1][pawn.column - 1].color != '':
                    if self.grid[pawn.row + 2][pawn.column - 2].color == '':
                        return True
        if pawn.row - 1 > 0:
            if pawn.column + 1 < 9:
                if self.grid[pawn.row - 1][pawn.column + 1].color != self.turn and self.grid[pawn.row - 1][pawn.column + 1].color != '':
                    if self.grid[pawn.row - 2][pawn.column + 2].color == '':
                        return True
            if pawn.column - 1 > 0:
                if self.grid[pawn.row - 1][pawn.column - 1].color != self.turn and self.grid[pawn.row - 1][pawn.column - 1].color != '':
                    if self.grid[pawn.row - 2][pawn.column - 2].color == '':
                        return True
        return False

    def reinitPawn(self, pawn):
        pawn.color = ''
        pawn.button.text = ''

    def reinitPrev(self):
        self.prevPawn = 0

    def changeTurn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
        return False

class Pawn(object):
    color = ''
    button = 0
    row = 0
    column = 0
    queen = False

    def __init__(self):
        return

if __name__ == '__main__':
    Checker().run()

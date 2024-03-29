import kivy
import copy

from math import sqrt
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class Checker(App):
    dynamicValue = 10
    players = {}
    victory = False
    multiple = False
    prevPawn = ''
    prevColor = ''
    pawnEated = False
    turn = 'w'
    grid = []
    layout = ''
    clicked = False

    def build(self):
        self.dynamicValue = 6
        gridValue = self.dynamicValue * self.dynamicValue
        diviser = int(sqrt(gridValue))
        self.layout = GridLayout(cols=self.dynamicValue, rows=self.dynamicValue)
        nbPawns = int((self.dynamicValue / 2) * ((self.dynamicValue / 2) -1))
        self.players['b'] = Player('Noir', 'w', nbPawns, 1)
        self.players['w'] = Player('Blanc', 'b', nbPawns, -1)
        color = 0
        counter = 0
        jumpLine = 0
        for i in range(0, gridValue):
            if jumpLine != int(i / diviser):
                jumpLine += 1
                counter += 1
            try:
                value = self.grid[int(i / (diviser * (i % diviser)))]
            except Exception as e:
                self.grid.append([])
            buttonId = str(int(i / diviser)) + '-' + str(int(i % diviser))
            pawn = ''
            if counter % 2 != 0:
                color = (0.75, 0.58, 0.36, 2.5)
                if i < int(nbPawns * 2):
                    pawn = 'b'
                if i >= int(gridValue - (nbPawns * 2)):
                    pawn = 'w'
            else:
                color = (0.84, 0.70, 0.49, 2.5)
            y = int(i / diviser)
            x = int(i % diviser)
            self.grid[y].append([])
            self.grid[y][x].append('')
            self.grid[y][x] = Pawn(pawn, Button(id = buttonId, background_color=color, on_press=self.movePawn, text=pawn, font_size=int(200 / self.dynamicValue)), y, x, False)
            self.layout.add_widget(self.grid[y][x].button)
            counter += 1
        return self.layout

    def movePawn(self, button):
        matching = button.id.split('-')
        row = int(matching[0])
        column = int(matching[1])
        pawn = self.grid[row][column]
        if self.clicked == True:
            if row == self.prevPawn.row and column == self.prevPawn.column and self.pawnEated == False:
                self.reinitPrev()
                self.clicked = False
                print('Mouvement annulé')
            elif row != self.prevPawn.row and column != self.prevPawn.column:
                if pawn.color == '':
                    self.place(row, column)
            else:
                print('Mouvement Interdit')
                return False
        else:
            if pawn.color == self.turn:
                self.prevPawn = pawn
                self.prevColor = pawn.button.background_color
                pawn.button.background_color = (0, 0.7, 0, 2)
                self.clicked = True
        return False

    def place(self, row, column):
        if self.prevPawn.color == self.turn:
            self.check(row, column)
            return False
        return False

    def check(self, row, column):
        if self.checkMovable(row, column) == True:
            if self.pawnEated == False:
                self.changeTurn()
        return False

    def checkMovable(self, row, column):
        if self.grid[row][column].color == '':
            if abs(row - self.prevPawn.row) == 2 and abs(column - self.prevPawn.column) == 2:
                if self.grid[int(row - ((row - self.prevPawn.row) / 2))][int(column - ((column - self.prevPawn.column) / 2))].color == self.players[self.turn].ennemy:
                    self.grid[int(row - ((row - self.prevPawn.row) / 2))][int(column - ((column - self.prevPawn.column) / 2))].color = ''
                    self.grid[int(row - ((row - self.prevPawn.row) / 2))][int(column - ((column - self.prevPawn.column) / 2))].button.text = ''
                    self.updateScore(self.players[self.turn].ennemy)
                    self.pawnEated = True
                    return self.swapPawnValues(row, column)
            else:
                if row - self.prevPawn.row == self.players[self.turn].orientation and abs(column - self.prevPawn.column) == 1:
                    return self.swapPawnValues(row, column)
        return False

    def checkForEatable(self, row, column):
        if (row + 1) < self.dynamicValue and (column + 1) < self.dynamicValue and  self.grid[row + 1][column + 1].color == self.players[self.turn].ennemy:
            if (row + 2) < self.dynamicValue and (column + 2) < self.dynamicValue and self.grid[row + 2][column + 2].color == '':
                return True
        if (row - 1) >= 0 and (column + 1) < self.dynamicValue and self.grid[row - 1][column + 1].color == self.players[self.turn].ennemy:
            if (row - 2) >= 0 and (column + 2) < self.dynamicValue and self.grid[row - 2][column + 2].color == '':
                return True
        if (row + 1) < self.dynamicValue and (column - 1) >= 0 and self.grid[row + 1][column - 1].color == self.players[self.turn].ennemy:
            if (row + 2) < self.dynamicValue and (column - 2) >= 0 and self.grid[row + 2][column - 2].color == '':
                return True
        if (row - 1) >= 0 and (column - 1) >= 0 and self.grid[row - 1][column - 1].color == self.players[self.turn].ennemy:
            if (row - 2) >= 0 and (column - 2) >= 0 and self.grid[row - 2][column - 2].color == '':
                return True
        return False

    def swapPawnValues(self, row, column):
        self.grid[row][column].button.text, self.prevPawn.button.text = self.prevPawn.button.text, self.grid[row][column].button.text
        self.grid[row][column].color, self.prevPawn.color = self.prevPawn.color, self.grid[row][column].color
        if self.pawnEated and self.checkForEatable(row, column):
            self.grid[row][column].button.background_color = (0, 0.7, 0, 2)
            self.grid[self.prevPawn.row][self.prevPawn.column].button.background_color = self.prevColor
            self.prevPawn = self.grid[row][column]
            return True
        self.pawnEated = False
        self.reinitPrev()
        return True

    def reinitPawn(self, pawn):
        pawn.color = ''
        pawn.button.text = ''

    def reinitPrev(self):
        self.grid[self.prevPawn.row][self.prevPawn.column].button.background_color = self.prevColor
        self.prevPawn = 0

    def updateScore(self, color):
        self.players[color].score -= 1
        print('Scores:')
        print(self.players[self.turn].name + ' : ' + str(self.players[self.turn].score))
        print(self.players[color].name + ' : ' + str(self.players[color].score))
        if self.players[color].score <= 0:
            print('Victoire des ' + self.players[self.turn].name + 's!')

    def changeTurn(self):
        print('Fin du tour des ' + self.players[self.turn].name + 's.')
        self.turn = self.players[self.turn].ennemy
        self.clicked = False
        return False

class Pawn(object):
    color = ''
    button = 0
    row = 0
    column = 0
    queen = False

    def __init__(self, color, button, row, column, queen):
        self.color = color
        self.button = button
        self.row = row
        self.column = column
        self.queen = queen
        return

class Player(object):
    name = ''
    ennemy = ''
    score = 0
    orientation = 0

    def __init__(self, name, ennemy, score, orientation):
        self.name = name
        self.ennemy = ennemy
        self.score = score
        self.orientation = orientation
        return

if __name__ == '__main__':
    Checker().run()

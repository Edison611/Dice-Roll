from tkinter import *
import random

class GUIDie(Canvas):
    '''6-sided Die class for GUI'''

    def __init__(self,master,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIDie(master,[valueList,colorList]) -> GUIDie
        creates a GUI 6-sided die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        # create a 60x60 white canvas with a 5-pixel grooved border
        Canvas.__init__(self,master,width=60,height=60,bg='white',\
                        bd=5,relief=GROOVE)
        # store the valuelist and colorlist
        self.valueList = valueList
        self.colorList = colorList
        # initialize the top value
        self.top = 1

    def get_top(self):
        '''GUIDie.get_top() -> int
        returns the value on the die'''
        return self.valueList[self.top-1]

    def roll(self):
        '''GUIDie.roll()
        rolls the die'''
        self.top = random.randrange(1,7)
        self.draw()

    def draw(self):
        '''GUIDie.draw()
        draws the pips on the die'''
        # clear old pips first
        self.erase()
        # location of which pips should be drawn
        pipList = [[(1,1)],
                   [(0,0),(2,2)],
                   [(0,0),(1,1),(2,2)],
                   [(0,0),(0,2),(2,0),(2,2)],
                   [(0,0),(0,2),(1,1),(2,0),(2,2)],
                   [(0,0),(0,2),(1,0),(1,2),(2,0),(2,2)]]
        for location in pipList[self.top-1]:
            self.draw_pip(location,self.colorList[self.top-1])

    def draw_pip(self,location,color):
        '''GUIDie.draw_pip(location,color)
        draws a pip at (row,col) given by location, with given color'''
        (centerx,centery) = (17+20*location[1],17+20*location[0])  # center
        self.create_oval(centerx-5,centery-5,centerx+5,centery+5,fill=color)

    def erase(self):
        '''GUIDie.erase()
        erases all the pips'''
        pipList = self.find_all()
        for pip in pipList:
            self.delete(pip)

class Shotput(Frame):
    '''frame for a game of 400 Meters'''

    def __init__(self,master,name):
        '''Decath400MFrame(master,name) -> Decath400MFrame
        creates a new 400 Meters frame
        name is the name of the player'''
        # set up Frame object
        Frame.__init__(self,master)
        self.grid()
        # label for player's name
        Label(self,text=name,font=('Arial',18)).grid(columnspan=3,sticky=W)
        # initialize game data
        self.score = 0
        self.highscore = 0
        self.gameround = -1
        self.attempts = 1
        self.play()
        
    def play(self):
        # set up score and rerolls
        self.scoreLabel = Label(self,text='Attempt #' + str(self.attempts) + ' Score: 0',font=('Arial',18))
        self.scoreLabel.grid(row=0,column=2,columnspan=3)
        self.highscoreLabel = Label(self,text='High Score: '+str(self.highscore),font=('Arial',18))
        self.highscoreLabel.grid(row=0,column=5,columnspan=3,sticky=E)
        # initialize game data
        self.score = 0
        # set up dice
        self.dice = []
        for n in range(8):
            self.dice.append(GUIDie(self,[0,2,3,4,5,6],['red']+['black']*5))
            self.dice[n].grid(row=1,column=n)
        # set up buttons
        self.rollButton = Button(self,text='Roll',command=self.roll)
        self.rollButton.grid(row=2,columnspan=1)
        self.stopButton = Button(self,text='Stop',state=ACTIVE,command=self.stop)
        self.stopButton.grid(row=3,columnspan=1)

    def roll(self):
        '''Shotput.roll()
        handler method for the roll button click'''
        # roll the dice
        self.dice[1+self.gameround].roll()
        self.score += self.dice[1+self.gameround].get_top()
        # Detects if player fouled out
        if self.dice[1+self.gameround].get_top() == 0:
            self.rollButton['state'] = DISABLED
            self.scoreLabel['text'] = 'FOULED OUT'
            self.stopButton['text'] = 'FOUL'
            return
        
        self.scoreLabel['text'] = 'Attempt #' + str(self.attempts) + ' Score: '+str(self.score)
        self.gameround += 1  # go to next round
        if self.gameround < 7:  # move buttons to next dice
            self.rollButton.grid(row=2,column=1+self.gameround,columnspan=1)
            self.stopButton.grid(row=3,column=1+self.gameround,columnspan=1)
            self.rollButton['state'] = ACTIVE
            self.stopButton['state'] = ACTIVE
        else:  # game over
            self.stop()

    def stop(self):
        '''Shotput.stop()
        handler method for the stop button click'''
        # If the 3 attempts are used then it stops the program
        if self.attempts == 3:
            self.stopButton.grid_remove()
            self.rollButton.grid_remove()
            self.highscoreLabel['text'] = "Highscore: " + str(self.highscore)
            self.scoreLabel['text'] = 'Game Over'
            return

        # Detects whether there is a foul
        if self.stopButton['text'] == 'FOUL':
            self.reset()
            return

        # Updates the scoreboard
        if self.score > self.highscore:
            self.highscore = self.score
            
        self.reset()
            
    def reset(self):
        '''Shotput.reset()
        resets the board for the next attempt'''

        # removes all the previous buttons and labels
        self.stopButton.grid_remove()
        self.rollButton.grid_remove()
        self.scoreLabel.grid_remove()
        self.highscoreLabel.grid_remove()

        self.gameround = -1
        self.attempts += 1
        self.score = 0
        self.play()

# play the game
name = input("Enter your name: ")
root = Tk()
root.title('Shot Put')
game = Shotput(root,name)
game.mainloop()

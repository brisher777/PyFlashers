'''
Created on May 18, 2013

@author: ben
'''

import Tkinter
import PyFlashers_defines
import tkFileDialog

class FlashCard(Tkinter.Tk):
    
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        
    def initialize(self):
        self.grid()
        

        self.entry_question = Tkinter.Entry()
        self.question_var = Tkinter.StringVar()
        self.question_var.set('this is a question maybe?')
        self.entry_question.grid(row = 0, column = 1)
        
        
        
        
        
        
        
        
        ## create a menu object
        self.menu_bar = Tkinter.Menu(self) 
        self['menu'] = self.menu_bar 
        self.file_menu = Tkinter.Menu(self.menu_bar)  
        self.menu_bar.add_cascade(label = 'File', menu=self.file_menu)
        self.file_menu.add_command(label = 'Open')#, command = self.open_file)
        self.file_menu.add_command(label = 'Save as...')#, command = self.save_as)
        
        
    ## child window generator
    ## generic for now
    ## one window will be for generation
    ## one window will be for reading / practicing the flash cards
    def win2(self):
        # this is the child window
        board = Tkinter.Toplevel()
        board.title("Window 2")
        s1Var = Tkinter.StringVar()
        s2Var = Tkinter.StringVar()
        s1Var.set("s1")
        s2Var.set("s2")
        square1Label = Tkinter.Label(board,textvariable=s1Var)
        square1Label.grid(row=0, column=7)
        square2Label = Tkinter.Label(board,textvariable=s2Var)
        square2Label.grid(row=0, column=6)
        
if __name__ == '__main__':
    app = FlashCard(None)
    app.title('PyFlashers')
    app.mainloop()
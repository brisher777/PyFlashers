'''
Created on May 18, 2013

@author: ben

-- TODO --
  if a number isn't in a regex of the tree, keep processing new input:
      else show that number's question/answer
  decide on user interaction; enter, button, etc...
  when opening a file, only look for xml

-- END -- 

-- LAYOUT -- 
3 main entry fields for I/O
    1 number
    1 question
    1 answer
    
2 full windows, both derived from a root window or the root window will be input with an option to start regurgitation in a child window
    1 for input
          twitter length messages for input?
    1 for regurgitation
        for regurg, fill in the blank for the answer and then compare to the original
-- END -- 

options to save or open the file 

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
        
        self.question_var = Tkinter.StringVar()
        self.entry_question = Tkinter.Entry(self, textvariable = self.question_var)
        self.question_var.set('this is a question maybe?')
        self.entry_question.grid(row = 0, column = 1)
        
        self.answer_var = Tkinter.StringVar()
        self.entry_answer = Tkinter.Entry(self, textvariable = self.answer_var)
        self.answer_var.set('this is a question maybe?')
        self.entry_answer.grid(row = 1, column = 1)
        
        self.number_var = Tkinter.StringVar()        
        self.entry_number = Tkinter.Entry(self, textvariable = self.number_var)
        self.number_var.set('this is a question maybe?')
        self.entry_number.grid(row = 2, column = 1)
        
        
        
        
        
        ## create a menu object
        self.menu_bar = Tkinter.Menu(self) 
        self['menu'] = self.menu_bar 
        self.file_menu = Tkinter.Menu(self.menu_bar)  
        self.menu_bar.add_cascade(label = 'File', menu=self.file_menu)
        self.file_menu.add_command(label = 'Open', command = self.open_file)
        self.file_menu.add_command(label = 'Save as...', command = self.save_as)
        
    def save_as(self):
        file_name = tkFileDialog.asksaveasfilename(parent = self, title = 'Save the file as...')
        if len(file_name) > 0:
            saved_file = open('%s' % file_name, 'w')
            print 'you saved a file'
            #file.write('you saved a file') ## actually write something relevant later
            saved_file.close()
            
    def open_file(self):
        file_name = tkFileDialog.askopenfilename(parent = self, title = 'Open file...')
        opened_file = open('%s' % file_name, 'r')
        line = opened_file.readline()
        ## check for a non-null file
        ## open it in the appropriate way
        print 'you opened a file'
            
            
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
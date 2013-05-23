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
    3 labels, 1 for ea. above
    1 menu toolbar, write to file and read from file will be handled there
    
    
2 full windows, both derived from a root window or the root window will be input with an option to start regurgitation in a child window
    1 for input
          twitter length messages for input?
    1 for regurgitation
        for regurg, fill in the blank for the answer and then compare to the original
-- END -- 

-- IDEA --
2 radio buttons, when one is checked, its in input mode else it's in regurg mode.
-- END --

-- IMPLEMENTATION CONCEPT --
when a field has an entry in it from the user
.get() it, pass it to _defines and grab an object to later write to file
also use .set() to make it an empty box after each entry while incrementing
the #number# field
-- NEXT --
for answer comparison, if the answer isn't 100% right, but there are matching words
print out the matching words with variable length _______'s where the words were
either wrong or missing.  If it's completely wrong (else) then tell them they're dumb
-- END --

-- THINGS TO UNFUCK --
number field doesn't need a text field, an entry will do fine, ... fix it

'''

import Tkinter
#import PyFlashers_defines
import tkFileDialog

class FlashCard(Tkinter.Frame):
    def __init__(self, parent):
        Tkinter.Frame.__init__(self, parent)   
        self.parent = parent        
        self.initialize()


    def initialize(self):
        
        self.parent.title("PyFlashers")
        
        menu_bar = Tkinter.Menu(self.parent)
        self.parent.config(menu = menu_bar)
        
        file_menu = Tkinter.Menu(menu_bar)
        file_menu.add_command(label = 'Open', command = self.open_file)
        file_menu.add_command(label = 'Save as...',
                                   command = self.save_as)
        menu_bar.add_cascade(label = 'File', menu = file_menu)
        
        
        ###############################################################
        self.toolbar = Tkinter.Frame()
        self.done_next = Tkinter.Button(name="toolbar", text="Next", 
                              borderwidth=1)#, command=self.OnBold,)
        self.done_next.pack(in_=self.toolbar, side="right")
        
        self.something = Tkinter.Button(name='stuff', text='stuff',
                                        borderwidth = 1)
        self.something.pack(in_=self.toolbar, side = 'left')
        
        text_frame_1 = Tkinter.Frame(borderwidth=1, relief="sunken")
        self.text_1 = Tkinter.Text(height = 5, width = 30, wrap="word", 
                                   background="white", borderwidth=0, 
                                   highlightthickness=0)
        
        text_frame_2 = Tkinter.Frame(borderwidth=1, relief="sunken")
        self.text_2 = Tkinter.Text(height = 5, width = 30, wrap="word", background="white", 
                            borderwidth=0, highlightthickness=0)
        
        text_frame_3 = Tkinter.Frame(borderwidth=1, relief="sunken")
        self.text_3 = Tkinter.Text(height = 5, width = 30, wrap="word", background="white", 
                            borderwidth=0, highlightthickness=0)
        #self.vsb = Tkinter.Scrollbar(orient="vertical", borderwidth=1,
                                #command=self.text.yview)
        #self.text.configure(yscrollcommand=self.vsb.set)
        #self.vsb.pack(in_=text_frame,side="right", fill="y", expand=False)
        self.text_1.pack(in_=text_frame_1, side="left", fill="both", expand=True)
        self.text_2.pack(in_=text_frame_2, side="left", fill="both", expand=True)
        self.text_3.pack(in_=text_frame_3, side="left", fill="both", expand=True)
        self.toolbar.pack(side="top", fill="x")

        text_frame_1.pack(side="bottom", fill="both", expand=True)
        text_frame_2.pack(side="bottom", fill="both", expand=True)
        text_frame_3.pack(side="bottom", fill="both", expand=True)
        ################################################################
        
        
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
        
        '''
        
        
        self.num_label = Tkinter.Label(self, text = 'Index Number: ').grid(row = 0, column = 0)
        self.q_label_in = Tkinter.Label(self, text = 'Question Input: ').grid(row = 1, column = 0)
        self.q_label_in = Tkinter.Label(self, text = 'Answer Input: ').grid(row = 2, column = 0)
        
        self.question_var = Tkinter.StringVar()
        self.entry_question = Tkinter.Entry(self, textvariable = self.question_var)
        self.question_var.set('this is a question maybe?')
        self.entry_question.grid(row = 0, column = 1)
        
        self.answer_var = Tkinter.StringVar()
        self.entry_answer = Tkinter.Entry(self, textvariable = self.answer_var)
        self.answer_var.set('this is a answer maybe?')
        self.entry_answer.grid(row = 1, column = 1)
        
        self.number_var = Tkinter.StringVar()        
        self.entry_number = Tkinter.Entry(self, textvariable = self.number_var, width = 50)
        self.number_var.set('this is a number maybe?')
        self.entry_number.grid(row = 2, column = 1, rowspan = 5, columnspan = 10, sticky = 'S')
        
        
        self.w = Tkinter.Canvas(self, width = 50, height = 20)
        self.w.create_text(10, 10, text = 'stuff\nstuff\nstuff\nstuff', anchor = 'nw')
        self.w.grid(row = 2, column = 1)

        
        self.text = Tkinter.Text(wrap = 'word', background = 'white',
                                 borderwidth = 0, highlightthickness = 0)
        self.text_frame = Tkinter.Frame(self.text, borderwidth = 1, 
                                        relief = 'sunken')
        self.vsb = Tkinter.Scrollbar(self.text_frame, orient = 'vertical', 
                                     borderwidth = 1)
        self.text.configure(yscrollcommand = self.vsb.set)
        self.text.grid(row = 2, column = 1)
                
        
        
        ## create a menu object
        self.menu_bar = Tkinter.Menu(self) 
        self['menu'] = self.menu_bar 
        self.file_menu = Tkinter.Menu(self.menu_bar)  
        self.menu_bar.add_cascade(label = 'File', menu=self.file_menu)
        self.file_menu.add_command(label = 'Open', command = self.open_file)
        self.file_menu.add_command(label = 'Save as...',
                                   command = self.save_as)
        self.menu_bar.pack(root)


        '''           
            
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

def main():
    
    root = Tkinter.Tk()
    #root.geometry('250x150+300+300')
    app = FlashCard(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()
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
-- NEXT --
validate entry to 3 digits for number area
-- END --

-- THINGS TO UNFUCK --

-- END -- 
'''

import Tkinter as tk
import PyFlashers_defines as pf
import tkFileDialog
import xml.etree.ElementTree as ET

class FlashCard(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)   
        self.parent = parent        
        self.initialize()


    def initialize(self):
        
        self.parent.title("PyFlashers")
        self.text_bool = False
        
        ###############################################################
        ################            menu bar            ###############
        ###############################################################
            
        menu_bar = tk.Menu(self.parent)
        self.parent.config(menu = menu_bar)

        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label = 'Open', command = self.open_file)
        file_menu.add_command(label = 'Save as...',
                                   command = self.save_as)
        menu_bar.add_cascade(label = 'File', menu = file_menu)
              
        ###############################################################
        ################            tool bar            ###############
        ###############################################################
        
        toolbar = tk.Frame()
        
        done_next = tk.Button(name="toolbar", text="Next", 
                              borderwidth=1, command = self.next)
        done_next.pack(in_=toolbar, side="right")
        
        go_to_button = tk.Button(name='go To', text='Go to...',
                                        borderwidth = 1)
        go_to_button.pack(in_=toolbar, side = 'right')

        self.space_var = tk.IntVar()
        
        create_button = tk.Radiobutton(toolbar, text = 'Creation Station',
                                       variable = self.space_var, value = 0, 
                                       indicatoron = 0, command = self.setup)
        create_button.pack(side='left')
        
        reader_button = tk.Radiobutton(toolbar, text = 'Reader', 
                                       variable = self.space_var, value = 1, 
                                       indicatoron = 0, command = self.setup)
        reader_button.pack(side='left')
        
        self.num_var = tk.StringVar()
        num_display = tk.Entry(toolbar, width = 8,
                                         justify = 'center', 
                                         textvariable = self.num_var)
        self.num_var.set('0')
        num_display.pack(in_ = toolbar, expand = True, fill = tk.Y)
        
        toolbar.pack(side="top", fill="x")
        
        ###############################################################
        ################         text frames            ###############
        ###############################################################
    def text_frame(self):
        if self.text_bool == False:
            self.text_frame_1 = tk.Frame(borderwidth=1, relief="sunken")
            self.answer_text = tk.Text(height = 5, width = 30, wrap="word", 
                                       background="white", borderwidth=0, 
                                       highlightthickness=0)
            
            self.text_frame_2 = tk.Frame(borderwidth=1, relief="sunken")
            self.question_text = tk.Text(height = 5, width = 30, wrap="word", 
                             background="white", borderwidth=0, 
                             highlightthickness=0)
            
            self.answer_text.pack(in_= self.text_frame_1, side="left", fill="both", 
                        expand=True)
            self.question_text.pack(in_= self.text_frame_2, side="left", fill="both", 
                        expand=True)
            
    
            self.text_frame_1.pack(side="bottom", fill="both", expand=True)
            self.text_frame_2.pack(side="bottom", fill="both", expand=True)
            
            ###############################################################
            ################             labels             ###############
            ###############################################################
            self.q_label = tk.Label(self.text_frame_2, 
                               text = 'Question Input', width = 12)
            self.q_label.pack(side = 'left')
            
            self.a_label = tk.Label(self.text_frame_1, 
                               text = 'Answer Input', width = 12)
            self.a_label.pack(side = 'left')
            self.text_bool = True
        else:
            pass
        
    def save_as(self):
        file_name = tkFileDialog.asksaveasfilename(parent = self, 
                                                   title = 'Save the file as...')
        if len(file_name) > 0:
            saved_file = open('%s' % file_name, 'w')
            print 'you saved a file'
            #file.write('you saved a file') ## actually write something relevant later
            saved_file.close()
            
    def open_file(self):
        file_name = tkFileDialog.askopenfilename(parent = self, 
                                                 title = 'Open file...')
        opened_file = open('%s' % file_name, 'r')
        #line = opened_file.readlines()
        self.pf_obj = pf.PyFlasher(opened_file)
        self.xml_obj = self.pf_obj.read_xml()
        
    def next(self):
        temp_display = self.xml_obj.next()
        
        self.num_var.set(temp_display[0])
        
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(tk.END, temp_display[1])
        
        self.answer_text.delete(1.0, tk.END)
        self.answer_text.insert(tk.END, temp_display[2])

            
    def setup(self):
        if self.space_var.get() == 0:
            self.text_frame()
            self.q_label.configure(text = 'Question Input')
            self.a_label.configure(text = 'Answer Input')
        elif self.space_var.get() == 1:
            self.text_frame()
            self.q_label.configure(text = 'Question Viewer')
            self.a_label.configure(text = 'Answer Checker')
        
def main():
    
    root = tk.Tk()
    #root.geometry('250x150+300+300')
    app = FlashCard(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()
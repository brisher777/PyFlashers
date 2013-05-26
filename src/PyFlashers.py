'''
Created on May 18, 2013

@author: ben

-- TODO --
learn how to use an 'enter keystroke' event handler
-- NEXT -- 
randomly select slightly insulting messages when a user inputs a wrong statement
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

'''

import Tkinter as tk
import tkFileDialog
import xml.etree.ElementTree as ET

class FlashCard(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)   
        self.parent = parent        
        self.initialize()

    def initialize(self):
        self.file_list = []
        self.parent.title("PyFlashers")
        
        ###############################################################
        ################            menu bar            ###############
        ###############################################################
            
        menu_bar = tk.Menu(self.parent)
        self.parent.config(menu = menu_bar)

        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label = 'Open', command = self.open_file)
        file_menu.add_command(label = 'Save as...', command = self.save_as)
        menu_bar.add_cascade(label = 'File', menu = file_menu)
        
        help_menu = tk.Menu(menu_bar)
        help_menu.add_command(label = 'OMG Help!') ## add command later
        menu_bar.add_cascade(label = 'Help', menu = help_menu)
             
        ###############################################################
        ################            tool bar            ###############
        ###############################################################
        
        toolbar = tk.Frame()
        
        done_next = tk.Button(name="toolbar", text="Next", 
                              borderwidth=1, command = self.next)
        done_next.pack(in_=toolbar, side="right")
        
        go_to_button = tk.Button(name='go To', text='Go to...',
                                        borderwidth = 1, command = self.go_to)
        go_to_button.pack(in_=toolbar, side = 'right')

        self.space_var = tk.IntVar()
        
        create_button = tk.Radiobutton(toolbar, text = 'Creation Station',
                                       variable = self.space_var, value = 0, 
                                       indicatoron = 0, command = self.setup)
        create_button.pack(side='left', fill = 'y')
        
        reader_button = tk.Radiobutton(toolbar, text = 'Reader', 
                                       variable = self.space_var, value = 1, 
                                       indicatoron = 0, command = self.setup)
        reader_button.pack(side='left', fill = 'y')
        
        self.num_var = tk.StringVar()
        num_display = tk.Entry(toolbar, width = 8,
                                         justify = 'center', 
                                         textvariable = self.num_var)
        self.num_var.set('0')
        num_display.pack(in_ = toolbar, expand = True, fill = tk.Y)
        
        toolbar.pack(side="top", fill="x")
        self.text_frame()

    def text_frame(self):
        
        ###############################################################
        ################         text frames            ###############
        ###############################################################
        
        self.below_tool = tk.Frame(borderwidth = 1)
        self.text_frame_1 = tk.Frame(borderwidth=1, relief="sunken")
        self.answer_text = tk.Text(height = 5, width = 30, wrap="word", 
                                   background="white", borderwidth=0, 
                                   highlightthickness=0)
        
        self.text_frame_2 = tk.Frame(borderwidth=1, relief="sunken")
        self.question_text = tk.Text(height = 5, width = 30, wrap="word", 
                         background="white", borderwidth=0, 
                         highlightthickness=0)
        
        self.answer_text.pack(in_= self.text_frame_1, side="left", 
                              fill="both", expand=True)
        self.question_text.pack(in_= self.text_frame_2, side="left", 
                                fill="both", expand=True)
        
        self.text_frame_1.pack(in_= self.below_tool, side="bottom", 
                               fill="both", expand=True)
        self.text_frame_2.pack(in_ = self.below_tool, side="bottom", 
                               fill="both", expand=True)
        self.below_tool.pack(side = 'top', fill = 'both', expand = True)
        
        ###############################################################
        ################             labels             ###############
        ###############################################################
        
        self.q_label = tk.Label(self.text_frame_2, 
                           text = 'Question Input', width = 12)
        self.q_label.pack(side = 'left')
        
        self.a_label = tk.Label(self.text_frame_1, text = 'Answer Input', 
                                width = 12)
        self.a_label.pack(side = 'left')
        
    def save_as(self):
        file_name = tkFileDialog.asksaveasfilename(parent = self, 
                                                   title = 'Save the file as...')
        if len(file_name) > 0:
            saved_file = open('%s' % file_name, 'w')
            saved_file.write('<?xml version="1.0"?>\n')
            saved_file.write('<data>')
            for i in self.file_list:
                saved_file.write(ET.tostring(i))     
            saved_file.write('</data>')
            saved_file.close()
    
    def open_file(self):
        self.file_name = tkFileDialog.askopenfilename(parent = self, 
                                                 title = 'Open file...')
        opened_file = open('%s' % self.file_name, 'r')
        self.xml_obj = self.read_xml(opened_file)
        
    def go_to(self):
        if self.space_var.get() == 0:
            pass
        elif self.space_var.get() == 1:
            tree = ET.parse(self.file_name)
            root = tree.getroot()
            print self.num_var.get() == root.findall('number')
            print root.find('number').text == self.num_var.get()
            '''
            if number[0] == self.num_var.get():
                self.question_text.delete(1.0, tk.END)
                self.answer_text.delete(1.0, tk.END)
                self.num_var.set(number[0])
                self.question_text.insert(1.0, number[1])
                self.answer_text.insert(1.0, number[2])
            ''' 
                     
        
    def read_xml(self, data):
        tree = ET.parse(data)
        root = tree.getroot()
        for number in root.findall('number'):
            question = number.find('question').text
            answer = number.find('answer').text
            yield number.text, question, answer
            
    def compare(self):
        pass
    '''
        if self.answer_text.get(1.0, tk.END) == get the original answer using the number index:
            print 'you\'re right'
    '''
        
            
    def next(self):
        
        if self.space_var.get() == 0:
            #tree = ET.parse(self.file_list)
            #root = tree.getroot()
            
            num = self.num_var.get()
            question = self.question_text.get(1.0, tk.END)
            answer = self.answer_text.get(1.0, tk.END)
            ###############################################################
            ##########  This builds a list of generator objects  ##########
            ###############################################################
            self.file_list.append(self.build(num, question, answer))#.iter())
            self.num_var.set(int(num) + 1)
            self.answer_text.delete(1.0, tk.END)
            self.question_text.delete(1.0, tk.END)   
            
        elif self.space_var.get() == 1:
            try:
                temp_display = self.xml_obj.next()
                
                self.num_var.set(temp_display[0])
                
                self.question_text.delete(1.0, tk.END)
                self.question_text.insert(tk.END, temp_display[1])
                
                #self.answer_text.delete(1.0, tk.END)
                #self.answer_text.insert(tk.END, temp_display[2])
            except AttributeError:
                self.question_text.delete(1.0, tk.END)
                self.question_text.insert(1.0, 'hey dummy, open a file first')
            except StopIteration:
                self.question_text.delete(1.0, tk.END)
                self.answer_text.delete(1.0, tk.END)
                self.question_text.insert(1.0, 'You have reached the end of the file')
                
    def build(self, number, question, answer):
        
        ## build an xml object and return it
        ## to the caller
        top = ET.Element('number')
        top.text = number
        quest = ET.SubElement(top, 'question')
        quest.text = question
        ans = ET.SubElement(top, 'answer')
        ans.text = answer
        return top
    
    def setup(self):
        if self.space_var.get() == 0:
            self.below_tool.destroy()
            self.text_frame()
            try:
                self.check_ans.destroy()
            except AttributeError:
                self.q_label.configure(text = 'Question Input')
                self.a_label.configure(text = 'Answer Input')
                self.a_label.pack(side = 'left')
        elif self.space_var.get() == 1:
            self.below_tool.destroy()
            self.text_frame()
            self.q_label.configure(text = 'Question Viewer')
            self.a_label.configure(text = 'Answer Checker')
            self.a_label.pack(side = 'top')
            self.check_ans = tk.Button(name="checker", text="Compare", 
                  borderwidth=1, command = self.compare)
            self.check_ans.pack(in_ = self.text_frame_1, side = 'bottom', 
                                fill = 'x')
        
def main():
    root = tk.Tk()
    #root.geometry('250x150+300+300')
    app = FlashCard(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()
'''
Created on May 18, 2013

@author: ben

-- TODO --
learn how to use an 'enter keystroke' event handler and a tab handler
-- NEXT -- 
add a help file
-- END --
'''

import Tkinter as tk
import tkFileDialog as tkfd
import xml.etree.ElementTree as ET
import re

class FlashCard(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)   
        self.parent = parent        
        self.initialize()

    def initialize(self):
        ## empty list for storing created 'cards'
        self.file_list = []
        
        self.parent.title("PyFlashers")
        
        ## part of entry validation for the number display
        self.valid_command = (self.register(self.validate), '%d', '%i', '%P', \
                         '%s', '%S', '%v', '%V', '%W')
        
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
        help_menu.add_command(label = 'OMG Help!')
        menu_bar.add_cascade(label = 'Help', menu = help_menu)
             
        ###############################################################
        ################            tool bar            ###############
        ###############################################################
        
        toolbar = tk.Frame()
        
        ## next button
        done_next = tk.Button(name = 'toolbar', text = 'Next', borderwidth = 1, 
                              command = self.next)
        done_next.pack(in_ = toolbar, side = 'right')
        
        ## go to button
        go_to_button = tk.Button(name='go To', text='Go to...', borderwidth = 1, 
                                 command = self.go_to)
        go_to_button.pack(in_ = toolbar, side = 'right')
        
        ## variable to keep track of which workspace the user is in
        self.space_var = tk.IntVar()
        
        ## radio button to select the workspace for creating 'cards'
        create_button = tk.Radiobutton(toolbar, text = 'Creation Station',
                                       variable = self.space_var, value = 0, 
                                       indicatoron = 0, command = self.setup)
        create_button.pack(side = 'left', fill = 'y')
        
        ## radio button to select the workspace to review 'cards'
        reader_button = tk.Radiobutton(toolbar, text = 'Reader', 
                                       variable = self.space_var, value = 1, 
                                       indicatoron = 0, command = self.setup)
        reader_button.pack(side='left', fill = 'y')
        
        ## display for which numbered card the user is working with currently
        self.num_var = tk.StringVar()
        num_display = tk.Entry(toolbar, width = 8, justify = 'center',
                               textvariable = self.num_var, validate = 'key',
                               vcmd = self.valid_command)
        self.num_var.set('1')
        num_display.pack(in_ = toolbar, expand = True, fill = tk.Y)
        
        toolbar.pack(side="top", fill="x")
        self.text_frame()

    def text_frame(self):
        
        ###############################################################
        ################         text frames            ###############
        ###############################################################
        
        ## variable of all the widgets below the toolbar
        ## it gets destroyed and redrawn each time the user switches between 
        ## workspaces
        self.below_tool = tk.Frame(borderwidth = 1)
        
        ## answer text box
        self.text_frame_1 = tk.Frame(borderwidth = 1, relief = 'sunken')
        self.answer_text = tk.Text(height = 5, width = 30, wrap = 'word', 
                                   background = 'white', borderwidth = 0, 
                                   highlightthickness = 0)
        self.answer_text.pack(in_ = self.text_frame_1, side = 'left',
                      fill = 'both', expand = True)
        
        ## question text box
        self.text_frame_2 = tk.Frame(borderwidth = 1, relief = 'sunken')
        self.question_text = tk.Text(height = 5, width = 30, wrap = 'word', 
                                     background = 'white', borderwidth = 0, 
                                     highlightthickness = 0)
        self.question_text.pack(in_ = self.text_frame_2, side = 'left', 
                                fill = 'both', expand = True)
        
        self.text_frame_1.pack(in_ = self.below_tool, side = 'bottom', 
                               fill = 'both', expand = True)
        self.text_frame_2.pack(in_ = self.below_tool, side = 'bottom', 
                               fill = 'both', expand = True)
        self.below_tool.pack(side = 'top', fill = 'both', expand = True)
        
        ###############################################################
        ################             labels             ###############
        ###############################################################
        
        self.q_label = tk.Label(self.text_frame_2, text = 'Question Input', 
                                width = 12)
        self.q_label.pack(side = 'left')
        
        self.a_label = tk.Label(self.text_frame_1, text = 'Answer Input', 
                                width = 12)
        self.a_label.pack(side = 'left')
        
    def save_as(self):
        file_name = tkfd.asksaveasfilename(parent = self, 
                                           title = 'Save the file as...')
        
        ## if the filename isn't blank, build the xml file
        if len(file_name) > 0:
            saved_file = open('%s' % file_name, 'w')
            saved_file.write('<?xml version="1.0"?>\n')
            saved_file.write('<data>')
            for i in self.file_list:
                saved_file.write(ET.tostring(i))     
            saved_file.write('</data>')
            saved_file.close()
    
    def open_file(self):
        self.file_name = tkfd.askopenfilename(parent = self, 
                                              title = 'Open file...')
        opened_file = open('%s' % self.file_name, 'r')
        
        ## create an element tree object for use in other places
        self.xml_obj = self.read_xml(opened_file)
        
    def go_to(self):
        ## checks workspace, 0 is for 'card' creation, 1 is for 'card' review
        if self.space_var.get() == 0:
            ## finds the entry corresponding to the number displayed and 
            ## displays the qestion and answer
            for node in self.file_list:
                if node.text == self.num_var.get():
                    self.question_text.delete(1.0, tk.END)
                    self.answer_text.delete(1.0, tk.END)
                    self.num_var.set(node.text)
                    self.question_text.insert(1.0, node.find('question').text)
                    self.answer_text.insert(1.0, node.find('answer').text)
        ## checking workspace
        else:
            ## displays the entry's corresponding question only, since this
            ## is the review portion of the program
            try:
                tree = ET.parse(self.file_name)
                root = tree.getroot()
                for node in root:
                    if node.text == self.num_var.get():
                        self.question_text.delete(1.0, tk.END)
                        self.answer_text.delete(1.0, tk.END)
                        self.num_var.set(node.text)
                        self.question_text.insert(1.0, node.find('question').text)
            except AttributeError:
                self.question_text.delete(1.0, tk.END)
                self.answer_text.delete(1.0, tk.END)
                self.question_text.insert(1.0, 'Did you open a file?')    
        
    ## generator function to yield 1 'number' entry from the opened file
    def read_xml(self, data):
        tree = ET.parse(data)
        self.root = tree.getroot()
        for number in self.root.findall('number'):
            question = number.find('question').text
            answer = number.find('answer').text
            yield number.text, question, answer
            
    def compare(self):
        ## completely wrong answer tracker
        counter = 0
        
        ## grab existing answer before deletion
        user_answer = self.answer_text.get(1.0, tk.END).strip()
        self.answer_text.delete(1.0, tk.END)
        
        ## cycle through xml file
        for node in self.root:
            ## find the specified entry
            if node.text == self.num_var.get():
                ## if the answer is completely right, congratulate and 
                ## increment the counter
                if user_answer == node.find('answer').text:
                    self.answer_text.insert(tk.END, 'Who\'s awesome? You\'re awesome!')
                    counter += 1
                ## if the answer isn't completely right, cycle through and 
                ## display all the correct words that were entered, and 
                ## blank lines where words were missed.  This can be repeated
                ## until the answer is completely right
                else:
                    for orig_word in re.split('\W+', node.find('answer').text):
                        for ans_word in re.split('\W+', user_answer):
                            if orig_word == ans_word:
                                counter += 1
                                self.answer_text.insert(tk.END, orig_word + ' ')
                                break
                        if orig_word != ans_word:
                            self.answer_text.insert(tk.END, ('_' * len(orig_word) + ' '))
                ## counter is only incremented on complete or partial correct 
                ## answers, so a value of zero will be rewarded with an inspiring 
                ## message
                if counter == 0:
                    self.answer_text.delete(1.0, tk.END)
                    self.answer_text.insert(tk.END, 'You were completely wrong, suck less next time.')
                        
    ## just limiting input to the number field to 3 digits
    def validate(self, action, index, value_if_allowed, prior_value, text, 
                 validation_type, trigger_type, widget_name):
        if text in '0123456789' and len(value_if_allowed) < 4:
            return True
        else:
            return False
                
    def next(self):
        ## check workspace
        if self.space_var.get() == 0:
            ## grab the current number, quesiton, and answer
            num = self.num_var.get()
            question = self.question_text.get(1.0, tk.END)
            answer = self.answer_text.get(1.0, tk.END)
            ## append an element tree object to a list
            self.file_list.append(self.build(num, question, answer))
            ## increment the number
            self.num_var.set(int(num) + 1)
            ## blank out the entry once it's in the list
            self.answer_text.delete(1.0, tk.END)
            self.question_text.delete(1.0, tk.END)
        else:
            ## display the next question
            self.answer_text.delete(1.0, tk.END)
            try:
                temp_display = self.xml_obj.next()
                self.num_var.set(temp_display[0])
                self.question_text.delete(1.0, tk.END)
                self.question_text.insert(tk.END, temp_display[1])
            except AttributeError: ## no file opened
                self.question_text.delete(1.0, tk.END)
                self.question_text.insert(1.0, 'hey dummy, open a file first')
            except StopIteration: ## no more objects in the generator
                self.question_text.delete(1.0, tk.END)
                self.answer_text.delete(1.0, tk.END)
                self.question_text.insert(1.0, 'You have reached the end of the file')
                
    def build(self, number, question, answer):
        ## build an xml object and return it to the caller
        top = ET.Element('number')
        top.text = number
        quest = ET.SubElement(top, 'question')
        quest.text = question
        ans = ET.SubElement(top, 'answer')
        ans.text = answer
        return top
    
    def setup(self):
        ## check workspace
        if self.space_var.get() == 0:
            ## nuke everything below the toolbar and redraw it
            self.below_tool.destroy()
            self.num_var.set('1')
            self.text_frame()
            try:
                self.check_ans.destroy()
            except AttributeError: ## if check answer isn't present
                self.q_label.configure(text = 'Question Input')
                self.a_label.configure(text = 'Answer Input')
                self.a_label.pack(side = 'left')
        else:
            ## nuke everything below the toolbar and redraw it
            self.below_tool.destroy()
            self.num_var.set('1')
            self.text_frame()
            self.q_label.configure(text = 'Question Viewer')
            self.a_label.configure(text = 'Answer Checker')
            self.a_label.pack(side = 'top')
            ## build the compare button, only necessary in the review
            ## workspace
            self.check_ans = tk.Button(name = 'checker', text = 'Compare', 
                                       borderwidth = 1, command = self.compare)
            self.check_ans.pack(in_ = self.text_frame_1, side = 'bottom', 
                                fill = 'x')
        
def main():
    root = tk.Tk()
    app = FlashCard(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()
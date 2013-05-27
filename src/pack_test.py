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
import tkFileDialog
import xml.etree.ElementTree as ET

def go_to(self):
    if self.space_var.get() == 0:
        if int(self.num_var.get()) > 999 or int(self.num_var.get()) < 0:
            self.question_text.delete(1.0, tk.END)
            self.answer_text.delete(1.0, tk.END)
            self.question_text.insert(1.0, 'Let\'s be realistic, shall we?')
        else:
            for node in self.file_list:
                if node.text == self.num_var.get():
                    self.question_text.delete(1.0, tk.END)
                    self.answer_text.delete(1.0, tk.END)
                    self.num_var.set(node.text)
                    self.question_text.insert(1.0, node.find('question').text)
                    self.answer_text.insert(1.0, node.find('answer').text)
        self.file_list
    elif self.space_var.get() == 1:
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        if int(self.num_var.get()) > 999 or int(self.num_var.get()) < 0:
            self.question_text.delete(1.0, tk.END)
            self.answer_text.delete(1.0, tk.END)
            self.question_text.insert(1.0, 'Let\'s be realistic, shall we?')
        else:
            for number in root:
                if number.text == self.num_var.get():
                    self.question_text.delete(1.0, tk.END)
                    self.answer_text.delete(1.0, tk.END)
                    self.num_var.set(number.text)
                    self.question_text.insert(1.0, number.find('question').text)
                    self.answer_text.insert(1.0, number.find('answer').text)
                else:
                    self.question_text.delete(1.0, tk.END)
                    self.answer_text.delete(1.0, tk.END)
                    self.question_text.insert(1.0, 'Are you sure about that number?')
        
def go_to(self):
    if int(self.num_var.get()) > 999 or int(self.num_var.get()) < 0:
        self.question_text.delete(1.0, tk.END)
        self.answer_text.delete(1.0, tk.END)
        self.question_text.insert(1.0, 'Let\'s be realistic, shall we?')
    else:
        if self.space_var.get() == 0:
            for node in self.file_list:
                if node.text == self.num_var.get():
                    self.question_text.delete(1.0, tk.END)
                    self.answer_text.delete(1.0, tk.END)
                    self.num_var.set(node.text)
                    self.question_text.insert(1.0, node.find('question').text)
                    self.answer_text.insert(1.0, node.find('answer').text)
                else:
                    self.question_text.delete(1.0, tk.END)
                    self.answer_text.delete(1.0, tk.END)
                    self.question_text.insert(1.0, 'Are you sure about that number?')
        elif self.space_var.get() == 1:
            tree = ET.parse(self.file_name)
            root = tree.getroot()
            for node in root:
                if node.text == self.num_var.get():
                    self.question_text.delete(1.0, tk.END)
                    self.answer_text.delete(1.0, tk.END)
                    self.num_var.set(node.text)
                    self.question_text.insert(1.0, node.find('question').text)
                    self.answer_text.insert(1.0, node.find('answer').text)
                else:
                    self.question_text.delete(1.0, tk.END)
                    self.answer_text.delete(1.0, tk.END)
                    self.question_text.insert(1.0, 'Are you sure about that number?')




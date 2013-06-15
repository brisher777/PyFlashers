'''
Created on May 18, 2013

@author: ben

-- TODO --
finish help file
-- NEXT -- 
clean up save_as section (may not need renumbering with smarter buttons)
-- END --
'''

import Tkinter as tk
from tkFileDialog import askopenfilename, asksaveasfilename
import xml.etree.ElementTree as ET
from random import randrange
from re import split, search
from tkFont import Font
import ttk

class FlashCard(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent        
        self.custom_font = Font(family='Times', size=17)
        self.label_font = Font(family='URW Chancery L', size=16)
        self.default_font = Font(family='Century Schoolbook L', size=17)        
        self.style = ttk.Style()
        self.initialize()
        
    def initialize(self):
        '''Build the initial GUI with creation workspace as the default'''
        
        self.file_list = []
        
        self.GATE_OPEN = True
        self.FILE_EXISTS = False
        self.GOTO_USED = False
        
        #make things beautimous
        self.style.configure('Blue.TFrame', background='blue')
        self.style.configure('Blue.TNotebook', background='blue')
        self.style.configure('Blue.TButton', foreground='yellow',
                             font=self.default_font)
        self.style.map('Blue.TButton', background= [("active", "skyblue"),
                                                    ("!disabled", "blue")])
        self.style.configure('Blue.TNotebook.Tab', background='blue', 
                             font=self.label_font, foreground='yellow')
        self.style.map('Blue.TNotebook.Tab', background= [("active", "skyblue"),
                                                          ("!disabled", "blue")])
        
        self.parent.title('PyFlashers')
        
        # part of entry validation for the number display
        self.valid_command = (self.register(self.validate), '%d', '%i', '%P', \
                         '%s', '%S', '%v', '%V', '%W')
        
        '''
                                    menu bar
        '''
        
        menu_bar = tk.Menu(self.parent, background='dark blue', 
                           foreground='yellow', font=self.default_font,
                           activebackground='skyblue')
        self.parent.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, background='dark blue', font=self.default_font,
                            foreground='yellow', activebackground='skyblue')
        file_menu.add_command(label='Open', command=self.open_file)
        file_menu.add_command(label='Save as...', command=self.save_as)
        menu_bar.add_cascade(label='File', menu=file_menu)
        
        help_menu = tk.Menu(menu_bar, bg='dark blue',foreground='yellow', 
                            font=self.default_font, activebackground='skyblue')
        help_menu.add_command(label='OMG Help!', command=self.help_page)
        menu_bar.add_cascade(label='Help', menu=help_menu)
             
        '''
                                    notebook
        '''
        
        self.tab_bar = ttk.Frame(style='Blue.TFrame')
        self.notebook = ttk.Notebook(self.tab_bar, style='Blue.TNotebook')
        self.notebook.enable_traversal()
        self.notebook.pack(in_=self.tab_bar, fill='both', expand='y', padx=2, pady=3)

        self.create_tab = ttk.Frame(self.notebook, name='creation', style='Blue.TFrame')
        self.read_tab = ttk.Frame(self.notebook, name='reader',style='Blue.TFrame')
        
        
        
        
        go_to = ttk.Button(self.create_tab, text='Go to...', command=self.go_to, 
                           style='Blue.TButton')
        go_to.grid(row=0, column=0, sticky='we')
        
        self.an_num = tk.StringVar()
        num_display = tk.Entry(self.create_tab, bd=5, relief='sunken', 
                               foreground='dark blue', width=8, 
                               justify='center', textvariable=self.an_num,
                               validate='key', vcmd=self.valid_command)
        num_display.grid(row=0, column=1, sticky='ew')
        self.an_num.set('1')
        
        next_button = ttk.Button(self.create_tab, text='Next', command=self.next,
                                 style='Blue.TButton')
        next_button.grid(row=0, column=2, sticky='nsew')
        
        text_frame_1 = ttk.Frame(self.create_tab, style='Blue.TFrame')
        self.cq_text = tk.Text(text_frame_1, height=7, wrap='word', width=45, 
                                   bg='white', bd=2, highlightthickness=0,
                                   font=self.custom_font)
        self.cq_text.pack(in_=text_frame_1)
        text_frame_1.grid(row=1, column=0, columnspan=3, sticky='nesw')
        self.cq_text.bind('<Tab>', self.focus_next_window)
        self.cq_text.bind('<Button-3>', self.right_click, add='')
        
        py_label = tk.Label(self.create_tab, text='PyFlashers', bg='blue',
                            font=self.label_font, foreground='yellow', height=2)
        py_label.grid(row=2, column=1)
        
        text_frame_2 = ttk.Frame(self.create_tab, style='Blue.TFrame')
        self.ca_text = tk.Text(text_frame_2, height=7, wrap='word', width=45,
                                bg='white', bd=2, highlightthickness=0,
                                font=self.custom_font)
        self.ca_text.pack(in_=text_frame_2)
        text_frame_2.grid(row=3, column=0, columnspan=3, sticky='snew')
        self.ca_text.bind('<Tab>', self.focus_next_window)
        self.ca_text.bind('<Button-3>', self.right_click, add='')
        
        go_to = ttk.Button(self.read_tab, text='Go to...', 
                           command=self.go_to, style='Blue.TButton')
        go_to.grid(row=0, column=0, sticky='we')
        
        self.rd_num = tk.StringVar()
        num_display = tk.Entry(self.read_tab, bd=5, relief='sunken', 
                               foreground='dark blue', width=8, 
                               justify='center', textvariable=self.rd_num,
                               validate='key', vcmd=self.valid_command)
        num_display.grid(row=0, column=1, sticky='ew')
        self.rd_num.set('0')
        
        next_button = ttk.Button(self.read_tab, text='Next', 
                                 command=self.next, style='Blue.TButton')
        next_button.grid(row=0, column=2, sticky='nsew')
        
        text_frame_1 = ttk.Frame(self.read_tab, style='Blue.TFrame')
        self.rq_text = tk.Text(text_frame_1, height=7, wrap='word', width=45, 
                                   bg='white', bd=2, highlightthickness=0,
                                   font=self.custom_font)
        self.rq_text.pack(in_=text_frame_1)
        text_frame_1.grid(row=1, column=0, columnspan=3, sticky='nesw')
        self.rq_text.bind('<Tab>', self.focus_next_window)
        self.rq_text.bind('<Button-3>', self.right_click, add='')
        
        give_button = ttk.Button(self.read_tab, text='I give up', 
                                 command=self.give_up, style='Blue.TButton')
        give_button.grid(row=2, column=0, sticky='news')
        
        comp_button = ttk.Button(self.read_tab, text='Compare', 
                                 command=self.compare, style='Blue.TButton')
        comp_button.grid(row=2, column=2, sticky='news')
        
        py_label = tk.Label(self.read_tab, text='PyFlashers', bg='blue',
                            font=self.label_font, foreground='yellow', height=2)
        py_label.grid(row=2, column=1)
    
        text_frame_2 = ttk.Frame(self.read_tab, style='Blue.TFrame')
        self.ra_text = tk.Text(text_frame_2, height=7, wrap='word', width=45,
                                bg='white', bd=2, highlightthickness=0,
                                font=self.custom_font)
        self.ra_text.pack(in_=text_frame_2)
        text_frame_2.grid(row=3, column=0, columnspan=3, sticky='snew')
        self.ra_text.bind('<Tab>', self.focus_next_window)
        self.ra_text.bind('<Button-3>', self.right_click, add='')
        
        self.notebook.add(self.create_tab, text='Creation Station')
        self.notebook.add(self.read_tab, text='Reader')
        self.tab_bar.pack()
        
        
    def save_as(self):
        ''' Saves a file in a specific xml format that the program can use later '''
        file_name = asksaveasfilename(parent=self, 
                                           title='Save the file as...',
                                           filetypes=[('xml files', '.xml'),
                                                         ('all files', '.*')])
        FILE_EXISTS = False
        shebang = '<?xml version="1.0"?>\n'
        
        if file_name:
            try:
                saved_file = open('%s' % file_name, 'r')
                FILE_EXISTS = True
            except IOError:
                saved_file = open('%s' % file_name, 'w')
                
            if FILE_EXISTS:
                lines = saved_file.readlines()
                lines = lines[:-1]
                saved_file.close()
                saved_file = open('%s' % file_name, 'w')
                if lines != []:
                    if lines[0] != shebang:
                        saved_file.write(shebang)
                        saved_file.write('<data>\n')
                    for line in lines:
                        saved_file.write(line)
                if self.file_list != []:
                    saved_file.write('</answer></number>\n')
                    for node in self.file_list:
                        saved_file.write(ET.tostring(node))
                saved_file.write('</data>')
                saved_file.close()
                tree = ET.parse(file_name)
                root = tree.getroot()
                counter = 1
                for num_node in root:
                    num_node.text = str(counter)
                    counter += 1
                saved_file = open('%s' % file_name, 'w')
                saved_file.write(shebang)
                saved_file.write('<data>')
                for line in root:
                    saved_file.write(ET.tostring(line))
                saved_file.write('</data>')
                saved_file.close()
            else:
                saved_file.write(shebang)
                saved_file.write('<data>')
                for i in self.file_list:
                    saved_file.write(ET.tostring(i))     
                saved_file.write('</data>')
                saved_file.close()

    def open_file(self):
        self.file_name = askopenfilename(parent=self, title='Open file...',
                                              filetypes=[('xml files', '.xml'),
                                                         ('all files', '.*')])
        self.opened_file = open('%s' % self.file_name, 'r')
        
        # create an element tree object for use in other places
        self.FILE_EXISTS = True
        
        self.xml_obj = self.read_xml(self.opened_file)
        
    def random_number(self):
        if self.GATE_OPEN:
            self.temp_counter = 0
            for number in self.xml_obj:
                self.temp_counter += 1
            self.temp_counter += 1
            self.GATE_OPEN = False
        return randrange(1, self.temp_counter, 1)
        
    def go_to(self):
        workspace = str(self.focus_get())
        
        if 'creation' in workspace:
            try:
                tree = ET.parse(self.file_name)
                root = tree.getroot()
                self.GOTO_USED = True
                for num in root.findall('number'):
                    if num.text == self.an_num.get():
                        self.cq_text.delete(1.0, tk.END)
                        self.ca_text.delete(1.0, tk.END)
                        self.an_num.set(num.text)
                        self.cq_text.insert(1.0, num.find('question').text)
                        self.ca_text.insert(1.0, num.find('answer').text)
                        
            except AttributeError:
                for node in self.file_list:
                    if node.text == self.an_num.get():
                        self.cq_text.delete(1.0, tk.END)
                        self.ca_text.delete(1.0, tk.END)
                        self.an_num.set(node.text)
                        self.cq_text.insert(1.0, node.find('question').text)
                        self.ca_text.insert(1.0, node.find('answer').text)
        else:
            try:
                tree = ET.parse(self.file_name)
                root = tree.getroot()
                for node in root:
                    if node.text == self.rd_num.get():
                        self.rq_text.delete(1.0, tk.END)
                        self.ra_text.delete(1.0, tk.END)
                        self.rd_num.set(node.text)
                        self.rq_text.insert(1.0, node.find('question').text)
            except AttributeError:
                self.rq_text.delete(1.0, tk.END)
                self.ra_text.delete(1.0, tk.END)
                self.rq_text.insert(1.0, 'Did you open a file?')    
        
    # generator function to yield 1 'number' entry from the opened file
    def read_xml(self, data):
        tree = ET.parse(data)
        self.root = tree.getroot()
        
        for number in self.root.findall('number'):
            question = number.find('question').text
            answer = number.find('answer').text
            yield number.text, question, answer
            
    def compare(self):
        '''Compares answers given to those in the original file'''
        counter = 0
        
        user_answer = self.ra_text.get(1.0, tk.END).strip().lower()
        self.ra_text.delete(1.0, tk.END)
        try:
            for node in self.root:
                if node.text == self.rd_num.get():
                    if user_answer == node.find('answer').text.lower():
                        self.ra_text.insert(tk.END, 'Who\'s awesome? You\'re awesome!')
                        counter += 1
                        '''
                        if the answer isn't completely right, cycle through and 
                        display all the correct words that were entered, and 
                        blank lines where words were missed.  This can be repeated
                        until the answer is completely right
                        '''
                    else:
                        for orig_word in split('\W+', node.find('answer').text):
                            for ans_word in split('\W+', user_answer):
                                if orig_word.lower() == ans_word:
                                    counter += 1
                                    self.ra_text.insert(tk.END, orig_word + ' ')
                                    break
                            if orig_word != ans_word:
                                self.ra_text.insert(tk.END, ('_' * len(orig_word) + ' '))
                    if counter == 0:
                        self.ra_text.delete(1.0, tk.END)
                        self.ra_text.insert(tk.END, 'You were completely wrong, suck less next time.')
            return 'break'
        except AttributeError:
            self.rq_text.delete(1.0, tk.END)
            self.ra_text.delete(1.0, tk.END)
            self.rq_text.insert(1.0, 'Did you open a file?')  
                        
    def validate(self, action, index, value_if_allowed, prior_value, text, 
                 validation_type, trigger_type, widget_name):
        '''limit input to the number field to 3 digits'''
        return text in '0123456789' and len(value_if_allowed) < 4
      
    def next(self):
        workspace = str(self.focus_get())
        if 'creation' in workspace:
            if self.FILE_EXISTS == 'proceed':
                if self.GOTO_USED == True:
                    ''' sanity check to not let the user overwrite entries '''
                    temp_list = []
                    for i in self.file_list:
                        match = search('\d+', ET.tostring(i))
                        temp_list.append(match.group(0))
                    max_from_file_list = int(max(temp_list)) + 1
                    
                    tree = ET.parse(self.file_name)
                    root = tree.getroot()
                    nums = []
                    for num in root.findall('number'):
                        nums.append(num.text)
                    max_from_open_file = int(max(nums)) + 1
                    
                    if max_from_open_file > max_from_file_list:
                        self.an_num.set(str(max_from_open_file))
                    else:
                        self.an_num.set(str(max_from_file_list))
                    self.GOTO_USED = False
                else:
                    num = self.an_num.get()
                    question = self.cq_text.get(1.0, tk.END)
                    answer = self.ca_text.get(1.0, tk.END)
                    self.file_list.append(self.build(num, question, answer))
                    self.an_num.set(int(num) + 1)
                    self.ca_text.delete(1.0, tk.END)
                    self.cq_text.delete(1.0, tk.END)
            else:
                num = self.an_num.get()
                question = self.cq_text.get(1.0, tk.END)
                answer = self.ca_text.get(1.0, tk.END)
                self.file_list.append(self.build(num, question, answer))
                self.an_num.set(int(num) + 1)
                self.ca_text.delete(1.0, tk.END)
                self.cq_text.delete(1.0, tk.END)
            try:
                if self.FILE_EXISTS == True:
                    tree = ET.parse(self.file_name)
                    root = tree.getroot()
                    
                    nums = []
                    for num in root.findall('number'):
                        nums.append(num.text)
                    next_max = int(max(nums)) + 1
                    question = self.cq_text.get(1.0, tk.END)
                    answer = self.ca_text.get(1.0, tk.END)
                    self.file_list.append(self.build(str(next_max), question, answer))
                    self.an_num.set(int(next_max) + 1)
                    self.ca_text.delete(1.0, tk.END)
                    self.cq_text.delete(1.0, tk.END)
                    self.FILE_EXISTS = 'proceed'
            except AttributeError:
                num = self.an_num.get()
                question = self.cq_text.get(1.0, tk.END)
                answer = self.ca_text.get(1.0, tk.END)
                self.file_list.append(self.build(num, question, answer))
                self.an_num.set(int(num) + 1)
                self.ca_text.delete(1.0, tk.END)
                self.cq_text.delete(1.0, tk.END)
            
        else:
            self.ra_text.delete(1.0, tk.END)
            try:
                random_num = self.random_number()
                tree = ET.parse(self.file_name)
                root = tree.getroot()
                for num in root.findall('number'):                    
                    if num.text == str(random_num):
                        self.rq_text.delete(1.0, tk.END)
                        self.ra_text.delete(1.0, tk.END)
                        self.rd_num.set(num.text)
                        self.rq_text.insert(1.0, num.find('question').text)
            except AttributeError: # no file opened
                self.rq_text.delete(1.0, tk.END)
                self.rq_text.insert(1.0, 'hey dummy, open a file first')
            except StopIteration: # no more objects in the generator
                self.rq_text.delete(1.0, tk.END)
                self.ra_text.delete(1.0, tk.END)
                self.rq_text.insert(1.0, 'You have reached the end of the file')
            
    def build(self, number, question, answer):
        ''' build an xml object and return it to the caller '''
        top = ET.Element('number')
        top.text = number
        quest = ET.SubElement(top, 'question')
        quest.text = question
        ans = ET.SubElement(top, 'answer')
        ans.text = answer
        return top
    
    def give_up(self):
        ''' Give up and display the answer for the viewed question '''
        self.ra_text.delete(1.0, tk.END)
        try:
            for node in self.root:
                if node.text == self.rd_num.get():
                    self.ra_text.insert(1.0, node.find('answer').text)
        except AttributeError: # no file opened
            self.rq_text.delete(1.0, tk.END)
            self.rq_text.insert(1.0, 'hey dummy, open a file first')
            
    def focus_next_window(self, event):
        ''' Aids in tabbing around the program '''
        event.widget.tk_focusNext().focus()
        return 'break'

    def right_click(self, event):
        ''' right click context menu for all Tk Entry and Text widgets '''

        try:
            def rclick_copy(event, apnd=0):
                event.widget.event_generate('<Control-c>')
    
            def rclick_cut(event):
                event.widget.event_generate('<Control-x>')
    
            def rclick_paste(event):
                event.widget.event_generate('<Control-v>')
    
            event.widget.focus()
    
            nclst=[
                   (' Cut', lambda event=event: rclick_copy(event)),
                   (' Copy', lambda event=event: rclick_cut(event)),
                   (' Paste', lambda event=event: rclick_paste(event)),
                   ]
    
            rmenu = tk.Menu(None, tearoff=0, takefocus=0)
    
            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)
    
            rmenu.tk_popup(event.x_root+40, event.y_root+10, entry='0')
    
        except tk.TclError:
            pass
    
        return 'break'


    def right_click_binder(self, rclk):
    
        try:
            for box in [ 'Text', 'Entry', 'Listbox', 'Label']: #
                rclk.bind_class(box, sequence='<Button-3>',
                             func=self.right_click, add='')
        except tk.TclError:
            pass
        
    def help_page(self):
        help_root = tk.Toplevel()
        help_root.title('Help Page')
        
        help_panel = tk.Frame(help_root, name='creation')
        help_panel.pack(side='top', fill='both', expand='y')
        
        notebook = ttk.Notebook(help_panel, name='notebook')
        notebook.enable_traversal()
        notebook.pack(fill='both', expand='y', padx=2, pady=3)
        
        create_tab = ttk.Frame(notebook, name='create')
        create_msg = ''' This is the creation message '''
        create_label = ttk.Label(create_tab, wraplength='4i', justify=tk.LEFT,
                                 anchor=tk.N, text=create_msg)
        
        create_label.grid(row=0, column=0, columnspan=2, sticky='new', pady=5)
        create_tab.rowconfigure(1, weight=1)
        create_tab.columnconfigure((0,1), weight=1, uniform=1)
        
        reader_tab = ttk.Frame(notebook, name='read')
        reader_msg = '''This is a slightly longer reader message that will 
        concern all of my followers for years to come.  Are you still paying 
        attention?'''
        reader_label = ttk.Label(reader_tab, wraplength='4i', justify=tk.LEFT,
                                 anchor=tk.N, text=reader_msg)
        reader_label.grid(row=0, column=0, columnspan=2, sticky='new', pady=5)
        reader_tab.rowconfigure(1, weight=1)
        reader_tab.columnconfigure((0,1), weight=1, uniform=1)
        
        comp_tab = ttk.Frame(notebook, name='compare')
        comp_msg = '''This is a slightly longer reader message that will 
        concern all of my followers for years to come.  Are you still paying 
        attention?'''
        comp_label = ttk.Label(comp_tab, wraplength='4i', justify=tk.LEFT,
                                 anchor=tk.N, text=comp_msg)
        reader_label.grid(row=0, column=0, columnspan=2, sticky='new', pady=5)
        reader_tab.rowconfigure(1, weight=1)
        reader_tab.columnconfigure((0,1), weight=1, uniform=1)

        notebook.add(create_tab, text='Creation Station', underline=0, padding=2)
        notebook.add(reader_tab, text='Reader', underline=0, padding=2)
        notebook.add(comp_tab, text='Compare', underline=0, padding=2)
        
        dismiss_button = ttk.Button(help_root, text='Okay', 
                                    command=help_root.destroy)
        dismiss_button.pack()

def main():
    root = tk.Tk()
    app = FlashCard(root)
    root.mainloop()

if __name__ == '__main__':
    main()
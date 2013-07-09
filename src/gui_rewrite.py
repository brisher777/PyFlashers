import Tkinter as tk
from tkFont import Font
import ttk
import shelve
from tkFileDialog import askopenfilename, asksaveasfilename
from random import randrange
from re import sub, split

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
        
        self.RECORDSDICT = {}
        self.QUESTION = 0 #enhance readability for shelve access
        self.ANSWER = 1 #enhance readability for shelve access
        self.MAX_KEYS = 0
        self.IS_RANDOM = tk.BooleanVar()
        self.RANDOMS = []
        
        #define names for most widgets used in the GUI; used to facilitate looping init's
        menu_names = ('Menu Bar', 'File Menu', 'Help Menu')
        read_buttons = ('Go To', 'Next', 'Give Up', 'Compare')
        create_buttons = ('Go To', 'Next')
        frame_names = ('Tab Bar', 'Create Tab', 'Read Tab', 'Question Frame', 'Answer Frame')
        entry_names = ('Creator Index', 'Reader Index')
        text_names = ('Create Questions', 'Create Answers', 'Read Questions', 'Read Answers')
        
        #initialize dictionaries
        menus, notebooks, entries, self.vars, self.texts, labels, checks = {}, {}, {}, {}, {}, {}, {}
        buttons, frames = {'Readers': {}, 'Creators': {}}, {'Readers': {}, 'Creators': {}}
        
        # part of entry validation for the number display
        self.valid_command = (self.register(self.validate), '%d', '%i', '%P', \
                         '%s', '%S', '%v', '%V', '%W')
        
        #make things beautimous
        self.style.theme_use('default')
        self.style.configure('Blue.TFrame', background='blue')
        self.style.configure('Blue.TNotebook', background='blue')
        self.style.configure('Blue.TButton', foreground='yellow',
                             font=self.default_font)
        self.style.configure('Blue.TNotebook.Tab', background='blue', 
                             font=self.label_font, foreground='yellow')
        self.style.configure('Blue.TCheckbutton', font=self.label_font, 
                             foreground='yellow')
        self.style.configure('Blue.TLabel', font=self.custom_font,
                             foreground='yellow', background='blue')
        self.style.map('Blue.TButton', background= [("active", "skyblue"),
                                                    ("!disabled", "blue")])
        self.style.map('Blue.TNotebook.Tab', background= [("active", "skyblue"),
                                                          ("!disabled", "blue")])
        self.style.map('Blue.TCheckbutton', background=[("active", "skyblue"),
                                                          ("!disabled", "blue")],
                                            indicatorcolor=[('selected', 'skyblue')])
        
        #name of program
        self.parent.title('PyFlashers')
        
        #populate dictionaries with menu objects
        for obj in menu_names:
            menu = tk.Menu(bg='dark blue', foreground='yellow', font=self.default_font,
                           activebackground='skyblue')
            menus[obj] = menu
        
        #build the dropdowns of each menu
        self.parent.config(menu=menus['Menu Bar'])
        menus['File Menu'].add_command(label='Open', command=self.open)
        menus['File Menu'].add_command(label='Save As...', command=self.save_as)
        menus['Help Menu'].add_command(label='OMG Help!', command=self.help_page)
        menus['Menu Bar'].add_cascade(label='File', menu=menus['File Menu'])
        menus['Menu Bar'].add_cascade(label='Help', menu=menus['Help Menu'])

        #populate dictionaries with frame and notebook objects
        for (i, obj) in enumerate(frame_names):
            if i == 0:
                frame = ttk.Frame(style='Blue.TFrame')
                frames['Creators'][obj] = frame
                notebooks['Notebook'] = ttk.Notebook(frames['Creators']['Tab Bar'], style='Blue.TNotebook')
                notebooks['Notebook'].enable_traversal()
                notebooks['Notebook'].pack(in_=frames['Creators']['Tab Bar'], fill='both',
                                           expand='y', padx=2, pady=3)
            elif i == 1 or i == 2:
                frame = ttk.Frame(notebooks['Notebook'], style='Blue.TFrame')
            elif i == 3 or i == 4:
                frame = ttk.Frame(frames['Creators']['Create Tab'], style='Blue.TFrame')
                frame2 = ttk.Frame(frames['Creators']['Read Tab'], style='Blue.TFrame')
                frames['Readers'][obj] = frame2
            frames['Creators'][obj] = frame
        
        #designate position of frames in each notebook tab
        frames['Creators']['Answer Frame'].grid(row=3, column=0, columnspan=3, sticky='news')
        frames['Creators']['Question Frame'].grid(row=1, column=0, columnspan=3, sticky='news')
        frames['Readers']['Answer Frame'].grid(row=3, column=0, columnspan=3, sticky='news')
        frames['Readers']['Question Frame'].grid(row=1, column=0, columnspan=3, sticky='news')
        
        #populate dictionaries with button objects
        for (i, obj) in enumerate(create_buttons):
            button = ttk.Button(frames['Creators']['Create Tab'], text=obj, style='Blue.TButton')
            if i == 0:
                button.grid(row=0, column=i, sticky='news')
            else:
                button.grid(row=0, column=i+1, sticky='news')
            buttons['Creators'][obj] = button
            
        for (i, obj) in enumerate(read_buttons):
            button = ttk.Button(frames['Creators']['Read Tab'], text=obj, style='Blue.TButton')
            buttons['Readers'][obj] = button
            
        buttons['Creators']['Next'].config(command=self.create_next)
        buttons['Creators']['Go To'].config(command=self.create_goto)
        
        buttons['Readers']['Next'].config(command=self.read_next)
        buttons['Readers']['Go To'].config(command=self.read_goto)
        buttons['Readers']['Give Up'].config(command=self.give_up)
        buttons['Readers']['Compare'].config(command=self.compare)
        
            
        buttons['Readers']['Give Up'].grid(row=2, column=0, sticky='news')
        buttons['Readers']['Compare'].grid(row=2, column=2, sticky='news')
        buttons['Readers']['Next'].grid(row=0, column=2, sticky='news')
        buttons['Readers']['Go To'].grid(row=0, column=0, sticky='news')
            
        
        #int variables for indexing
        self.vars['Create Number'] = tk.IntVar()
        self.vars['Create Number'].set(1)
        self.vars['Read Number'] = tk.IntVar()
        self.vars['Read Number'].set(0)
        
        for obj in entry_names:
            if 'Creator' in obj:
                entry = tk.Entry(frames['Creators']['Create Tab'], textvariable=self.vars['Create Number'])
            else:
                entry = tk.Entry(frames['Creators']['Read Tab'], textvariable=self.vars['Read Number'])
            entry.config(bd=5, relief='sunken', foreground='dark blue', width=8,
                         justify='center', validate='key', vcmd=self.valid_command)
            entries[obj] = entry
            entries[obj].grid(row=0, column=1, sticky='ew')
        
        #dole out text objects for each question and answer frame
        for obj in text_names:
            if 'Create' in obj:
                if 'Questions' in obj:
                    text = tk.Text(frames['Creators']['Question Frame'])
                    text.pack(in_=frames['Creators']['Question Frame'])
                else:
                    text = tk.Text(frames['Creators']['Answer Frame'])
                    text.pack(in_=frames['Creators']['Answer Frame'])
            elif 'Read' in obj:
                if 'Questions' in obj:
                    text = tk.Text(frames['Readers']['Question Frame'])
                    text.pack(in_=frames['Readers']['Question Frame'])
                else:
                    text = tk.Text(frames['Readers']['Answer Frame'])
                    text.pack(in_=frames['Readers']['Answer Frame'])
            self.texts[obj] = text
            self.texts[obj].config(height=7, wrap='word', width=45, bg='white', bd=2,
                              highlightthickness=0, font=self.custom_font)
            self.texts[obj].bind('<Tab>', self.focus_next_window)
            self.texts[obj].bind('<Button-3>', self.right_click, add='')
            
        #PyFlashers label insert
        labels['Py Label'] = tk.Label(frames['Creators']['Create Tab'], text='PyFlashers', 
                                      bg='blue', font=('URW Chancery L', 21), 
                                      foreground='yellow')
        labels['Py Label'].grid(row=2, column=1)
            
        #Checkbutton to toggle randomness of reader 
        checks['Random'] = ttk.Checkbutton(frames['Creators']['Read Tab'], 
                                           text='Randomize', style='Blue.TCheckbutton',
                                           variable=self.IS_RANDOM)
        checks['Random'].grid(row=2, column=1)
        
        #add the completed notebook tabs to the notebook
        notebooks['Notebook'].add(frames['Creators']['Create Tab'], text='Creation Station')
        notebooks['Notebook'].add(frames['Creators']['Read Tab'], text='Reader')
        frames['Creators']['Tab Bar'].pack()
        
    ''' logic functions incoming '''    
    def create_next(self):
        ''' cycles the index to the next logical entry and sends Q&A's to the database'''
        
        number = self.vars['Create Number'].get()
        try:
            self.MAX_KEYS = max(self.RECORDSDICT.keys())
        except ValueError:
            pass #suppress error on first entry
        question = self.texts['Create Questions'].get(1.0, tk.END)
        answer = self.texts['Create Answers'].get(1.0, tk.END)
        if number >= self.MAX_KEYS:
            self.vars['Create Number'].set(number + 1)
            self.RECORDSDICT[number] = (question, answer)
        else:
            self.vars['Create Number'].set(self.MAX_KEYS + 2)
            self.RECORDSDICT[self.MAX_KEYS + 1] = (question, answer)
                    
        self.texts['Create Questions'].delete(1.0, tk.END)
        self.texts['Create Answers'].delete(1.0, tk.END)
        
    def read_next(self):
        ''' cycles the index to the next numerical entry in the opened database '''
        
        number = self.vars['Read Number'].get()
        self.texts['Read Questions'].delete(1.0, tk.END)
        self.texts['Read Answers'].delete(1.0, tk.END)
        if self.IS_RANDOM.get() == 1:
            random_num = randrange(1, len(self.db['records']) + 1, 1)
            try:
                if random_num not in self.RANDOMS:
                    self.RANDOMS.append(random_num)
                    self.vars['Read Number'].set(random_num)
                    self.texts['Read Questions'].insert(1.0, self.db['records'][random_num][self.QUESTION])
                else: #force recursion runtime error to denote end of file
                    self.read_next()
            except RuntimeError:
                    self.texts['Read Questions'].insert(1.0, 'You have reached the end of the file.')
        else:
            try:
                self.texts['Read Questions'].insert(1.0, self.db['records'][number + 1][self.QUESTION])
                self.vars['Read Number'].set(number + 1)
            except AttributeError: #no file opened
                self.texts['Read Questions'].insert(1.0, 'Hey Dummy, Open a file first.')
            except KeyError:
                self.texts['Read Questions'].insert(1.0, 'You have reached the end of the file.')
        
    def create_goto(self):
        ''' specify which entry to jump to in the creation workspace '''
        
        try:
            number = self.vars['Create Number'].get()
            self.texts['Create Questions'].delete(1.0, tk.END)
            self.texts['Create Answers'].delete(1.0, tk.END)
            self.texts['Create Questions'].insert(1.0, self.RECORDSDICT[number][self.QUESTION])
            self.texts['Create Answers'].insert(1.0, self.RECORDSDICT[number][self.ANSWER])
        except KeyError:
            self.texts['Create Questions'].delete(1.0, tk.END)
            self.texts['Create Answers'].delete(1.0, tk.END)
            self.texts['Create Questions'].insert(1.0, 'That number doesn\'t exist in the database')
    
    def read_goto(self):
        ''' specify which entry to jump to in the review workspace '''
        
        self.texts['Read Questions'].delete(1.0, tk.END)
        self.texts['Read Answers'].delete(1.0, tk.END)
        try:
            number = self.vars['Read Number'].get()
            self.texts['Read Questions'].insert(1.0, self.db['records'][number][self.QUESTION])
        except KeyError:
            self.texts['Read Questions'].insert(1.0, 'That number doesn\'t exist in the database')
        except AttributeError:
            self.texts['Read Questions'].insert(1.0, 'Hey Dummy, Open a file first.')
    
    def give_up(self):
        ''' Give up and display the answer for the viewed question '''
        
        self.texts['Read Answers'].delete(1.0, tk.END)
        try:
            number = self.vars['Read Number'].get()
            self.texts['Read Answers'].insert(1.0, self.db['records'][number][self.ANSWER])
        except KeyError:
            self.texts['Read Answers'].insert(1.0, 'That number doesn\'t exist in the database')
        except AttributeError:
            self.texts['Read Answers'].insert(1.0, 'Hey Dummy, Open a file first.')
            
    def compare(self):
        ''' Compares answers given to those in the database '''
        
        counter = 0
        number = self.vars['Read Number'].get()
        user_answer = self.texts['Read Answers'].get(1.0, tk.END)
        user_answer = sub('[ ,\n().]', ' ', user_answer)
        user_answer = sub(' +', ' ', user_answer).strip()
        self.texts['Read Answers'].delete(1.0, tk.END)
        
        try:
            orig_answer = sub('[ ,\n().]', ' ', self.db['records'][number][self.ANSWER].lower())
            orig_answer = sub(' +', ' ', orig_answer).strip()
            if user_answer == orig_answer:
                self.texts['Read Answers'].insert(1.0, 'Who\'s awesome? You\'re awesome!')
                counter += 1
            else:
                for orig_word in split('\W+', orig_answer):
                    for ans_word in split('\W+', user_answer):
                        if orig_word == ans_word:
                            self.texts['Read Answers'].insert(tk.END, orig_word + ' ')
                            counter += 1
                            break
                    if orig_word != ans_word:
                        self.texts['Read Answers'].insert(tk.END, ('_' * len(orig_word) + ' '))
            if counter == 0:
                self.texts['Read Answers'].insert(tk.END, 'You were completely wrong, suck less next time.')
            return 'break'
        except AttributeError:
            self.texts['Read Answers'].insert(1.0, 'Hey Dummy, Open a file first.')
    
    def save_as(self):
        ''' Saves a file in a shelve database that the program can use later '''        
        
        file_name = asksaveasfilename(parent=self,
                                      title='Save the file as...',
                                      filetypes=[('all files', '.*')])
        
        if file_name:
            db = shelve.open('%s' % file_name)
            db['records'] = self.RECORDSDICT
            db.close()
    
    def open(self):
        ''' opens a file for use by the program '''
        
        file_name = askopenfilename(parent=self, title='Open file...')
        self.db = shelve.open('%s' % file_name)
        
    ''' helper functions incoming '''  
    def validate(self, action, index, value_if_allowed, prior_value, text, 
                 validation_type, trigger_type, widget_name):
        '''limit input to the number field to 3 digits'''
        return text in '0123456789' and len(value_if_allowed) < 4
    
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
            nclst=[(' Cut', lambda event=event: rclick_copy(event)),
                   (' Copy', lambda event=event: rclick_cut(event)),
                   (' Paste', lambda event=event: rclick_paste(event))]
    
            rmenu = tk.Menu(None, tearoff=0, takefocus=0)
    
            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)
    
            rmenu.tk_popup(event.x_root+40, event.y_root+10, entry='0')
    
        except tk.TclError:
            pass
    
        return 'break'

    def right_click_binder(self, rclk):
        ''' event handler for right clicking inside the gui '''
        
        try:
            for box in [ 'Text', 'Entry', 'Listbox', 'Label']: #
                rclk.bind_class(box, sequence='<Button-3>',
                             func=self.right_click, add='')
        except tk.TclError:
            pass
        
    def help_page(self):
        ''' builds a helpful interface '''
        
        help_root = tk.Toplevel(background='dark blue')
        help_root.title('Help Page')
        
        frame_names = ('Panel', 'Create', 'Read', 'Compare')
        frames, labels = {}, {}
        
        for (i, obj) in enumerate(frame_names):
            if i == 0:
                frame = ttk.Frame(help_root, style='Blue.TFrame')
                frame.pack(side='top', fill='both', expand='y')
                notebook = ttk.Notebook(frame, style='Blue.TNotebook')
                notebook.enable_traversal()
                notebook.pack(fill='both', expand='y', padx=2, pady=3)
            else:
                frame = ttk.Frame(notebook, style='Blue.TFrame')
                frame.rowconfigure(1, weight=1)
                frame.columnconfigure((0,1), weight=1, uniform=1)
            frames[obj] = frame

        create_msg = '''The Creation Station allows you to enter questions and \
answers into the text fields and save each one sequentially by hitting the next \
button.  Save the entries with File->Save As drop down menu. '''
            
        read_msg = '''The Reader workspace is for reviewing an opened file of \
question/answer entries.  The Randomizer feature will randomize review questions. \
The default behavior is to cycle through sequentially.  Giving up will show the \
complete answer.'''            
            
        comp_msg = '''The Compare button checks to see if the answer is \
completely right.  If the answer is only partially correct, it will cycle through \
and display all the correct words that were entered, then insert blank lines \
where words were missed.  This can be repeated until the answer is completely right.'''            
            
        for obj in frames:
            if obj != 'Panel':
                label = ttk.Label(frames[obj], wraplength='4i', justify=tk.LEFT,
                                  anchor=tk.N, style='Blue.TLabel')
                label.grid(row=0, column=0, columnspan=2, sticky='new', pady=5)
                labels[obj] = label
        labels['Create'].config(text=create_msg)
        labels['Read'].config(text=read_msg)
        labels['Compare'].config(text=comp_msg)
        
        for obj in frame_names:
            if obj != 'Panel':
                notebook.add(frames[obj], text=obj, underline=0, padding=2)
        
        dismiss_button = ttk.Button(help_root, text='Okay', style='Blue.TButton', 
                                    command=help_root.destroy)
        dismiss_button.pack() 

if __name__ == '__main__':
    root = tk.Tk()
    FlashCard(root).mainloop()
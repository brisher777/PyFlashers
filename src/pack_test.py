'''
Created on May 22, 2013

@author: ben
'''
from tk import Tk, Frame, Menu
import tkFileDialog

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Simple menu")
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=self.onExit)
        
        menubar.add_cascade(label="File", menu=fileMenu)
        

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

    def onExit(self):
        self.quit()

def main():
  
    root = Tk()
    root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
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

def build(number, question, answer):
        
    ## build an xml object and return it
    ## to the caller
    top = ET.Element('number')
    top.text = number
    quest = ET.SubElement(top, 'question')
    quest.text = question
    ans = ET.SubElement(top, 'answer')
    ans.text = answer
    return top

lists = []
lists.append(build('11110', '1stuffdsafdsaf', '1anfdsafsafr'))
lists.append(build('21110', '2stuffdsafdsaf', '2anfdsafsafr'))
lists.append(build('31110', '3stuffdsafdsaf', '3anfdsafsafr'))
lists.append(build('41110', '4stuffdsafdsaf', '4anfdsafsafr'))
lists.append(build('551110', '5stuffdsafdsaf', '5anfdsafsafr'))
lists.append(build('61110', '6stuffdsafdsaf', '6anfdsafsafr'))
lists.append(build('711110', '7stuffdsafdsaf', '7anfdsafsafr'))


print lists
for i in lists:
    print ET.tostring(i)
'''
Created on May 18, 2013

@author: ben
-- ask the user for input, possibly a GUI, more easily a file --
-- print out a template at the beginning of each run and direct the user to it? -- 
-- build a dictionary, question as the key, answer as the item -- 
-- for user input, you could read the last char of their input and replace it with a question mark if it's not a question mark --
'''

import xml.etree.ElementTree as ET

## get user input
auto_number = 2
user_question = 'What is the square root of 3'
user_answer = '9'

## build an xml file
top = ET.Element('data')
num = ET.SubElement(top, 'number')
num.text = '1'
quest = ET.SubElement(num, 'question')
quest.text = user_question
ans = ET.SubElement(num, 'answer')
ans.text = user_answer

## write to disk
f = open('xml_test.xml', 'w')
f.write('<?xml version="1.0"?>\n')
f.write(ET.tostring(top))
f.flush()
f.close()

## read file 
## implement random generation of question
tree = ET.parse('xml_test.xml')
root = tree.getroot()

for number in root.findall('number'):
    question = number.find('question').text
    answer = number.find('answer').text
    #print question + '\n' + answer
'''
Created on May 18, 2013

@author: ben
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
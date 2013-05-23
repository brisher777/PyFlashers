'''
Created on May 18, 2013

@author: ben
'''

import xml.etree.ElementTree as ET

## PyFlasher takes a file object as first parameter
## the parameter can be NULL if there's only file creation
class PyFlasher():
    def __init__(self, data):
        self.data = data
        
        
    
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
        
    def write_xml(self, obj_list):
        
        ## write to disk
        f = open('xml_test.xml', 'w')
        f.write('<?xml version="1.0"?>\n')
        f.write('<data>')
        for top in obj_list:
            f.write(ET.tostring(top))
        f.write('</data>')
        f.flush()
        f.close()

    def read_xml(self):
        ## read file 
        ## implement random generation of question
        #tree = ET.parse('xml_test.xml')
        #root = tree.getroot()
        self.tree = ET.parse(self.data)
        self.root = self.tree.getroot()
        for number in self.root.findall('number'):
            question = number.find('question').text
            answer = number.find('answer').text
            print question + '\n' + answer
    
    def check_answer(self):
        pass
        ## this will be for answer comparison
        


monkey = PyFlasher("NULL")
print 'making an empty list'
print '==========================================================='
my_list = []
print 'building a few xml objects'
print '==========================================================='
obj_0 = monkey.build('09', 'is this radio good?', 'meh')
obj_1 = monkey.build('10', 'am i cool', 'yes')
obj_2 = monkey.build('11', 'stuff', 'more stuff')
obj_3 = monkey.build('12', 'question', 'answer')
print 'appending objects to list'
print '==========================================================='
my_list.append(obj_0)
my_list.append(obj_1)
my_list.append(obj_2)
my_list.append(obj_3)
print 'passing list of objects to write function for file creation'
print '==========================================================='
monkey.write_xml(my_list)

'''
for number in root.findall('number'):
    question = number.find('question').text
    answer = number.find('answer').text
    #print question + '\n' + answer
'''
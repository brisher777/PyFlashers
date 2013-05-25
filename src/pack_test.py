'''
Created on May 22, 2013

@author: ben
'''

import tkFileDialog
import xml.etree.ElementTree as ET

def read_xml(data):
    ## read file 
    ## implement random generation of question
    #tree = ET.parse('xml_test.xml')
    #root = tree.getroot()
    list = []
    tree = ET.parse(data)
    root = tree.getroot()
    for number in root.findall('number'):
        question = number.find('question').text
        answer = number.find('answer').text
        yield number.text, question, answer

        
f = open('xml_test.xml', 'r')
data = read_xml(f)

print data.next()
print data.next()
print data.next()
print data.next()
print data.next()

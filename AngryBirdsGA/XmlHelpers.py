import xml.etree.ElementTree as ET
from AngryBirdsGA import *

def initXMLLevel():
    """ Returns a list of strings containing the structure of the XML Level definition """
    root = ET.Element("Level")
    tree = ET.ElementTree(root)
    root.set('width', '2')

    camera = ET.SubElement(root, 'Camera')

    birds = ET.SubElement(root, 'Birds')
    ET.SubElement(birds, 'Bird').set('type', 'BirdRed')
    ET.SubElement(birds, 'Bird').set('type', 'BirdBlack')
    ET.SubElement(birds, 'Bird').set('type', 'BirdWhite')

    slingshot = ET.SubElement(root, 'Slingshot')
    slingshot.set('x', '-5')
    slingshot.set('y', '-2.5')

    gameObject = ET.SubElement(root, 'GameObjects')

    s_xml = ET.tostring(root, encoding='unicode', method='xml')
    return s_xml.replace('>', '>\n')

def writeXML(individual, filename):
    """ Writes the XML level representation of individual to the filename"""
    #filename = "file:/home/itt-mcc/Pictures/Untitled-2.png"
    global STRING_XML
    if STRING_XML == "":
        STRING_XML = initXMLLevel()

    
    f = open(filename, "w")
    index = STRING_XML.find('Camera')
    final_xml = []
    final_xml.append('<?xml version="1.0" encoding ="utf-8"?>')
    final_xml.append(STRING_XML[:index + len('Camera')])
    final_xml.append(' x="0" y="0" minWidth="20" maxWidth="25" ')
    prev_index = index + len('Camera')
    index = STRING_XML.find('GameObjects')
    final_xml.append(STRING_XML[prev_index:index + len('GameObjects')])
    final_xml.append('>\n')
    i = 0
    el_width = 0
    el_height = -350
    el_height_cont = 0

    # From this point it generates the XML string by reading the
    # values for each individual
    for item in individual:
        base_x = item[1]
        base_x = 0
        base_y = item[2]
        base_y = 0
        for element in item[0]:
            if len(element) <= 2:
                el_width = element[1]
                el_height = el_height + (element[0]/2)
                el_height_cont = element[0]/2
            else: 
                #print(element)
                x_val = (element[2] + base_x)/100
                y_val = (element[3] + base_y + el_height)/100
                final_xml.append('<Block' + 
                                ' type="' + element[0] + '"' +
                                ' material="' + element[1] + '"' +
                                ' x="' + str(x_val) + '"' +
                                ' y="' + str(y_val) + '"' +
                                ' rotation="' + str(element[4]) + '"' +
                                ' id="' + str(i) + '"/>\n')
                i+=1
            # End if
        el_height = el_height + el_height_cont
    
    final_xml.append('</GameObjects>\n')
    final_xml.append(STRING_XML[index + len('<GameObjects\>'):])

    f.write(''.join(final_xml))

    f.close()
    score = el_height
    return el_height
import xml.etree.ElementTree as ET
from xml.dom import minidom
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
    STRING_XML = ""

    if STRING_XML == "":
        STRING_XML = initXMLLevel()

    f = open(filename, "w+")
    index = STRING_XML.find('Camera')
    final_xml = []
    final_list = []
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
    #print(individual)
    #print(individual)
    for item in individual:
        #print(item)
        #print("item 0")
        base_x = item[0][0][0]
        #base_x = 0
        print(item[0][0][0])
        base_y = item[0][0][1]
        #base_y = 0
        #print(item[1])
        for element in item:
            #print(element)
            #print("elemrnt 1")
            for obj in element:
                #print(obj)
                #print("obj 2")
                if len(obj) <= 2:
                    el_width = obj[0]
                    el_height = el_height + (obj[1]/2)
                    el_height_cont = obj[1]/2
                else: 
                    x_val = (obj[2] + base_x)/100
                    y_val = (obj[3] + base_y + el_height)/100
                    final_xml.append('<Block' + 
                                    ' type="' + obj[0] + '"' +
                                    ' material="' + obj[1] + '"' +
                                    ' x="' + str(x_val) + '"' +
                                    ' y="' + str(y_val) + '"' +
                                    ' rotation="' + str(obj[4]) + '"' +
                                    ' id="' + str(i) + '"/>\n')
                    final_list.append([obj[0], obj[1], str(x_val), str(y_val), str(obj[4]), str(i)])
                    i+=1
            # End if
        el_height = el_height + el_height_cont
    
    final_xml.append('</GameObjects>\n')
    final_xml.append(STRING_XML[index + len('<GameObjects\>'):])

    f.write(''.join(final_xml))

    f.close()
    el_height = el_height + 350
    return [el_height, i+1, final_list]

def readXML(filename):
    # Reads the entire file
    xmldoc = minidom.parse(filename)

    # Gets all the elements in the file that have the BLOCK tag
    item_list = xmldoc.getElementsByTagName('Block')

    final_list = [[Objeto.getAttribute('type'), Objeto.getAttribute('material'), Objeto.getAttribute('x'), Objeto.getAttribute('y'), Objeto.getAttribute('rotation'), Objeto.getAttribute('id')] for Objeto in item_list]
    
    #final_list = [Dic.type.value, Dic.material.value, Dic.x.value, Dic.y.value, Dic.rotation.value] in Dic for Piece.__attrs  in item_list
    # Prints the lenght of the array of pieces
    #print(len(item_list))

    # Prints the type of each piece in the file
    for s in item_list:
        pass
        #print(s.attributes['type'].value)

    return final_list

def calculate_mask(individual, mask):
    # 
    # First
    temp_individual = individual.copy()
    height_list = []
    new_x_list = []
    x = 750
    el_height = -350
    el_height_cont = 0
    cumulative_height = 0
    print(individual)
    for item in individual:
        for element in item:
            for obj in element:
                if len(obj) <= 2:
                    height_list.append(obj[1])

    print(height_list)

    for j in range(6, -1, -1):
        for i in range(2, -1, -1):
            print(mask[i][j])
            # set x value to the column value
            # get a piece and place it
            
            while cumulative_height <= (mask[i][j] * 150):
                # while the height of the current column is less than an estimated value continue adding pieces
                print(height_list[0])
                print(height_list)
                cumulative_height += height_list[0]
                new_x_list.append(x)
                el_height = el_height + (height_list[0]/2)
                el_height_cont = height_list[0]/2
                height_list.pop(0)
            
            #print("Line break")
            
            # Check if the next line requires adding pieces
            if mask[i-1][j] == 0 or (i-1)==-1:
                # reset the height value
                x += -250
                print(cumulative_height)
                print(height_list[0])
                cumulative_height = 0
                print("-----< Column break >-----")
                # Exit current iteration
                break
    for r in range(0, len(height_list)):
        new_x_list.append(9999)
    print("----< Re-Write Individual >----")

    print(new_x_list)   
    c = 0         

    for i in range(len(new_x_list)):
        temp_individual[i][0][0][0] = new_x_list[i]
        #new_x_list.pop(0)
    #print(temp_individual[0])
    """
    for x in new_x_list:
        temp_individual[c][0][0][0] = x
        print(temp_individual[c][0][0][0])
        print("--------Fin")
        c += 1
    """
    #print(temp_individual)
    """
    for item in individual:
        for element in item:
            for obj in element:
                if len(obj) <= 2:
                    obj[0] = new_x_list[0]
                    height_list.append(obj[1])
                    new_x_list.pop(0)
                    print(obj[0])
    """
    #print(individual)
    return temp_individual

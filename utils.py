import os
# from xml.etree.ElementTree import Element, SubElement, ElementTree
import numpy as np

import xml.etree.ElementTree as ET


def makeXML(Boxes):
    root = ET.Element('annotation')
    ET.SubElement(root, 'filename').text = '수정필요' # filename 수정필요

    #TODO : 인덱스 수정 필요
    for box in Boxes: #per Box
        visible = box[6]
        if visible == False:
            continue

        xmin = box[0]
        ymin = box[1]
        xmax = box[2]
        ymax = box[3]
        string = box[4]
        orientation = box[5]
        symbol_object = ET.SubElement(root, 'symbol_object')
        ET.SubElement(symbol_object, 'type').text = '수정필요' #수정필요
        ET.SubElement(symbol_object, 'class').text = string
        bndbox = ET.SubElement(symbol_object, 'bndbox')
        ET.SubElement(bndbox, 'xmin').text = xmin
        ET.SubElement(bndbox, 'ymin').text = ymin
        ET.SubElement(bndbox, 'xmax').text = xmax
        ET.SubElement(bndbox, 'ymax').text = ymax
        ET.SubElement(symbol_object, 'degree').text = orientation
        ET.SubElement(symbol_object, 'flip').text = 'n' # 수정필요할수도
        ET.SubElement(symbol_object, 'etc').text = None # 수정필요할수도


    tree = ET.ElementTree(root)
    tree.write('test.xml')  # 수정필요


def object_to_element(xml_obj, type):
    if type == 'gt':
        string = xml_obj[1].text
        orientation = int(float(xml_obj[2].text))
        xmin = int(xml_obj[3][0].text)
        ymin = int(xml_obj[3][1].text)
        xmax = int(xml_obj[3][2].text)
        ymax = int(xml_obj[3][3].text)

        return string, orientation, xmin, ymin, xmax, ymax

    elif type == 'res':
        string = xml_obj[0].text
        orientation = int(float(xml_obj[1].text))
        xmin = int(xml_obj[2][0].text)
        ymin = int(xml_obj[2][1].text)
        xmax = int(xml_obj[2][2].text)
        ymax = int(xml_obj[2][3].text)

        return string, orientation, xmin, ymin, xmax, ymax


def parseXML(xml_path, type):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # size = root.find('size')  # GT에만 있음
    # width = int(size.find('width').text)
    # height = int(size.find('height').text)

    result = []

    for child in root.findall('object'):
        visible = True
        string, orientation, xmin, ymin, xmax, ymax = object_to_element(child, type)
        result.append([string, orientation, xmin, ymin, xmax, ymax, visible]) # add Visible

    result = np.array(result) # np array 로 변환

    return result

# for test
# path = r'C:\Users\master\Desktop\PNID_GUI\test_res.xml'
# result = parseXML(path, 'res')
# print(result)



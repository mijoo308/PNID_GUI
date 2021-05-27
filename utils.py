import os
# from xml.etree.ElementTree import Element, SubElement, ElementTree
import numpy as np

import xml.etree.ElementTree as ET


# Result xml 형식 기준
def makeXML(Boxes, filename):
    root = ET.Element('annotation')
    ET.SubElement(root, 'filename').text = filename

    # string, orientation, xmin, ymin, xmax, ymax, visible
    for box in Boxes: #per Box
        visible = box[-1]
        if not visible:
            continue

        string = box[0]
        orientation = box[1]
        xmin = box[2]
        ymin = box[3]
        xmax = box[4]
        ymax = box[5]
        type = box[6]

        symbol_object = ET.SubElement(root, 'symbol_object')
        ET.SubElement(symbol_object, 'type').text = type
        ET.SubElement(symbol_object, 'class').text = string
        bndbox = ET.SubElement(symbol_object, 'bndbox')
        ET.SubElement(bndbox, 'xmin').text = str(xmin)
        ET.SubElement(bndbox, 'ymin').text = str(ymin)
        ET.SubElement(bndbox, 'xmax').text = str(xmax)
        ET.SubElement(bndbox, 'ymax').text = str(ymax)
        ET.SubElement(symbol_object, 'degree').text = str(orientation)
        ET.SubElement(symbol_object, 'flip').text = 'n'
        ET.SubElement(symbol_object, 'etc').text = None

    indent(root)
    tree = ET.ElementTree(root)
    tree.write(filename + '_fixed.xml')


def object_to_element(xml_obj, xml_type):

    bndbox = xml_obj.find("bndbox")

    string = None
    orientation = None
    type = None
    if xml_type == 'gt':
        string = xml_obj.find('string').text
        orientation = int(float(xml_obj.find('orientation').text))
    elif xml_type == 'res':
        string = xml_obj.find('class').text
        orientation = int(float(xml_obj.find('degree').text))
        type = xml_obj.find('type').text

    xmin = int(bndbox[0].text)
    ymin = int(bndbox[1].text)
    xmax = int(bndbox[2].text)
    ymax = int(bndbox[3].text)

    return string, orientation, xmin, ymin, xmax, ymax, type


def parseXML(xml_path, xml_type):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # size = root.find('size')  # GT에만 있음
    # width = int(size.find('width').text)
    # height = int(size.find('height').text)

    result = []
    object = None

    if xml_type == 'gt':
        object = 'object'
    elif xml_type == 'res':
        object = 'symbol_object'

    for child in root.findall(object):
        visible = True
        string, orientation, xmin, ymin, xmax, ymax, type = object_to_element(child, xml_type)
        result.append([string, orientation, xmin, ymin, xmax, ymax, type, visible])  # add Visible

    result = np.array(result)  # np array 로 변환

    return result

def indent(elem, level=0):  # 자료 출처 https://goo.gl/J8VoDK
    """ XML의 들여쓰기 포함한 출력을 위한 함수

    """
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i



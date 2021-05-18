import os
# from xml.etree.ElementTree import Element, SubElement, ElementTree

import xml.etree.ElementTree as ET

def makeXML(drawing_width, drawing_height, txt_root, img_dir):

    width = str(drawing_width)
    height = str(drawing_height)
    depth = '3' #

    txt_list = []
    for file in os.listdir(txt_root):
        if file.endswith("origin_result.txt"):
            txt_list.append(os.path.join(txt_root, file))

    for txt_file in txt_list: #per Drawing
        file_name = str(os.path.basename(txt_file).split('_')[0])
        img_name = file_name + ".jpg"
        # path = os.path.join(folder, img_name)
        xml_txt_path = os.path.join(txt_root, file_name + ".xml")

        root = ET.Element('annotation')

        # basic_drawing_information = SubElement(root, 'basic_drawing_information')
        # SubElement(basic_drawing_information, 'folder').text = folder
        ET.SubElement(root, 'filename').text = img_name
        # SubElement(root, 'path').text = path
        # size = SubElement(root, 'size')
        # SubElement(size, 'width').text = width
        # SubElement(size, 'height').text = height
        # SubElement(size, 'depth').text = depth

        rf = open(txt_file, 'r', encoding='UTF8')
        lines = rf.readlines()
        rf.close()
        for line in lines: #per Box
            info = line.split('ㅣ')
            xmin = info[0]
            ymin = info[1]
            xmax = info[2]
            ymax = info[3]
            string = info[4]
            orientation = info[5]

            symbol_object = ET.SubElement(root, 'object')
            ET.SubElement(symbol_object, 'string').text = string
            ET.SubElement(symbol_object, 'orientation').text = orientation
            bndbox = ET.SubElement(symbol_object, 'bndbox')
            ET.SubElement(bndbox, 'xmin').text = xmin
            ET.SubElement(bndbox, 'ymin').text = ymin
            ET.SubElement(bndbox, 'xmax').text = xmax
            ET.SubElement(bndbox, 'ymax').text = ymax


        tree = ET.ElementTree(root)
        tree.write(xml_txt_path)


def object_to_element(xml_obj, type):
    if type == 'gt':
        string = xml_obj[1].text
        orientation = xml_obj[2].text
        xmin = int(xml_obj[3][0].text)
        ymin = int(xml_obj[3][1].text)
        xmax = int(xml_obj[3][2].text)
        ymax = int(xml_obj[3][3].text)

        return string, orientation, xmin, ymin, xmax, ymax

    elif type == 'res':
        string = xml_obj[0].text
        orientation = xml_obj[1].text
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
        string, orientation, xmin, ymin, xmax, ymax = object_to_element(child, type)
        result.append([string, orientation, str(xmin), str(ymin), str(xmax), str(ymax)])
    return result

# for test
# path = r'C:\Users\master\Desktop\PNID_GUI\test_res.xml'
# result = parseXML(path, 'res')
# print(result)



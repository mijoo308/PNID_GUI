import cv2
import os
import numpy as np
import PIL
from PIL import ImageDraw, ImageFont, Image
from xml.etree.ElementTree import Element, SubElement, ElementTree

#--------Param from 'run_EasyOCR.py'--------
#
# drawing_path = '' #
sizeForCrop = 0
sizeForStride = 0
#
# result_path = ''
originWidth = 0
originHeight = 0
#---------------------

def resizeBigImg(src):
    resizedImg = src.Image.resize((6622, 4677))
    return resizedImg


def getXposYpos(width, height):
    xPosList = []
    yPosList = []
    xPosList.append(0)
    yPosList.append(0)

    startX = 0
    while 1:
        startX = startX + sizeForStride
        if startX + sizeForCrop > width:
            startX = width - sizeForCrop
            xPosList.append(startX)
            break
        else:
            xPosList.append(startX)

    startY = 0
    while 1:
        startY = startY + sizeForStride
        if startY + sizeForCrop > height:
            startY = height - sizeForCrop
            yPosList.append(startY)
            break
        else:
            yPosList.append(startY)

    return xPosList, yPosList


def make_rotated_img(dirname):
    imgNames_withExt = os.listdir(dirname)  # [S199.jpg, S211-100.jpg, S211-103.jpg]

    already_exist = False

    for imgName_withExt in imgNames_withExt:
        if imgName_withExt.endswith("-rotated.jpg"):
            already_exist = True

    if not already_exist:
        for imgName_withExt in imgNames_withExt:  # S199.jpg
            imgName = os.path.splitext(imgName_withExt)[0]  # S199
            full_img_path = os.path.join(dirname, imgName_withExt)
            rotated_full_img_path = os.path.join(dirname, imgName + "-rotated.jpg")

            drawing = cv2.imread(full_img_path)
            rotated_img = cv2.rotate(drawing, cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite(rotated_full_img_path, rotated_img)


def crop_big_image(result_root, dirname): # drawing_path
    imgNames_withExt = os.listdir(dirname)  # [S199.jpg, S211-100.jpg, S211-103.jpg]
    print(imgNames_withExt)

    already_exist = False

    only_img_list = []
    for imgName_withExt in imgNames_withExt:
        full_img_path = os.path.join(dirname, imgName_withExt)
        if os.path.isdir(full_img_path):
            already_exist = True
        else:
            only_img_list.append(full_img_path)


    if not already_exist:
        for imgName_withExt in imgNames_withExt:  # S199.jpg
            print(imgName_withExt)
            imgName = os.path.splitext(imgName_withExt)[0]  # S199
            full_img_path = os.path.join(dirname, imgName_withExt)

            crop_result_dir = os.path.join(dirname, imgName)  # 해당 도면이름의 dir생성  (crop result 폴더)
            if not os.path.isdir(crop_result_dir):
                os.mkdir(crop_result_dir)

                drawing = cv2.imread(full_img_path)

                # resizedImg = cv2.resize(drawing, dsize=(resizedWidth, resizedHeight))
                cv2.imwrite(os.path.join(result_root, imgName + ".jpg"), drawing)

                # 도면 사이즈 지정하는 게 아니라 도면에 따라 해당 도면의 width height 이용
                drawing_width = drawing.shape[1]
                drawing_height = drawing.shape[0]

                xPosList, yPosList = getXposYpos(drawing_width, drawing_height)

                y_num = 0
                for y in yPosList:
                    x_num = 0
                    for x in xPosList:
                        croppedImg = drawing[y:y + sizeForCrop, x:x + sizeForCrop]
                        save_name = str(imgName) + '_' + str(x_num) + '_' + str(y_num) + '.jpg'
                        cv2.imwrite(os.path.join(crop_result_dir, save_name), croppedImg)
                        x_num += 1
                    y_num += 1
    else:
        for only_img in only_img_list:
            drawing = cv2.imread(only_img)
            imgName = os.path.splitext(os.path.basename(only_img))[0]
            print(imgName)

            cv2.imwrite(os.path.join(result_root, imgName + ".jpg"), drawing)


def merge_result(dir, resultRoot): #per Drawing

    txtNames_withExt = os.listdir(dir)

    img_name = os.path.basename(dir)
    img_name = str(img_name.split('_')[0])
    finalTxtResultPath = os.path.join(resultRoot, img_name + ".txt")
    f_write = open(finalTxtResultPath, 'w')

    full_img_path = os.path.join(resultRoot, img_name + ".jpg")
    drawing = cv2.imread(full_img_path)
    drawing_width = drawing.shape[1]
    drawing_height = drawing.shape[0]


    xPosList, yPosList = getXposYpos(drawing_width, drawing_height)



    for txtName_withExt in txtNames_withExt: # per subDrawing  KNU-A-22300-001-01_0_0.txt
        recognition_txt_path = os.path.join(dir, txtName_withExt)
        txtName = str(txtName_withExt.split('.')[0])  # S199-100_1_1.jpg

        relativeXpos = int(txtName.split('_')[1])
        # print("relativeXPos" + str(relativeXpos))
        relativeYpos = int(txtName.split('_')[2])
        # print("relativeYPos" + str(relativeYpos))

        subDrawingL = xPosList[relativeXpos]
        subDrawingT = yPosList[relativeYpos]
        subDrawingR = subDrawingL + sizeForCrop
        subDrawingB = subDrawingT + sizeForCrop

        xPosList_LastIndex = len(xPosList) - 1
        yPosList_LastIndex = len(yPosList) - 1

        case = 0
        rightSideInCommonL = 0
        downSideInCommonT = 0
        if relativeXpos != xPosList_LastIndex and relativeYpos != yPosList_LastIndex:  # 둘다 마지막 아님
            case = 1
            rightSideInCommonL = xPosList[relativeXpos + 1]
            downSideInCommonT = yPosList[relativeYpos + 1]

        elif relativeYpos != yPosList_LastIndex:  # x만 마지막
            case = 2
            downSideInCommonT = yPosList[int(relativeYpos) + 1]

        elif relativeXpos != xPosList_LastIndex:  # y만 마지막
            case = 3
            rightSideInCommonL = xPosList[int(relativeXpos) + 1]

        else:  # 둘 다 마지막
            case = 4

        # print("case: " + str(case))
        craftTessFile = open(recognition_txt_path, 'r')
        lines = craftTessFile.readlines()
        craftTessFile.close()

        for line in lines: #per detection Box
            # draw = ImageDraw.Draw(newImageForMerge)
            parsedBox = line.split('ㅣ')
            relB_xmin = int(parsedBox[0])
            relB_ymin = int(parsedBox[1])
            relB_xmax = int(parsedBox[2])
            relB_ymax = int(parsedBox[3])
            # Tstring = parsedBox[4]

            absB_xmin = subDrawingL + relB_xmin
            absB_ymin = subDrawingT + relB_ymin
            absB_xmax = subDrawingL + relB_xmax
            absB_ymax = subDrawingT + relB_ymax

            if case == 1:  # 둘다 마지막 아님
                # if absB_xmin != subDrawingL and absB_ymin != subDrawingT and absB_xmin < rightSideInCommonL and absB_ymin < downSideInCommonT:
                if subDrawingL + 2 < absB_xmin < rightSideInCommonL and subDrawingT + 2 < absB_ymin < downSideInCommonT:
                    resultData = str(absB_xmin) + "ㅣ" + str(absB_ymin) + "ㅣ" + str(absB_xmax) + "ㅣ" + str(absB_ymax) + "\n"
                    f_write.write(resultData)

            elif case == 2:  # x만 마지막
                # if absB_xmin != subDrawingL and absB_ymin != subDrawingT and absB_ymin < downSideInCommonT:
                if subDrawingL + 2 < absB_xmin and subDrawingT + 2 < absB_ymin < downSideInCommonT:
                    resultData = str(absB_xmin) + "ㅣ" + str(absB_ymin) + "ㅣ" + str(absB_xmax) + "ㅣ" + str(absB_ymax) + "\n"
                    f_write.write(resultData)

            elif case == 3:  # y만 마지막
                # if absB_xmin != subDrawingL and absB_ymin != subDrawingT and absB_xmin < rightSideInCommonL:
                if subDrawingL + 2 < absB_xmin < rightSideInCommonL and subDrawingT + 2 < absB_ymin:
                    resultData = str(absB_xmin) + "ㅣ" + str(absB_ymin) + "ㅣ" + str(absB_xmax) + "ㅣ" + str(absB_ymax) + "\n"
                    f_write.write(resultData)

            elif case == 4:  # 둘다 마지막
                # if absB_xmin != subDrawingL and absB_ymin != subDrawingT:
                if subDrawingL + 2 < absB_xmin and subDrawingT + 2 < absB_ymin:
                    resultData = str(absB_xmin) + "ㅣ" + str(absB_ymin) + "ㅣ" + str(absB_xmax) + "ㅣ" + str(absB_ymax) + "\n"
                    f_write.write(resultData)


    f_write.close()


def return_to_original_size(exceptXpos, exceptYpos, txt_dir, outpath):
    basename = os.path.basename(txt_dir)
    txt_name = str(basename.split('_')[0])
    filename_to_save = os.path.join(outpath, txt_name + "_origin_result.txt")

    f_to_read = open(txt_dir, 'r', encoding='UTF8')
    lines = f_to_read.readlines()
    f_to_read.close()

    f_to_write = open(filename_to_save, 'w', encoding='UTF8')
    for line in lines:
        parsed_box = line.split('ㅣ')
        resized_xmin = int(parsed_box[0])
        resized_ymin = int(parsed_box[1])
        resized_xmax = int(parsed_box[2])
        resized_ymax = int(parsed_box[3])
        Tstring = parsed_box[4]
        orientation = parsed_box[5]
        confidence = parsed_box[6]

        #
        # origin_xmin = int(resized_xmin*3/2)
        # origin_ymin = int(resized_ymin*3/2)
        # origin_xmax = int(resized_xmax*3/2)
        # origin_ymax = int(resized_ymax*3/2)
        #
        origin_xmin = int(resized_xmin)
        origin_ymin = int(resized_ymin)
        origin_xmax = int(resized_xmax)
        origin_ymax = int(resized_ymax)

        if not(origin_xmax > exceptXpos and origin_ymax > exceptYpos):
            data = str(origin_xmin) + "ㅣ" + str(origin_ymin) + "ㅣ" + str(origin_xmax) + "ㅣ" + str(origin_ymax) + "ㅣ" + Tstring + "ㅣ" + orientation + 'ㅣ' + confidence
            f_to_write.write(data)
        # data = str(origin_xmin) + "ㅣ" + str(origin_ymin) + "ㅣ" + str(origin_xmax) + "ㅣ" + str(
        #     origin_ymax) + "ㅣ" + Tstring + "ㅣ" + orientation + 'ㅣ' + confidence
        # f_to_write.write(data)

    f_to_write.close()

def except_selected_pos(txt_dir, outpath, padding=None, info_box=None):
    #
    # pad_xpos = padding[0]
    # pad_ypos = padding[1]
    # info_xpos = info_box[0]
    # info_ypos = info_box[1]

    basename = os.path.basename(txt_dir)
    txt_name = str(basename.split('_')[0])
    filename_to_save = os.path.join(outpath, basename)

    f_to_read = open(txt_dir, 'r', encoding='UTF8')
    lines = f_to_read.readlines()
    f_to_read.close()

    f_to_write = open(filename_to_save, 'w', encoding='UTF8')

    for line in lines:
        parsed_box = line.split('ㅣ')
        xmin = int(parsed_box[0])
        ymin = int(parsed_box[1])
        xmax = int(parsed_box[2])
        ymax = int(parsed_box[3])
        Tstring = parsed_box[4]
        orientation = parsed_box[5]
        confidence = parsed_box[6]

        # if xmin > pad_xpos and ymax < pad_ypos:
        #     if not (xmax > info_xpos and ymax > info_ypos):
        #         if Tstring != "":
        #             data = str(xmin) + "ㅣ" + str(ymin) + "ㅣ" + str(xmax) + "ㅣ" + str(ymax) + "ㅣ" + Tstring + "ㅣ" + orientation + 'ㅣ' + confidence
        #             f_to_write.write(data)

        if Tstring != "":
            data = str(xmin) + "ㅣ" + str(ymin) + "ㅣ" + str(xmax) + "ㅣ" + str(
                ymax) + "ㅣ" + Tstring + "ㅣ" + orientation + 'ㅣ' + confidence
            f_to_write.write(data)

    f_to_write.close()


def makeXML(drawing_width, drawing_height, txt_root, img_dir):

    width = str(drawing_width)
    height = str(drawing_height)
    depth = '3' # ??
    object_type = 'text'
    flip = 'n'
    etc = None
    # folder = os.path.realpath(img_dir)

    txt_list = []
    for file in os.listdir(txt_root):
        if file.endswith("origin_result.txt"):
            txt_list.append(os.path.join(txt_root, file))

    for txt_file in txt_list: #per Drawing
        file_name = str(os.path.basename(txt_file).split('_')[0])
        img_name = file_name + ".jpg"
        # path = os.path.join(folder, img_name)
        xml_txt_path = os.path.join(txt_root, file_name + ".xml")

        root = Element('annotation')

        # basic_drawing_information = SubElement(root, 'basic_drawing_information')
        # SubElement(basic_drawing_information, 'folder').text = folder
        SubElement(root, 'filename').text = img_name
        # SubElement(root, 'path').text = path
        # size = SubElement(root, 'size')
        # SubElement(size, 'width').text = width
        # SubElement(size, 'height').text = height
        # SubElement(size, 'depth').text = depth

        rf = open(txt_file, 'r', encoding='UTF8')
        lines = rf.readlines()
        rf.close()
        id_iter = 0
        for line in lines: #per Box
            info = line.split('ㅣ')
            xmin = info[0]
            ymin = info[1]
            xmax = info[2]
            ymax = info[3]
            string = info[4]
            orientation = info[5]

            # prev ver-----------------------------------------------------------
            symbol_object = SubElement(root, 'object')
            # SubElement(symbol_object, 'type').text = object_type
            SubElement(symbol_object, 'string').text = string
            SubElement(symbol_object, 'orientation').text = orientation

            # recent ver-----------------------------------------------------------
            # symbol_object = SubElement(root, 'symbol_object')
            # SubElement(symbol_object, 'type').text = 'text'
            # SubElement(symbol_object, 'class').text = string
            # SubElement(symbol_object, 'degree').text = orientation
            #----------------------------------------------------------------------


            bndbox = SubElement(symbol_object, 'bndbox')
            SubElement(bndbox, 'xmin').text = xmin
            SubElement(bndbox, 'ymin').text = ymin
            SubElement(bndbox, 'xmax').text = xmax
            SubElement(bndbox, 'ymax').text = ymax

            # recent ver-----------------------------------------------------------
            #SubElement(symbol_object, 'degree').text = orientation
            # SubElement(symbol_object, 'flip').text = flip
            # SubElement(symbol_object, 'etc').text = etc
            # ----------------------------------------------------------------------

            # id_iter += 1

        indent(root)
        tree = ElementTree(root)
        tree.write(xml_txt_path)

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

def IOU_fast(result2_boxes, result2_texts, result1_box, result1_text, iou_threshold): # 결과2의 박스[], 결과1의 박스 하나  # iou_threshold도 parameter로 빼야 함
    '''
        boxes : coordinates of each box
        scores : score of each box
        iou_threshold : iou threshold(box with iou larger than threshold will be removed)
    '''
    result2_boxes = np.array(result2_boxes) # 다른 박스들인 듯
    result1_box = np.array(result1_box) # 현재박스


    if len(result2_boxes) == 0:
        return []

    # transform coordinate to original coordinate
    x1 = result2_boxes[:, 1]
    y1 = originHeight - result2_boxes[:, 2]
    x2 = result2_boxes[:, 3]
    y2 = originHeight - result2_boxes[:, 0]


    bx1 = result1_box[0]
    by1 = result1_box[1]
    bx2 = result1_box[2]
    by2 = result1_box[3]

    # Compute area of each boxes
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    boxarea = (bx2-bx1+1)*(by2-by1+1)

    # With vector implementation, we can calculate fast
    xx1 = np.maximum(x1, bx1) #Score가 가장 높은 박스와 나머지 박스의 좌표 비교
    yy1 = np.maximum(y1, by1)
    xx2 = np.minimum(x2, bx2)
    yy2 = np.minimum(y2, by2)

    w = np.maximum(0, xx2 - xx1 + 1)
    h = np.maximum(0, yy2 - yy1 + 1)
    intersection = w * h

    # Calculate the iou

    iou = intersection / (area + boxarea - intersection)

    boxInd = np.argmax(iou)  #iou가 같은 경우가 있으면?,,

    if iou[boxInd] == 0:
        return None #겹치는 box 없음

    else:
        orientation = 0
        for_debug = iou[boxInd]
        if iou[boxInd] > iou_threshold:
            confidence2 = result2_boxes[boxInd][4]
            confidence1 = result1_box[4]

            if confidence1 > confidence2: # origin result
                data = str(bx1) + 'ㅣ' + str(by1) + 'ㅣ' + str(bx2) + 'ㅣ' + str(by2) + 'ㅣ' + result1_text + 'ㅣ' + str(orientation) + 'ㅣ' + str(confidence1) + '\n'

            else:  # rotated_result
                orientation = 90
                data = str(x1[boxInd]) + 'ㅣ' + str(y1[boxInd]) + 'ㅣ' + str(x2[boxInd]) + 'ㅣ' + str(y2[boxInd]) + 'ㅣ' + result2_texts[boxInd] + 'ㅣ' + str(orientation) + 'ㅣ' + str(confidence2) + '\n'

            return data

        else:
            return None












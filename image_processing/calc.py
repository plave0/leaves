'''Calculations'''
import image_processing.fex as f
import cv2

def calc_rectangularity(image):
    '''Calculates the rectangularity of a leaf.'''

    #Calculates enclosing rectangle area
    _, rect = f.find_rect(image)
    rect_area = rect[1][0] * rect[1][1];
    print(rect_area)

    #Calculate leaf area
    leaf_area = calc_leaf_area(image)
    print(leaf_area)

    #Calculate rectangularity in procentage
    rectangularity = (leaf_area/rect_area) * 100
    print(rectangularity)

def calc_circularity(image):
    '''Calculates the circularity of a leaf.'''

    #Calculates enclosing circle area
    img, circ = f.find_encl(image)
    res = f.resize_image(img, 0.3)
    f.show_image(res)
    circ_area = cv2.contourArea(circ)
    print(circ_area)

    #Calculate leaf area
    leaf_area = calc_leaf_area(image)
    print(leaf_area)

    #Calculate circularity in procentage
    circularity = (leaf_area/circ_area) * 100
    print(circularity)

def calc_leaf_area(image):
    '''Calculates leaf area.'''

    cnt_img, cnt = f.find_cnt(image)
    res = f.resize_image(cnt_img, 0.3)
    f.show_image(res)
    return cv2.contourArea(cnt[0])

def calc_leaf_circumference(image):
    '''Calculates leaf circumference.'''

    cnt_img, _ = f.find_cnt(image)
    gray_image = cv2.cvtColor(cnt_img, cv2.COLOR_BGR2GRAY)
    circumference = cv2.countNonZero(gray_image)
    print(circumference)
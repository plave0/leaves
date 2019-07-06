'''Calculations'''
import image_processing.fex as f
import cv2
import numpy as np
from math import sqrt

def calc_rectangularity(image):
    '''Calculates the rectangularity of a leaf.'''

    #Calculates enclosing rectangle area
    _, rect, _ = f.find_rect(image)
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

def calc_hw_ratio(image):
    '''Calculates height-width ratio of a leaf.'''

    _,rect, _ = f.find_rect(image)
    height = rect[1][0]
    width = rect[1][1]

    print(height/width)

def calc_simetry(image):
    '''Calculates leaf simerty.'''

    _, _, rect_points = f.find_rect(image, keep_original=True)
    middle_points = [] #Array of points that represent the centers of all four sides of the rectangle

    #Calculate middle poitns
    for poin_index in range(len(rect_points)):
        next_point_index = (poin_index + 1)%4
        point1 = rect_points[poin_index]
        point2 = rect_points[next_point_index]

        x = int((point1[0]+point2[0])/2)
        y = int((point1[1]+point2[1])/2)
        middle_point = [x,y]
        middle_points.append(middle_point)
    

    rect, _, _ = f.find_rect(image, keep_original=True)
    for point in middle_points:
        point = tuple(point)
        print(point)
        cv2.circle(rect,point,10,(0,255,0),-1)

    cv2.line(rect,tuple(middle_points[0]), tuple(middle_points[2]),(0,255,0),2)
    cv2.line(rect,tuple(middle_points[1]), tuple(middle_points[3]),(0,255,0),2)

    segments = [] #Segments of leafs
    segment_areas = [] #Areas of leaf segments
    simetries  = [] #Simetries (rectangles) of leafs
    thresh = f.find_thresh(image)

    #Create al the simetries (right, left, bottom, top)
    simetries.append(np.array([rect_points[0],middle_points[0],middle_points[2], rect_points[3]]))
    simetries.append(np.array([middle_points[0],rect_points[1], rect_points[2],middle_points[2]]))
    simetries.append(np.array([rect_points[0], rect_points[1],middle_points[1], middle_points[3]]))
    simetries.append(np.array([middle_points[3], middle_points[1],rect_points[2], rect_points[3]]))

    #Calculates the segments and the areas
    for sim in simetries:
        canvas = np.zeros((image.shape[0], image.shape[1], 1), dtype=np.uint8)
        cv2.fillPoly(canvas, pts=[sim], color=(255,255,255))
        segments.append(cv2.bitwise_and(thresh, canvas))
        
        area = cv2.countNonZero(canvas)
        segment_areas.append(area)
        print(area)

    #Calculate the simery
    tb_simetry = segment_areas[3]/segment_areas[2]
    rl_simetry = segment_areas[1]/segment_areas[0]
    print(tb_simetry)
    print(rl_simetry)
    simetry = tb_simetry*rl_simetry
    print(simetry)

    for seg in segments:
        res = f.resize_image(seg,0.3)
        f.show_image(res)

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

def calc_cc_ratio(image):
    '''Calculates ratio of enclosing circle
    and leaf circumferences.'''

    encl_circ = calc_encl_circumference(image)

    cnt,_ = f.find_cnt(image)
    cnt = cv2.cvtColor(cnt, cv2.COLOR_RGB2GRAY)
    leaf_circ = cv2.countNonZero(cnt)

    ratio = leaf_circ/encl_circ
    print(ratio)

def calc_ca_ratio(image):
    '''Calculates the ration betwen the 
    circumference of the enclsing circle and the leaf's area.'''

    encl_circ = calc_encl_circumference(image)
    
    _,cnt = f.find_cnt(image)
    area = cv2.contourArea(cnt[0])
    ratio = area/encl_circ

    print(ratio)
    return ratio


def calc_encl_circumference(image):
    '''Calulates the circumference of the enclosing circle.'''

    encl,_ = f.find_encl(image)
    cnt,_=f.find_cnt(encl)
    cnt = cv2.cvtColor(cnt, cv2.COLOR_BGR2GRAY)
    circ = cv2.countNonZero(cnt)
    return circ


'''Calculations'''
import image_processing.fex as f
import cv2
import numpy as np
from math import sqrt,pow,pi

def calc_rectangularity(image):
    '''Calculates the rectangularity of a leaf.'''

    #Calculates enclosing rectangle area
    _, rect, _ = f.find_rect(image)
    rect_area = rect[1][0] * rect[1][1];

    #Calculate leaf area
    leaf_area = calc_leaf_area(image)

    #Calculate rectangularity in procentage
    rectangularity = (leaf_area/rect_area) * 100

    return rectangularity

def calc_circularity(image):
    '''Calculates the circularity of a leaf.'''

    #Calculates enclosing circle area
    _, _, circ = f.find_encl(image)
    circ_area = pow(circ[1],2)*pi

    #Calculate leaf area
    leaf_area = calc_leaf_area(image)

    #Calculate circularity in procentage
    circularity = (leaf_area/circ_area) * 100
    
    #Returns circularity
    return circularity

def calc_hw_ratio(image):
    '''Calculates height-width ratio of a leaf.'''

    #Calculates the height and the width
    _,rect, _ = f.find_rect(image)
    height = rect[1][0]
    width = rect[1][1]

    #Returns ratio
    return height/width

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
    
    #Initiation
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

    #Calculate the simery
    tb_simetry = segment_areas[3]/segment_areas[2]
    rl_simetry = segment_areas[1]/segment_areas[0]
    simetry = tb_simetry*rl_simetry

    #Return simetry 
    return simetry

def calc_leaf_area(image):
    '''Calculates leaf area.'''

    #Calculate and return leaf area
    cnt_img, cnt = f.find_cnt(image)
    return cv2.contourArea(cnt)

def calc_cc_ratio(image):
    '''Calculates ratio of enclosing circle
    and leaf circumferences.'''

    #Calculates circumference of the enclosing circle
    encl_circ = calc_encl_circumference(image)

    #Calculates leaf circumference
    cnt,_ = f.find_cnt(image)
    cnt = cv2.cvtColor(cnt, cv2.COLOR_RGB2GRAY)
    leaf_circ = cv2.countNonZero(cnt)

    #Return ratio
    return encl_circ/leaf_circ

def calc_ca_ratio(image):
    '''Calculates the ration betwen the 
    circumference of the enclsing circle and the leaf's area.'''

    #Calculates circumference of the enclosing circle
    encl_circ = calc_encl_circumference(image)
    
    #Calculates leaf area
    _,cnt = f.find_cnt(image)
    area = cv2.contourArea(cnt)

    #Returns ratio
    return area/encl_circ

def calc_ch_ratio(image):
    '''Calculates ratio betwen circumference of 
    eclosing circle ant the height of the leaf.'''

    #Calculates circumference of the enclosing circle
    encl_circ = calc_encl_circumference(image)

    #Calculates the height of the leaf
    _,rect,_= f.find_rect(image)
    height = rect[1][0]
    
    #Returns the ratio
    return encl_circ/height

def calc_cw_ratio(image):
    '''Calculates ratio betwen circumference of 
    eclosing circle ant the width of the leaf.'''

    #Calculates circumference of the enclosing circle
    encl_circ = calc_encl_circumference(image)

    #Calculates the width of the leaf
    _,rect,_= f.find_rect(image)
    width = rect[1][1]

    #Return ratio
    return encl_circ/width

def calc_center_distance_ratio(image):
    '''Calculates the ratio between the circumference 
    of the enclosing circle and the distance between the centers
    of the enclosing circle and rectangel.'''

    #Calculates circumference of the enclosing circle
    encl_circ = calc_encl_circumference(image)

    #Calulate centers
    _,_,encl = f.find_encl(image,keep_original=True)
    _,_,rect = f.find_rect(image,keep_original=True)
    encl_center = encl[0]
    rect_center = rect[0]

    #Calulate distance
    distance = sqrt(pow(encl_center[0]-rect_center[0],2)+pow(encl_center[1]-rect_center[1],2))

    #Returns ratio
    return encl_circ/distance

def calc_encl_circumference(image):
    '''Calulates the circumference of the enclosing circle.'''

    encl,_,_= f.find_encl(image)
    cnt,_=f.find_cnt(encl)
    cnt = cv2.cvtColor(cnt, cv2.COLOR_BGR2GRAY)
    circ = cv2.countNonZero(cnt)
    return circ

def calc_all(image):
    '''Calculate all the features.'''
    
    print("hw ratio:" + str(calc_hw_ratio(image)))
    print("===")
    print("simetry:" + str(calc_simetry(image)))
    print("===")
    print("circularity:" + str(calc_circularity(image)))
    print("===")
    print("rectangularity:" + str(calc_rectangularity(image)))
    print("===")
    print("ca ratio:" + str(calc_ca_ratio(image)))
    print("===")
    print("cc ratio:" + str(calc_cc_ratio(image)))
    print("===")
    print("ch ratio:" + str(calc_ch_ratio(image)))
    print("===")
    print("cw ratio:" + str(calc_cw_ratio(image)))
    print("===")
    print("center distance ratio:" + str(calc_center_distance_ratio(image)))
    print("===")
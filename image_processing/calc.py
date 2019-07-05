'''Calculations'''
import image_processing.fex as f
from cv2 import contourArea

def calc_rectangularity(image):

    #Calculates enclosing rectangle area
    _, rect = f.find_rect(image)
    rect_area = rect[1][0] * rect[1][1];
    print(rect_area)

    #Calculates leaf area
    cnt_img, cnt = f.find_cnt(image)
    res = f.resize_image(cnt_img, 0.3)
    f.show_image(res)
    leaf_area = contourArea(cnt[0])
    print(leaf_area)

    #Calculate rectangularity in procentage
    rectangularity = (leaf_area/rect_area) * 100
    print(rectangularity)
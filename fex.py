'''Feature extraxtion (fe-ex)'''
import cv2
import numpy as np

def find_edge(image):
    '''Returns the edge of a leaf.'''
    edge = cv2.Canny(image, 300, 480)
    return edge

def thresh(image):
    '''Returns thresholded image.'''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,230,255,cv2.THRESH_BINARY_INV)
    return thresh

def calc_area(image):
    '''Returns the area of a leaf.'''
    bw = thresh(image)
    return cv2.countNonZero(bw)

def hull(image):
    '''Returns image of the convex hull.'''
    thr = thresh(image)
    edge = find_edge(thr)
    cnt,_ = cv2.findContours(edge, 1, 2)
    new_img = np.zeros((edge.shape[0], edge.shape[1], 3), dtype = np.uint8) #Create a blank image (array of zeros)
    color = (256,256,256) #Define color for drawing the hulls
    hull_list = [] #Empty hull list
    for i in range(len(cnt)): #Append all hulls
        hull = cv2.convexHull(cnt[i])
        hull_list.append(hull)

    max_len_index = 0 #Index of the longest hull
    for i in range(len(hull_list)): #Iterate through all hulls
        #Check if the current hull is longer than the current longest
        if cv2.arcLength(hull_list[i], True) > cv2.arcLength(hull_list[max_len_index], True):
            max_len_index = i

    cv2.drawContours(new_img, hull_list, max_len_index, color) #Draw the longest hull to the blank image
    return new_img #Return the image

def calc_ciric(image):
    '''Returns the circumference of the leaf.'''
    edge = find_edge(image)
    return cv2.countNonZero(edge)

def resize_image(image, factor):
    '''Returns the resized image.
    Parameter 'factor' represents the number with which the width and the height are multipied.'''
    height, width = image.shape[:2]
    resized = cv2.resize(image, (round(factor*width), round(factor*height)), interpolation = cv2.INTER_CUBIC)
    return resized

def show_image(image, title = "img"):
    '''Open window and show the image.'''
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
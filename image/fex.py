'''Feature extraxtion (fe-ex)'''
import cv2
import numpy as np

def morph_adjust(image):
    '''Removes noise form the image, and returns the adjusted image.
    Uses morphological transormations to reduce noise.'''
    kernel = np.ones((5,5), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN,kernel)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel) 
    image = cv2.erode(image,kernel,iterations = 1)
    return image

def find_edge(image):
    '''Returns the edge of a leaf.'''
    edge = cv2.Canny(image, 300, 480)
    return edge

def find_thresh(image):
    '''Returns thresholded image.'''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,230,255,cv2.THRESH_BINARY_INV)
    thresh = morph_adjust(thresh)
    return thresh

def find_hull(image):
    '''Returns image of the convex hull.'''
    thr = find_thresh(image)
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
    return new_img, hull_list[max_len_index] #Return the image

def find_rect(image):
    '''Finds the smallest bounding rectangle of a leaf.'''
    _, hull = find_hull(image)

    rect = cv2.minAreaRect(hull)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    new_img = np.ones((2000, 2000, 3), dtype=np.uint8)
    cv2.drawContours(new_img, [box], 0, (0,0,256), 2)
    #Returns the image of the rect and the cnt
    return new_img, box

def find_encl(image):
    _, hull = find_hull(image)
    (x,y),radius = cv2.minEnclosingCircle(hull)
    center = (int(x),int(y))
    radius = int(radius)
    new_img = np.ones((2000, 2000, 3), dtype=np.uint8)
    cv2.circle(new_img,center,radius,(255,255,255),2)
    edge = find_edge(new_img)
    cnt,_ = cv2.findContours(edge, 1,2)
    new_img = np.ones((2000, 2000, 3), dtype=np.uint8)
    cv2.drawContours(new_img, [cnt[0]], 0, (0, 0, 256), 2)
    #Returns the image of the circ and the cnt
    return new_img, cnt

def calc_area(image):
    '''Returns the area of a leaf.'''
    bw = thresh(image)
    return cv2.countNonZero(bw)

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

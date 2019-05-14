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

def find_cnt(image):

    #Find contour
    thr = find_thresh(image)
    edge = find_edge(thr)
    cnt,_ = cv2.findContours(edge, 1, 2)

    #Draw contour
    new_img = np.zeros((edge.shape[0], edge.shape[1], 3), dtype = np.uint8)
    cv2.drawContours(new_img, cnt, 0, (255, 255, 0))

    #Returns drawn contour and the contour object
    return new_img, cnt

def find_hull(image):
    '''Returns image of the convex hull.'''

    #Find image contour
    img, cnt = find_cnt(image)

    new_img = np.zeros((img.shape[0], img.shape[1], 3), dtype = np.uint8) #Create a blank image (array of zeros)
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

    #Find leaf convex hull
    _, hull = find_hull(image)

    #Generate rectangle
    rect = cv2.minAreaRect(hull)
    x , y = rect[0]
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    
    #Fing the x cordinate of the point with the lowest x cordinate
    #and the y cordinate of the point with the lowest y cordinate
    min_x_point = box[0][0]
    min_y_point = box[0][1]
    for point in box:
        if point[0] < min_x_point:
            min_x_point = point[0]
        if point[1] < min_y_point:
            min_y_point = point[1]

    #Move center so all point are positive
    if min_x_point < 0:
        x += (abs(min_x_point) + 50)
    if min_y_point < 0:
        y += (abs(min_y_point) + 50)

    #Create new rectangle
    new_rect = ((x,y), rect[1], rect[2])
    shape = list(new_rect[1])
    box = cv2.boxPoints(new_rect)
    box = np.int0(box)

    #Draw rectangle
    max_x_point = box[0][0]
    max_y_point = box[0][1]
    for point in box:
        if point[0] > max_x_point:
            max_x_point = point[0]
        if point[1] > max_y_point:
            max_y_point = point[1]
    color = (0, 0, 255)
    img_size = (int(max_y_point)+20, int(max_x_point+20)+20, 3)
    rect_img = np.ones(img_size, dtype=np.uint8)
    cv2.drawContours(rect_img, [box], 0, color, 2)

    #Returns the image of the rectangle 
    #and the rect object that contains all info about the rectangle (ceter, height, width, rotation)
    return rect_img, rect

def find_encl(image):
    '''Finds the smallest enclosing circle of a leaf.'''

    #Find leaf convex hull
    _, hull = find_hull(image)

    #Generate circle
    (x,y),radius = cv2.minEnclosingCircle(hull)
    while x-radius < float(0):
        x+=50
    while y-radius < float(0):
        y+=50
    
    center = (int(x),int(y))
    radius = int(radius)
    
    #Draw circle
    color = (255,255,255)
    img_size = (int(x + radius + 100), int(y + radius + 100), 3)
    new_img = np.ones(img_size, dtype=np.uint8)
    cv2.circle(new_img,center,radius, color,-1)

    #Find circle contour
    _, hull = find_hull(new_img) 

    #Returns the image of the circ and the cnt
    return new_img, hull

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

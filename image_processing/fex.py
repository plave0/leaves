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
    edge = cv2.Canny(image, 20, 100)
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
    cnt,_ = cv2.findContours(thr, 1, 2)

    #Find the largest cnt
    max_len_index = 0
    for i in range(len(cnt)):    
        if cv2.arcLength(cnt[i], True) > cv2.arcLength(cnt[max_len_index], True):
            max_len_index = i

    #Draw contour
    new_img = np.zeros(image.shape, dtype = np.uint8)
    cv2.drawContours(new_img, cnt, max_len_index, (255, 255, 0))

    #Returns drawn contour and the contour object
    return new_img, cnt[max_len_index]

def find_hull(image):
    '''Returns image of the convex hull.'''

    #Find image contour
    img, cnt = find_cnt(image)

    #Find hull
    hull_list = [] #Empty hull list
    hull_list.append(cv2.convexHull(cnt))

    #Drawing hull
    new_img = np.zeros(img.shape, dtype = np.uint8) #Create a blank image (array of zeros)
    color = (256,256,256) #Define color for drawing the hulls
    cv2.drawContours(new_img, hull_list, 0, color) #Draw the longest hull to the blank image

    #Return hull image and hull object
    return new_img, hull_list[0] #Return the image

def find_rect(image, keep_original=False):
    '''Finds the smallest bounding rectangle of a leaf.'''

    #Find leaf convex hull
    hull_img, hull = find_hull(image)

    #Generate rectangle
    rect = cv2.minAreaRect(hull)
    x , y = rect[0]
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    
    #If the original image isn't kept
    if not keep_original:
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
        #and the rect object that contains all info about
        #the rectangle ((x,y), (height, width), rotation)
        #and the cordinates of all rectangle points
        return rect_img, rect, box
    #If the original image is kept
    else:
        #Draws contour
        color = (0, 0, 255)
        cv2.drawContours(image, [box], 0, color, 2)

        #Returns the image of the rectangle 
        #and the rect object that contains all info about
        #the rectangle ((x,y), (height, width), rotation)
        #and the cordinates of all rectangle points
        return image, rect, box

def find_encl(image, keep_original=False):
    '''Finds the smallest enclosing circle of a leaf.'''

    #Find leaf convex hull
    _, hull = find_hull(image)

    #Generate circle
    (x,y),radius = cv2.minEnclosingCircle(hull)
    center = (int(x),int(y))
    radius = int(radius)

    #If the original image is not kept
    if not keep_original:
        while x-radius < float(0):
            x+=50
        while y-radius < float(0):
            y+=50
    
        center = (int(x), int(y))
        #Draw circle
        color = (255,255,255)
        img_size = (int(y + radius + 100),int(x + radius + 100),3)
        new_img = np.ones(img_size, dtype=np.uint8)
        cv2.circle(new_img,center,radius, color,-1)

        #Find circle contour
        _, hull = find_hull(new_img) 

        #Returns the image of the circ, the cnt, and the circle parameter
        return new_img, hull, (center, radius)
    #If the original image is kept
    else:
        #Draw circle
        color = (255,255,255)
        new_img = np.ones(image.shape, dtype=np.uint8)
        cv2.circle(new_img,center,radius, color,-1)

        #Find circle contour
        _, hull = find_hull(new_img) 
        
        #Returns the image of the circ, the cnt, and the circle parameter
        return new_img, hull, (center, radius)

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

def test_fex(img):
    '''Test all the features of an image.'''

    image = find_edge(img)
    res = resize_image(image,0.4)
    show_image(res)
    #
    image = find_thresh(img)
    res = resize_image(image,0.4)
    show_image(res)
    #
    image,_ = find_cnt(img)
    res = resize_image(image,0.4)
    show_image(res)
    #
    image,_ = find_hull(img)
    res = resize_image(image,0.4)
    show_image(res)
    #
    image,_,_ = find_rect(img)
    res = resize_image(image,0.4)
    show_image(res)
    #
    image,_,_ = find_encl(img)
    res = resize_image(image,0.4)
    show_image(res)

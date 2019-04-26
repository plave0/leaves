'''Feature extraxtion (fe-ex)'''
import cv2

def find_edge():
    pass

def show_image(image, title = "img"):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''Feature extraxtion (fe-ex)'''
import cv2

def find_edge(image):
    edge = cv2.Canny(image, 300, 480)
    return edge

def show_image(image, title = "img"):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
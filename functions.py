import cv2
import numpy as np

def read_image(address):#'pdf2png\E1T7-1.png'
    img = cv2.imread(address)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret,thresh = cv2.threshold(img,40,255,cv2.THRESH_BINARY_INV)
    return thresh, img



def contours_extraction(thresh):
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours,hierarchy



def extent(contours):
    area = cv2.contourArea(contours)
    x,y,w,h = cv2.boundingRect(contours)
   
    extent = float(area)
    coord= {"x":x,"y":y,"w":w,"h":h,"area":extent}
    return coord

def list_to_dict_coord(contours):
    size = []
    dict = {}
    # loop over all the contours
    for i, cnt in enumerate(contours):
        size.append(extent(cnt))
    return size


def max_area(size):
    max_area = 0
    i_max = 0
    for i in range(0,len(size)):
        max_area_comp=size[i]["area"]
        if max_area_comp > max_area:
            max_area = max_area_comp
            i_max=i
    return max_area,i_max # temos o maior retangulo


def max_coord(m_area,size):
    x_coord=size[m_area[1]]["x"]
    y_coord = size[m_area[1]]["y"]

    return x_coord, y_coord



def retangule_draw(size,img):
    n,i=max_area(size)
    x=size[i]["x"]
    y=size[i]["y"]

    w=size[i]["w"]
    h=size[i]["h"]
    img_retangule=cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),5)

    dist = np.linalg.norm(np.array((x,y))-np.array((x+w,y+h)))
    cv2.imwrite("pdf2png/result_retangule.png",img_retangule)

    return dist,img_retangule,x,y,w,h

def circle_draw(dist,img,x,y,w,h):
    w1=round((w/2)+x)
    h1=round((h/2)+y)


    center_coordinates = (w1,h1)
    
    # Radius of circle
    radius = round(dist/2)
    
    # Blue color in BGR
    color = (255,0,255)
    
    # Line thickness of 2 px
    thickness = -1
    
    # Using cv2.circle() method
    # Draw a circle with blue line borders of thickness of 2 px
    image_circle = cv2.circle(img, center_coordinates, radius, color, thickness)

    # Displaying the image 
    cv2.imwrite("pdf2png/result_circle.png",image_circle)
    
    return image_circle
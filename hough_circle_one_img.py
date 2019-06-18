import cv2
import numpy as np

img = cv2.imread('typical_data/sgptsiskyimageC1.a1.20151001.235500.jpg.20151001235500.jpg', 0)
cimg = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100,
                            param1=60,param2=90,minRadius=160,maxRadius=0)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

print(len(circles))
# center of circle
print('center of circle: ' + str((i[0],i[1])))
# radius
print('radius: ' + str(i[2]))

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()


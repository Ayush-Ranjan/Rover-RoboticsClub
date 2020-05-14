#!/usr/bin/env python
from __future__ import print_function 
import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from matplotlib import pyplot as plt 
class image_converter: 
    def __init__(self):
        self.pub = rospy.Publisher('chatter', String, queue_size=10)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/magnus/camera/image_raw",Image,self.callback)
    def callback(self,data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        thresh1=cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)    
        x=cv_image.shape[1]
        y=cv_image.shape[0]
        ##for i in range(x):
            ##for j in range(y):    
        #colour = (thresh1[int(x/2)+60,int(y/2)])
        #print(colour)         
        thresh = cv2.threshold(thresh1, 50, 255, cv2.THRESH_BINARY)[1]
        _,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.circle(cv_image,(int(x/2),int(y/2)), 3, (255,0,0), 4)
        #print(len(contours))
        res = max(contours, key=cv2.contourArea)
        cv2.drawContours(cv_image, res, -1, (0,255,0), 3)
        M = cv2.moments(res)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centre=(cX,cY)
        cv2.circle(cv_image, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(cv_image, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.imshow("Image window", cv_image)
        cv2.waitKey(100)
        self.pub.publish(centre)

def main(args):
    ic = image_converter()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
if __name__ == '__main__':
    main(sys.argv)
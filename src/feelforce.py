#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class ForceMapper(): 
    def __init__(self):
        self.r = rospy.Rate(250) # 250hz
        self.thresh = 1
        self.obstacle = ""
        self.nearWall = 0
        self.sub = rospy.Subscriber('/scan', LaserScan, self.callBack)
        self.pub_obs = rospy.Publisher('obstacle', String, queue_size=10)
        self.start()
       
    def start(self):
        while not rospy.is_shutdown():
            self.pub_obs.publish(self.obstacle)
            self.r.sleep()

    def callBack(self, msg):
        size = len(msg.ranges)
        right = msg.ranges[0]
        front =  min(msg.ranges[size/2-50:size/2+50])
        frontLeft = msg.ranges[size*3/4]
        frontRight = msg.ranges[size/4]
        left = msg.ranges[size-1]
        print("front: ", front, size)
        if front<1:
            self.obstacle="front"
            self.nearWall=1
        #elif right<self.thresh:
         #   self.obstacle="right"
          #  self.nearWall=0.2
        #elif left<self.thresh:
         #   self.obstacle="left"
          #  self.nearWall=0.2
        elif frontLeft<0.3:
            self.obstacle="frontleft"
            self.nearWall=1
        elif frontRight<0.3:
            self.obstacle="frontright"
            self.nearWall=1
           
        else:
            self.obstacle=""
            self.nearWall=0

def main():
    rospy.init_node('ForceMapper')
    try:
        force = ForceMapper()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
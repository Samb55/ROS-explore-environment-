#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class Foward(): 
    def __init__(self):
        #self.decision = ""
        self.cmd_pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=1)
        self.sub = rospy.Subscriber('turning', String, self.decideForward)
        self.r = rospy.Rate(250) # 250hz
        self.linear_speed = 0.5
        self.move_cmd = Twist()
        self.start()


    def decideForward(self, data):
        self.decision=data.data
        if self.decision=="T":
            print(self.decision)
            self.stopMoving()
        else:
            print(self.decision)
            self.forward()
    
    def stopMoving(self):
        self.move_cmd.linear.x=0
        self.move_cmd.linear.z=0
    def forward(self):
        #print("MOVING FORWARD\n")
        self.move_cmd.linear.x = self.linear_speed
        #print(self.move_cmd)
        #self.cmd_pub.publish(self.move_cmd)
    
    def start(self):
        while not rospy.is_shutdown():
            self.cmd_pub.publish(self.move_cmd)
            self.r.sleep()
            
        
def main():
    rospy.init_node('Forward')
    try:
        Foward()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
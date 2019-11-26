#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class Turn(): 
    def __init__(self):
        self.cmd_pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=1)
        self.r = rospy.Rate(250) # 250hz
        self.move_cmd = Twist()
        
        self.isTurning = "F"
        self.pub_turning = rospy.Publisher('/turning', String, queue_size=10)
        self.sub = rospy.Subscriber('/obstacle', String, self.decideTurn)
        self.start()
        
    def turn(self, factor):
        self.move_cmd.linear.x = 0
        self.move_cmd.angular.z = factor
        self.isTurning = "T"

    def stopTurning(self):
        self.move_cmd.linear.x = 0
        self.move_cmd.angular.z = 0
        self.isTurning = "F"

    def start(self):
        while not rospy.is_shutdown():
            self.pub_turning.publish(self.isTurning)
            self.cmd_pub.publish(self.move_cmd)
            self.r.sleep()

    def decideTurn(self, decision):
        #rospy.loginfo(decision.data)
        self.decision=decision.data
        print(self.decision)
        if (self.decision == "front"):
            self.turn(1)
        #elif (self.decision == "left"):
        #    self.turn(0.5)
        #elif (self.decision == "right"):
        #    pass
        elif (self.decision == "frontleft"):
            self.turn(-0.5)
        elif (self.decision == "frontright"):
            self.turn(0.5)
        else:
            self.stopTurning()
        
def main():
    rospy.init_node('Turn')
    try:
        Turn()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
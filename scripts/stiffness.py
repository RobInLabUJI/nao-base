#!/usr/bin/env python

import rospy
from std_srvs.srv import Empty

def handle_stiffness_on(req):
    global motionProxy
    names = "Body"
    stiffnessLists = 1.0
    timeLists = 1.0
    motionProxy.stiffnessInterpolation(names, stiffnessLists, timeLists)
    return

def handle_stiffness_off(req):
    global motionProxy
    names = "Body"
    stiffnessLists = 0.0
    timeLists = 1.0
    motionProxy.stiffnessInterpolation(names, stiffnessLists, timeLists)
    return

def stiffness_server():
    global motionProxy
    motionProxy = ALProxy("ALMotion", robotIP, PORT)

    rospy.init_node('stiffness_server')
    rospy.Service('stiffness_on',  Empty, handle_stiffness_on)
    rospy.Service('stiffness_off', Empty, handle_stiffness_off)
    rospy.spin()

if __name__ == "__main__":
    stiffness_server()

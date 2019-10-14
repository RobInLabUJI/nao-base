#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from naoqi import ALProxy
import vision_definitions

def tracker_loop():

    rospy.init_node('vision', anonymous=True)
    pub = rospy.Publisher('camera/top/camera/image_raw', Image, queue_size=10)

    if rospy.has_param('nao_ip'):
        NAO_IP = rospy.get_param('nao_ip')
    else:
        NAO_IP = "127.0.0.1"
    if rospy.has_param('nao_port'):
        NAO_PORT = rospy.get_param('nao_port')
    else:
        NAO_PORT = 9559
    
    motionProxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
    motionProxy.setStiffnesses("Head", 1.0)

    tracker = ALProxy("ALTracker", NAO_IP, NAO_PORT)
    targetName = "RedBall"
    diameterOfBall = 0.06
    tracker.registerTarget(targetName, diameterOfBall)
    mode = "Head"
    tracker.setMode(mode)
    tracker.track(targetName)

    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        r.sleep()

if __name__ == '__main__':
    tracker_loop()

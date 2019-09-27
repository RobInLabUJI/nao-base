#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64MultiArray
from naoqi import ALProxy

def callback(msg):
   
    global motionProxy
    #tts.say(msg.data)
    names            = ["HeadYaw", "HeadPitch"]
    angles           = msg.data[0:2]
    fractionMaxSpeed = 0.1
    motionProxy.setAngles(names,angles,fractionMaxSpeed)
    
def head():

    rospy.init_node('head', anonymous=True)
    rospy.Subscriber("head_angles", Float64MultiArray, callback)

    if rospy.has_param('nao_ip'):
        NAO_IP = rospy.get_param('nao_ip')
    else:
        NAO_IP = "127.0.0.1"

    global motionProxy
    motionProxy = ALProxy("ALMotion", NAO_IP, 9559)
    motionProxy.setStiffnesses("Head", 1.0)
    rospy.spin()

if __name__ == '__main__':
    head()

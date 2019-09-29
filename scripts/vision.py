#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64MultiArray
from naoqi import ALProxy
    
def vision():

    rospy.init_node('vision', anonymous=True)
    pub = rospy.Publisher('head_joints', Float64MultiArray, queue_size=10)

    if rospy.has_param('nao_ip'):
        NAO_IP = rospy.get_param('nao_ip')
    else:
        NAO_IP = "127.0.0.1"
    if rospy.has_param('nao_port'):
        NAO_PORT = rospy.get_param('nao_port')
    else:
        NAO_PORT = 9559

    global motionProxy
    motionProxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
    motionProxy.setStiffnesses("Head", 1.0)

    r = rospy.Rate(10) # 10hz
    names = "Head"
    useSensors  = True
    while not rospy.is_shutdown():
        sensorAngles = motionProxy.getAngles(names, useSensors)
        msg = Float64MultiArray(data=sensorAngles)
        pub.publish(msg)
        r.sleep()

if __name__ == '__main__':
    vision()

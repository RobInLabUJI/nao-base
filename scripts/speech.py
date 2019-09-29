#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from naoqi import ALProxy

def callback(msg):
   
    global tts
    tts.say(msg.data)

    
def speech():

    rospy.init_node('speech', anonymous=True)
    rospy.Subscriber('speech', String, callback)

    if rospy.has_param('nao_ip'):
        NAO_IP = rospy.get_param('nao_ip')
    else:
        NAO_IP = '127.0.0.1'

    if rospy.has_param('nao_port'):
        NAO_PORT = rospy.get_param('nao_port')
    else:
        NAO_PORT = 9559

    global tts
    tts = ALProxy('ALTextToSpeech', NAO_IP, NAO_PORT)

    rospy.spin()

if __name__ == '__main__':
    speech()

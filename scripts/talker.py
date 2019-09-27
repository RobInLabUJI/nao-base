#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from naoqi import ALProxy

def callback(msg):
   
    global tts
    tts.say(msg.data)

    
def talker():

    rospy.init_node('talker', anonymous=True)
    rospy.Subscriber("talk", String, callback)

    if rospy.has_param('nao_ip'):
        NAO_IP = rospy.get_param('nao_ip')
    else:
        NAO_IP = "127.0.0.1"

    global tts
    tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)

    rospy.spin()

if __name__ == '__main__':
    talker()

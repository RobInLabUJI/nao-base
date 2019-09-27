#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from naoqi import ALProxy

def callback(msg):
   
    global tts
    tts.say(msg.data)
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", msg.data)

    
def talker():

    global tts
    tts = ALProxy("ALTextToSpeech", "192.168.1.22", 9559)

    rospy.init_node('talker', anonymous=True)
    rospy.Subscriber("talk", String, callback)
    rospy.spin()

if __name__ == '__main__':
    talker()

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
    pub = rospy.Publisher('word_recognized', Float64MultiArray, queue_size=10)

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
    asr = ALProxy("ALSpeechRecognition", NAO_IP, NAO_PORT)

    asr.setLanguage("English")
    vocabulary = ["yes", "no", "please"]
    asr.setVocabulary(vocabulary, False)
    asr.subscribe("Test_ASR")

    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        #pub.publish(msg)
        r.sleep()
    asr.unsubscribe("Test_ASR")

if __name__ == '__main__':
    speech()

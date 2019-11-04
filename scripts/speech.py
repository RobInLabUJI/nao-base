#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String
from naoqi import ALProxy

def callback(msg):
   
    global tts
    global asr
    asr.pause(True)
    tts.say(msg.data)
    asr.pause(False)
    
def speech():

    rospy.init_node('speech', anonymous=True)
    rospy.Subscriber('speech', String, callback)
    pub = rospy.Publisher('word_recognized', String, queue_size=10)

    if rospy.has_param('nao_ip'):
        NAO_IP = rospy.get_param('nao_ip')
    else:
        NAO_IP = '127.0.0.1'

    if rospy.has_param('nao_port'):
        NAO_PORT = rospy.get_param('nao_port')
    else:
        NAO_PORT = 9559

    global tts
    global asr
    tts = ALProxy('ALTextToSpeech', NAO_IP, NAO_PORT)
    asr = ALProxy("ALSpeechRecognition", NAO_IP, NAO_PORT)
    #asr.unsubscribe("Test_ASR")

    asr.setLanguage("English")
    vocabulary = ["yes", "no", "one", "two", "three"]
    asr.setVocabulary(vocabulary, False)
    asr.subscribe("Test_ASR")

    memValueSpeech = "SpeechDetected"
    memValueWord   = "WordRecognized"
    try:
      memoryProxy = ALProxy("ALMemory", NAO_IP, NAO_PORT)
    except Exception, e:
      print "Error when creating memory proxy:"
      print str(e)
      exit(1)

    r = rospy.Rate(2) # 2hz
    while not rospy.is_shutdown():
        speechDetected = memoryProxy.getData(memValueSpeech)
        if speechDetected:
            time.sleep(1.0)
            wordRecognized = memoryProxy.getData(memValueWord)
            print(wordRecognized)
            pub.publish(wordRecognized[0])
        r.sleep()
    asr.unsubscribe("Test_ASR")

if __name__ == '__main__':
    speech()

#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Vector3
from naoqi import ALProxy
#import vision_definitions

def tracker_loop():

    rospy.init_node('vision', anonymous=True)
    pub = rospy.Publisher('red_ball', Vector3, queue_size=10)

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

    try:
      memoryProxy = ALProxy("ALMemory", IP, PORT)
    except Exception, e:
      print "Error when creating memory proxy:"
      print str(e)
      exit(1)

    r = rospy.Rate(10) # 10hz
    v = Vector3()
    while not rospy.is_shutdown():
        p = tracker.getTargetPosition()
        v.x = p[0]
        v.y = p[1]
        v.z = p[2]
        pub.publish(v)
        r.sleep()

if __name__ == '__main__':
    tracker_loop()

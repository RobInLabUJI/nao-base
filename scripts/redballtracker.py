#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64MultiArray
from naoqi import ALProxy

def tracker_loop():

    rospy.init_node('vision', anonymous=True)
    pub = rospy.Publisher('red_ball', Float64MultiArray, queue_size=10)

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

    memValue = "redBallDetected"
    try:
      memoryProxy = ALProxy("ALMemory", NAO_IP, NAO_PORT)
    except Exception, e:
      print "Error when creating memory proxy:"
      print str(e)
      exit(1)

    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        val = memoryProxy.getData(memValue)
        data = [val[1][0], val[1][1], val[1][2], val[1][3]]
        msg = Float64MultiArray(data=data)
        pub.publish(msg)

        
        r.sleep()

if __name__ == '__main__':
    tracker_loop()

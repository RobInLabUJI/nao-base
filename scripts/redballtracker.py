#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64MultiArray
from naoqi import ALProxy

def tracker_loop():

    rospy.init_node('redball_tracker', anonymous=True)
    pub = rospy.Publisher('red_ball', Float64MultiArray, queue_size=10)

    if rospy.has_param('nao_ip'):
        NAO_IP = rospy.get_param('nao_ip')
    else:
        NAO_IP = "127.0.0.1"
    if rospy.has_param('nao_port'):
        NAO_PORT = rospy.get_param('nao_port')
    else:
        NAO_PORT = 9559
    
    try:
      redBallProxy = ALProxy("ALRedBallDetection", NAO_IP, NAO_PORT)
      period = 100
      redBallProxy.subscribe("Test_Red_Ball", period, 0.0 )
    except Exception, e:
      print "Error when creating redball detection proxy:"
      print str(e)
      exit(1)

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

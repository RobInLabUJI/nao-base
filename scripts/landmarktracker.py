#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64MultiArray
from naoqi import ALProxy

def tracker_loop():

    rospy.init_node('landmark_tracker', anonymous=True)
    pub = rospy.Publisher('landmark', Float64MultiArray, queue_size=10)

    if rospy.has_param('nao_ip'):
        NAO_IP = rospy.get_param('nao_ip')
    else:
        NAO_IP = "127.0.0.1"
    if rospy.has_param('nao_port'):
        NAO_PORT = rospy.get_param('nao_port')
    else:
        NAO_PORT = 9559
    
    try:
      landMarkProxy = ALProxy("ALLandMarkDetection", NAO_IP, NAO_PORT)
      period = 500
      landMarkProxy.subscribe("Test_Mark", period, 0.0 )
    except Exception, e:
      print "Error when creating landmark detection proxy:"
      print str(e)
      exit(1)

    memValue = "LandmarkDetected"
    try:
      memoryProxy = ALProxy("ALMemory", NAO_IP, NAO_PORT)
    except Exception, e:
      print "Error when creating memory proxy:"
      print str(e)
      exit(1)

    r = rospy.Rate(2) # 2hz
    while not rospy.is_shutdown():
        val = memoryProxy.getData(memValue)
        if(val and isinstance(val, list) and len(val) >= 2):

            # We detected naomarks !
            # For each mark, we can read its shape info and ID.

            # First Field = TimeStamp.
            timeStamp = val[0]

            # Second Field = array of Mark_Info's.
            markInfoArray = val[1]

            try:
              # Browse the markInfoArray to get info on each detected mark.
              for markInfo in markInfoArray:

                # First Field = Shape info.
                markShapeInfo = markInfo[0]

                # Second Field = Extra info (ie, mark ID).
                markExtraInfo = markInfo[1]
                print "mark  ID: %d" % (markExtraInfo[0])
                print "  alpha %.3f - beta %.3f" % (markShapeInfo[1], markShapeInfo[2])
                print "  width %.3f - height %.3f" % (markShapeInfo[3], markShapeInfo[4])
                data = [markExtraInfo[0], markShapeInfo[1], markShapeInfo[2], markShapeInfo[3], markShapeInfo[4]]
                msg = Float64MultiArray(data=data)
                pub.publish(msg)

            except Exception, e:
              print "Naomarks detected, but it seems getData is invalid. ALValue ="
              print val
              print "Error msg %s" % (str(e))
        
        r.sleep()

if __name__ == '__main__':
    tracker_loop()

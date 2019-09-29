#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from naoqi import ALProxy
import vision_definitions

def vision():

    rospy.init_node('vision', anonymous=True)
    pub = rospy.Publisher('camera/top/camera/image_raw', Image, queue_size=10)

    if rospy.has_param('nao_ip'):
        NAO_IP = rospy.get_param('nao_ip')
    else:
        NAO_IP = "127.0.0.1"
    if rospy.has_param('nao_port'):
        NAO_PORT = rospy.get_param('nao_port')
    else:
        NAO_PORT = 9559
    cameraID = 0

    videoProxy = ALProxy("ALVideoDevice", NAO_IP, NAO_PORT)
    resolution = vision_definitions.kQVGA  # 320 * 240
    colorSpace = vision_definitions.kRGBColorSpace
    imgClient = videoProxy.subscribe("client", resolution, colorSpace, 5)
    videoProxy.setParam(vision_definitions.kCameraSelectID, cameraID)

    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        alImage = videoProxy.getImageRemote(imgClient)
        imageWidth  = alImage[0]
        imageHeight = alImage[1]
        imageArray  = alImage[6]
        im = Image()
        im.height = imageHeight
        im.width  = imageWidth
        im.encoding = "rgb8"
        im.is_bigendian = 0
        im.step = 960
        im.data = imageArray
        pub.publish(im)
        r.sleep()
    videoProxy.unsubscribe(imgClient)

if __name__ == '__main__':
    vision()

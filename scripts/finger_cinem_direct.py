#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

pub = rospy.Publisher('joint_states', JointState, queue_size=10)

def callback(data):
	#read values from m1 and m2
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    try:
		motorup_index=data.name.index('gripper_motorup_joint')
		motordown_index=data.name.index('gripper_motordown_joint')
    except ValueError:
	    return
    
    if motorup_index>=0 and motordown_index>=0:
		
		motorup_pose=data.position[motorup_index];
		motordown_pose=data.position[motordown_index];
		
		#calculate finger pose
		finger_x = (motorup_pose+motordown_pose)*0.00124896/(91*4*math.pi)
		finger_theta = (motorup_pose-motordown_pose)*0.00124896/(91*4*math.pi*0.048)
		
		#publish to prismatic and revolute joints
		msgs_pub = JointState()
		msgs_pub.header = Header()
		msgs_pub.header.stamp = rospy.Time.now()
		msgs_pub.name = ['gripper_motorup_joint', 'gripper_motordown_joint', 'gripper_prismatic_joint', 'gripper_revolute_joint']
		msgs_pub.position = [data.position[motorup_index], data.position[motordown_index], finger_x, finger_theta]
		msgs_pub.velocity = []
		msgs_pub.effort = []
		pub.publish(msgs_pub)
    
    
def controller_finger():

    rospy.init_node('cinem_direct_finger_node', anonymous=True)

    rospy.Subscriber("joint_states_fake", JointState, callback)
    
    rospy.spin()

if __name__ == '__main__':
    controller_finger()


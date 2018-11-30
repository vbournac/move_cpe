#! /usr/bin/env python
 
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import Bool


class moveit_test_Coins:

  def __init__(self):
    print "============ Starting tutorial setup"
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
    self.robot = moveit_commander.RobotCommander()
    self.scene = moveit_commander.PlanningSceneInterface()
    self.group = moveit_commander.MoveGroupCommander("scara_cpe_group")
    self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory,queue_size=30)
    self.grip_publisher=rospy.Publisher('/grip',Bool,queue_size=30)
    self.detect_coin_subscriber = rospy.Subscriber("detect_metal",Bool,self.detection)
   
    
    self.group.set_named_target('straight')
    self.group.go(wait=True)
    self.group.set_pose_reference_frame("base_link")
    
    self.pose_A = geometry_msgs.msg.Pose()
    self.pose_B= geometry_msgs.msg.Pose()
    self.pose_B .position.x = 0.035
    self.pose_B.position.y = 0.14
    self.pose_B.position.z = -0.025
    
    self.pose_A .position.x = -0.073
    self.pose_A.position.y = 0.08
    self.pose_A.position.z = -0.025
    self.group.set_joint_value_target(self.pose_A,True)
    self.group.set_joint_value_target(self.pose_B,True)

    rospy.sleep(3)
    
  def detection(self,piece):
	self.coindetected=piece.data
  
  def move_to_position(self):
	self.group.set_joint_value_target(self.pose_A,True)
	self.group.plan()
	self.group.go(wait=True)
	rospy.sleep(1)
	self.grip_publisher.publish(True)
	rospy.sleep(1)
	self.group.set_joint_value_target(self.pose_B,True)
	self.group.plan()
	self.group.go(wait=True)
	rospy.sleep(1)
	self.grip_publisher.publish(False)
	rospy.sleep(1)
  
if __name__ == '__main__':
    try:
	moveit=moveit_test_Coins()
	moveit.move_to_position()
	rospy.spin()
    except rospy.ROSInterruptException:
        pass
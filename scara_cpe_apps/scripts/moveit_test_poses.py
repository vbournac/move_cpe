#! /usr/bin/env python
 
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg


class moveit_test_poses:

  def __init__(self):
    print "============ Starting tutorial setup"
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
    self.robot = moveit_commander.RobotCommander()
    self.scene = moveit_commander.PlanningSceneInterface()
    self.group = moveit_commander.MoveGroupCommander("scara_cpe_group")
    self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory,queue_size=30)
    self.group.set_named_target('straight')
    self.group.go(wait=True)
    self.group.set_pose_reference_frame("base_link")
    
    self.pose_B = geometry_msgs.msg.Pose()
    self.pose_D= geometry_msgs.msg.Pose()
    self.pose_B .position.x = -0.035
    self.pose_B.position.y = 0.12
    self.pose_B.position.z = -0.025
    
    self.pose_D .position.x = 0.035
    self.pose_D.position.y = 0.14
    self.pose_D.position.z = -0.025
    self.group.set_joint_value_target(self.pose_B,True)
    self.group.set_joint_value_target(self.pose_D,True)
    
    rospy.sleep(3)
  
  def move_to_position(self):
    for x in [self.pose_B,self.pose_D,self.pose_B]:
	self.group.set_joint_value_target(x,True)
	self.group.plan()
	self.group.go(True)
	rospy.sleep(5)

  
if __name__ == '__main__':
    try:
	moveit=moveit_test_poses()
	moveit.move_to_position()
	rospy.spin()
    except rospy.ROSInterruptException:
        pass
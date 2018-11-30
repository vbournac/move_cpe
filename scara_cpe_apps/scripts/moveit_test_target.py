#! /usr/bin/env python
 
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg


class moveit_test_named_target:

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
    rospy.sleep(3)
  
  def move_to_position(self):
    for x in ['right','straight','left']:
	self.group.set_named_target(x)
	self.group.go(wait=True)
	rospy.sleep(3)

  
if __name__ == '__main__':
    try:
	moveit=moveit_test_named_target()
	moveit.move_to_position()
	rospy.spin()
    except rospy.ROSInterruptException:
        pass
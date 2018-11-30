#! /usr/bin/env python
 
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg


class moveit_test_path:
  waypoints= []
  def __init__(self):
    print "============ Starting tutorial setup"
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
    self.robot = moveit_commander.RobotCommander()
    self.scene = moveit_commander.PlanningSceneInterface()
    self.group = moveit_commander.MoveGroupCommander("scara_cpe_group")
    self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory,queue_size=30)
    self.group.set_named_target('left')
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
        
    rospy.sleep(3)
  
  def move_to_position(self):
	#self.group.set_joint_value_target(self.pose_B,True)
	
	self.current_pose=self.group.get_current_pose().pose
	self.current_pose.position.z=-0.025
	
	self.waypoints.append(self.group.get_current_pose().pose)
	self.waypoints.append(self.pose_B)
	self.waypoints.append(self.pose_D)
	print self.waypoints
	
	#self.group.plan()
	#self.group.go(True)
	
	#rospy.sleep(3)
	#print 'do second move'
	(self.plan,self.fraction)=self.group.compute_cartesian_path(self.waypoints,0.01,1000)
	rospy.sleep(3)
	self.group.execute(self.plan)
	#print self.waypoints

	rospy.sleep(3)

  
if __name__ == '__main__':
    try:
	moveit=moveit_test_path()
	moveit.move_to_position()
	rospy.spin()
    except rospy.ROSInterruptException:
        pass
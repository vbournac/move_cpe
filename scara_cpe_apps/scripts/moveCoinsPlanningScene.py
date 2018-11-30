#! /usr/bin/env python
 
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import Bool


class moveit_test_Coins_Planning_scene:

  def __init__(self):
    print "============ Starting tutorial setup"
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
    self.robot = moveit_commander.RobotCommander()
    self.scene = moveit_commander.PlanningSceneInterface()
    rospy.sleep(2)
    self.group = moveit_commander.MoveGroupCommander("scara_cpe_group")
    self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory,queue_size=30)
    self.grip_publisher=rospy.Publisher('/grip',Bool,queue_size=30)
    self.detect_coin_subscriber = rospy.Subscriber("detect_metal",Bool,self.detection)

    self.eef_link = self.group.get_end_effector_link()
    print "============ End effector: %s" % self.eef_link


#Init robot in straight position
    self.group.set_named_target('straight')
    self.group.go(wait=True)
    self.group.set_pose_reference_frame("base_link")


#Define 2 positions A and B with coordonates
    self.pose_A = geometry_msgs.msg.Pose()
    self.pose_B= geometry_msgs.msg.Pose()

#Position B
    self.pose_B .position.x = 0.035
    self.pose_B.position.y = 0.14
    self.pose_B.position.z = -0.025

#Position A
    self.pose_A .position.x = -0.073
    self.pose_A.position.y = 0.08
    self.pose_A.position.z = -0.025
    self.group.set_joint_value_target(self.pose_A,True)
    self.group.set_joint_value_target(self.pose_B,True)
    
#add 2 different boxes
  #Small box that will be linked to "end_link"
    self.box_pose = geometry_msgs.msg.PoseStamped()
    self.box_pose.header.frame_id = "end_link"
    self.box_pose.header.stamp=rospy.Time.now()
    self.box_pose.pose.orientation.w = 1.0
    self.box_pose.pose.position.x = 0.02
    self.box_pose.pose.position.y = 0.00
    self.box_name = "box"
    self.scene.add_box(self.box_name,self.box_pose, size=(0.01, 0.01, 0.01))
    
  #big box that we be used as an obstacle for Robot
    self.box_pose_2= geometry_msgs.msg.PoseStamped()
    self.box_pose_2.header.frame_id = "world"
    self.box_pose_2.header.stamp=rospy.Time.now()
    self.box_pose_2.pose.orientation.w = 1.0
    self.box_pose_2.pose.position.x = 0.1
    self.box_pose_2.pose.position.y = 0.1
    self.box_name_2 = "box_2"
    self.scene.add_box(self.box_name_2,self.box_pose_2, size=(0.1, 0.1, 0.1))
    rospy.sleep(1)
    
    
  #go to position A then grip the coin
    self.group.set_joint_value_target(self.pose_A,True)
    self.group.plan()
    self.group.go(wait=True)
    rospy.sleep(1)
    self.grip_publisher.publish(True)#order to grip the coin
    rospy.sleep(1)
    
   #attach the small box to "end_link"
    rospy.sleep(2)
    grasping_group = 'scara_cpe_group'
    touch_links = self.robot.get_link_names(group=grasping_group)
    self.scene.attach_box(self.eef_link, self.box_name, touch_links=touch_links)
    rospy.sleep(1)
    
    
   #Go to position B
    self.group.set_joint_value_target(self.pose_B,True)
    self.group.plan()
    self.group.go(wait=True)
    rospy.sleep(1)
    self.grip_publisher.publish(False)#release the coin
    rospy.sleep(1)
    
   #detach the box from end-link then remove the small box (the big one remains)
    self.scene.remove_attached_object(self.eef_link,name=self.box_name)
    self.scene.remove_world_object(self.box_name)
    rospy.sleep(3)
    
  
if __name__ == '__main__':
    try:
	moveit=moveit_test_Coins_Planning_scene()
	rospy.spin()
    except rospy.ROSInterruptException:
        pass
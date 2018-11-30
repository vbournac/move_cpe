#! /usr/bin/env python
import roslib
import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction,FollowJointTrajectoryActionGoal
from trajectory_msgs.msg import JointTrajectoryPoint

if __name__ == '__main__':
    rospy.init_node('JointTrajectory')
    client = actionlib.SimpleActionClient('/scara_cpe/scara_cpe_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
    client.wait_for_server()

    move = FollowJointTrajectoryActionGoal()
    # Fill in the goal here
    
    point = JointTrajectoryPoint()
    point.positions = [0.0,0.0]
    point.time_from_start = rospy.Duration(3)
    move.goal.trajectory.joint_names = ['shoulder_1_joint', 'shoulder_2_joint']
   

    # move.goal.trajectory.points.positions[0]=1.5
    #move.goal.trajectory.points[0].positions[1]=1.5
    
    move.goal.trajectory.points.append(point)
    client.send_goal(move.goal)
    client.wait_for_result(rospy.Duration.from_sec(5.0))
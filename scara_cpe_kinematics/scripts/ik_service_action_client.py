#! /usr/bin/env python
import roslib
import rospy
import actionlib
import sys
import math
from control_msgs.msg import FollowJointTrajectoryAction,FollowJointTrajectoryActionGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from std_msgs.msg import Float32
from scara_cpe_kinematics.srv import gotoxy

def gotoxy_handle(req):
    move = FollowJointTrajectoryActionGoal()
    x= req.x
    y = req.y#float(sys.argv[1])
    offset = 0.048
    
    X= y - offset
    Y= -x
    
    l1= 0.08
    l2= 0.047
    theta2 = math.acos((X*X + Y*Y - l1*l1 - l2*l2)/(2*l1*l2))
    alpha = math.atan2(Y,X)
    beta = math.acos((X*X + Y*Y + l1*l1 - l2*l2)/(2*l1*math.sqrt(X*X + Y*Y)))
    theta1 = alpha - beta

    
    
    point = JointTrajectoryPoint()
    point.positions = [theta1,-theta2]
    point.time_from_start = rospy.Duration(3)
    move.goal.trajectory.joint_names = ['shoulder_1_joint', 'shoulder_2_joint']
   

    move.goal.trajectory.points.append(point)
    client.send_goal(move.goal)
    client.wait_for_result(rospy.Duration.from_sec(5.0))
    return True

if __name__ == '__main__':
    rospy.init_node('JointTrajectory')
    client = actionlib.SimpleActionClient('/scara_cpe/scara_cpe_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
    client.wait_for_server()
    positionx=0.035
    positiony=0.14
    # Fill in the goal here
    s = rospy.Service('gotoxy', gotoxy,gotoxy_handle )
    #gotoxy_handle(positionx,positiony)
    rospy.spin()

    
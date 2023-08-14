#! /usr/bin/env python
import rclpy
from geometry_msgs.msg import *
from rclpy.node import Node
from sensor_msgs.msg import *
import random

position = Pose()
laser = LaserScan()

def position_callback(data):
	global position

	position = data.pose[-1]

	

def laser_callback(data):
	global laser
	laser = data
	

if __name__=="__main__":

	rclpy.Subscriber("/scan", LaserScan, laser_callback)

	pub = rclpy.Publisher("/cmd_vel", Twist, queue_size=10)
	r = rclpy.Rate(5)
	velocity = Twist()
	while not rclpy.is_shutdown():

		if (len(laser.ranges) > 0):
			if (min(laser.ranges[90:270]) > 0.25):
				velocity.linear.x = random.uniform(-0.1, -0.25)
				velocity.angular.z = random.uniform(-0.1, 0.1)
			else:
				velocity.linear.x = 0.0
				velocity.angular.z = 0.25
			
			pub.publish(velocity)

		rclpy.loginfo("Linear velocity: %s m/s, Angular velocity: %s", velocity.linear.x, velocity.angular.z)
		rclpy.loginfo("Position: (%s, %s)", position.position.x, position.position.y)
		r.sleep()
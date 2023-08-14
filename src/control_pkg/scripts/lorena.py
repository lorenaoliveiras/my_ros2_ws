# !/usr/bin/env python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

distance = float()

class LinearVelPublisher(Node):

    def __init__(self):

        super().__init__('linear_vel_publisher')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):

        vel = Twist()

        vel.linear.x = 0.07
        vel.angular.z = 0.0

        self.publisher_.publish(vel)
        self.get_logger().info('Publishing velocity: linear x: "%f"' % vel.linear.x)


class AngularVelPublisher(Node):

    def __init__(self):

        super().__init__('angular_vel_publisher')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):

        vel = Twist()

        vel.linear.x = 0.0
        vel.angular.z = 0.7

        self.publisher_.publish(vel)
        self.get_logger().info('Publishing velocity: angular z: "%f"' % vel.angular.z)


class LaserSubscriber(Node):

    def __init__(self):
        super().__init__('laser_subscriber')

        qos_profile = QoSProfile(depth=10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT
        qos_profile.durability = QoSDurabilityPolicy.VOLATILE

        self.subscription = self.create_subscription(LaserScan, '/scan', self.listener_callback, qos_profile)
        self.subscription
        self.scan = LaserScan()

    def listener_callback(self, msg):

        global distance
        distance = msg.ranges[90]

        self.get_logger().info('I heard: min "%f" max "%f"'% (msg.ranges[90], msg.range_max))




def main(args=None):
    global distance

    rclpy.init(args=args)

    linear_vel_publisher = LinearVelPublisher()
    angular_vel_publisher = AngularVelPublisher()

    laser_subscriber = LaserSubscriber()

    #rclpy.spin(laser_subscriber)

    while rclpy.ok():
        rclpy.spin_once(laser_subscriber)
        rclpy.spin_once(linear_vel_publisher)
        print(distance)
        if distance <= 1.0:
            rclpy.spin_once(angular_vel_publisher)

    linear_vel_publisher.destroy_node()
    angular_vel_publisher.destroy_node()
    laser_subscriber.destroy_node()
    rclpy.shutdown()



if __name__ == "__main__":
    main()


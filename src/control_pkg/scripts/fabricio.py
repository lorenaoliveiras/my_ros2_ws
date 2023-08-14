from secrets import choice
import rclpy
from rclpy.node import Node
import random
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

dist = 1.0

class VelNode(Node):

    def __init__(self):
        super().__init__('velocity_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        time_period = 0.5
        self.timer = self.create_timer(time_period, self.timer_callback)

        self.subscription = self.create_subscription(LaserScan, '/scan', self.listener_callback, 10)
        self.subscription 

    def listener_callback(self, msg):
        global m

        self.get_logger().info('A distância é: "%f"' %msg.ranges[178])
        m = msg.ranges[178]


    def timer_callback(self):
        mover= Twist()

        if m > dist:

            mover.linear.x = 0.3
            mover.angular.z = 0.0

        if m <= dist:
            
            mover.linear.x = 0.0
            mover.angular.z = 0.8

        


        self.publisher_.publish(mover)
        self.get_logger().info('Velocidade Angular: "%f", Linear: "%f"' %(mover.angular.z, mover.linear.x))






def main(args=None):
    rclpy.init(args=args)

    vel_node  = VelNode()
    rclpy.spin(vel_node)
    vel_node.destroy_node()
    


    rclpy.shutdown()

if __name__ == '__main__':
    main() 
import rclpy
from rclpy.node import Node
import random
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.qos import QoSProfile

distancia = float()

class VelPublisher(Node):

    def __init__(self):
        super().__init__('vel_publisher')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.5 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 0.1
        msg.angular.z = 0.0
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing  linear speed: x: "%f" unidade de velocidade' %
(msg.linear.x))

class VelPublisher_angular(Node):

    def __init__(self):
        super().__init__('vel_publisher_angular')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.5 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.4
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing  angular speed: x: "%f" unidade de velocidade' %
(msg.angular.z))

class ScanSubscriber(Node):
    def __init__(self):
        super().__init__('scan_subscriber')
        qos_profile = QoSProfile(depth=10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT
        qos_profile.durability = QoSDurabilityPolicy.VOLATILE
        self.subscription = self.create_subscription(LaserScan, '/scan', self.listener_callback, qos_profile)
        self.subscription
        self.LaserScan = LaserScan()
    def listener_callback(self, msg):
        global distancia
        menor = msg.ranges[0]
        for dis in msg.ranges:
            if menor > dis:
                menor = dis
        distancia = menor
        self.get_logger().info('I heard: ranges[0] "%f" '% (msg.ranges[0]))

def main(args=None):
    global distancia
    print (distancia)
    rclpy.init(args=args)

    vel_publisher = VelPublisher()
    vel_publisher_angular = VelPublisher_angular()
    scan_subscriber = ScanSubscriber()

    #rclpy.spin_once(vel_publisher)
    rclpy.spin_once(scan_subscriber)
    print (distancia)

    while True:
        rclpy.spin_once(scan_subscriber)
        if (distancia < 0.5):
            print (distancia)
            rclpy.spin_once(vel_publisher_angular)
            continue
        else:
            rclpy.spin_once(vel_publisher)
            continue



    vel_publisher.destroy_node()
    scan_subscriber.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()
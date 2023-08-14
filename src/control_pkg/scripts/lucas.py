import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

VELOCIDADE_LINEAR_MAXIMA = 0.22
VELOCIDADE_ANGULAR_MAXIMA = 0.6
CONST_PROXIMIDADE = 0.48

def perto(array):
    for valor in array:
        if valor <= CONST_PROXIMIDADE:
            return True
        return False

class Vel_publisher(Node):
    def __init__(self):
        super().__init__('vel_publisher')

        self._publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        periodo_timer = 1
        self.timer = self.create_timer(periodo_timer, self.timer_callback)

        self.subscription = self.create_subscription(LaserScan, '/scan', self.listener_callback, 10)
        self.subscription
        self.scan = list()

    def timer_callback(self):
        msg = Twist()

        if perto(self.scan):
            msg.angular.z = VELOCIDADE_ANGULAR_MAXIMA
            msg.linear.x = 0.
        else:
            msg.angular.z = 0.
            msg.linear.x = VELOCIDADE_LINEAR_MAXIMA

        self._publisher.publish(msg)
        self.get_logger().info(f'Publicando: {msg}')

    def listener_callback(self, msg):
        self.scan = msg.ranges
        self.get_logger().info(f'SCAN: {msg}')

def main(args=None):
    rclpy.init(args=args)
    vel_publisher = Vel_publisher()
    rclpy.spin(vel_publisher)
    vel_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
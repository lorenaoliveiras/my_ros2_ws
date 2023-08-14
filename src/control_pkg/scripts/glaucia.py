import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

Twist_linear = 0.25
Twist_angular = 0.8
Aproximacao = 0.45
def close(array):
    for value in array:
        if value <= Aproximacao:
            return 1
    return 0

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.subscription =self.create_subscription(LaserScan, '/scan', self.listener_callback, 10)
        self.subscription
        self.scan = list()


    def timer_callback(self):
        msg = Twist()
        if close(self.scan):
            msg.angular.z = Twist_angular
            msg.linear.x = 0.
        else:
            msg.angular.z = 0.
            msg.linear.x = Twist_linear
        
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg}')

    def listener_callback(self, msg):
        self.scan = msg.ranges


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


#dentro da pasta src em turtlebot3_simulations abri a turtlebot3_gazebo e em models modifiquei o ângulo tanto em model-1_4.sdf quanto na model.sdf
#linhas 140 = 180
#141 = 1.0
#142 = -1.57
#143 = 1.57
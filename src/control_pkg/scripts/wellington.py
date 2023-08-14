import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

MAX_LIN_VEL = 0.22
MAX_ANG_VEL = 0.6

PROXIMITY_CONSTANT = 0.48

def close(array):
    for value in array:
        if value <= PROXIMITY_CONSTANT:
            return True
    return False
    
class Vel_publisher(Node):
    def __init__(self):
        super().__init__('vel_publisher')
        
        # pedaço como publisher
        self._publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 1 
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        # pedaço como subscriber
        self.subscription = self.create_subscription(LaserScan, '/scan', self.listener_callback, 10)
        self.subscription # pra evitar aviso de "unused variable"
        self.scan = list()
        
    # Função do publisher
    def timer_callback(self):
        msg = Twist()
        
        if close(self.scan):
            msg.angular.z = MAX_ANG_VEL
            msg.linear.x = 0.
        else:
            msg.angular.z = 0.
            msg.linear.x = MAX_LIN_VEL
            
        self._publisher.publish(msg)
        
        self.get_logger().info(f'Publishing: {msg}')
        
    
    # Função do subscriber
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
    main();
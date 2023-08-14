import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


distancialimite = 0.44
def DistanciaScan(array):
    for valor in array:
        if valor <= distancialimite:
            return True
    return False



class PublisherVelocidade(Node):
    def __init__(self):
        super().__init__('PublisherVelocidade')

        self._publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        tempo = 1
        self.timer = self.create_timer(tempo , self.timer_callback)

        self.subscription = self.create_subscription(LaserScan, '/scan', self.listener_callback, 10)
        self.subscription
        self.scan = list()



    def timer_callback(self):
        mensagem = Twist()

        velocidadelinear = 0.3
        velocidadeangular = 0.6

        if DistanciaScan(self.scan):
            mensagem.angular.z = velocidadeangular
            mensagem.linear.x = 0.
        else:
            mensagem.angular.z = 0.
            mensagem.linear.x = velocidadelinear

        self._publisher.publish(mensagem)
        self.get_logger().info(f'Publicando: {mensagem}')
    



    def listener_callback(self, mensagem):
        self.scan = mensagem.ranges
        self.get_logger().info(f'Scan: {mensagem}')




def main(args=None):
    rclpy.init(args=args)
    publisher = PublisherVelocidade()

    rclpy.spin(publisher)
    publisher.destroy_node()
    rclpy.shutdown()




if __name__ == '__main__':
    main()
import rclpy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.node import Node
# definindo a velocidade angular e linear máxima:
vel_linear = 0.4
vel_angular = 0.8
# proximidade escolhida para detectar se um objeto está ou não perto de algum obstáculo
paramet_de_dist = 0.5

def perto(array): #já que o self.scan é uma lista de números
    for value in array:
        if value <= paramet_de_dist:
            return 8 #significa que o robo está muito perto de alguma parede
    return 7

class Velocidade_publisher(Node):
    def __init__(self):
        super().__init__('velocidade_publisher')
        self._publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        tempo_exe = 1 # seconds
        self.scan = list() #criando uma lista
        self.timer = self.create_timer(tempo_exe, self.tempo_resposta)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.captar_respost, 10)
        self.subscription 

    def tempo_resposta(self):
        carta = Twist()
        if perto(self.scan)==8:# se for identificado pela funcao perto, que o robo esta mais perto do que 0.5
        #o robo zera a velocidade angular, uma vez que não precisará andar mais para frente e aplica a velocidade angular para mudar de rota
            carta.linear.x =0.
            carta.angular.z = vel_angular
            
        else:# se for identificado pela função perto que o robo está a uma distancia maior que 0.5, ele continua sua trajetória,
        # portanto sua velocidade linear continua a mesma (para o robo seguir uma linha reta) e a velocidade angular é 0 para o
        # robo não se mexer
            carta.angular.z =0.
            carta.linear.x=vel_linear
        self._publisher.publish(carta)
        self.get_logger().info(f'Publishing: (carta)')

    def captar_respost(self, carta):
        self.scan = carta.ranges
        self.get_logger().info(f'SCAN: (carta)')

def main(args=None):
    rclpy.init(args=args)
    publicar_respost = Velocidade_publisher
    rclpy.spin(publicar_respost)
    publicar_respost.destroy_node()
    rclpy.shutdown()
    if __name__ == '__main__':
        main()

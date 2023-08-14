import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist #topico do publisher
from sensor_msgs.msg import LaserScan #topico do subscriber

vam = 1.0
vlm = 0.22
distancia_seguranca = 0.5

def proximidade(array): 
    for p in array: #pega o valor p de distancia fornecido pelo scan
        if p < distancia_seguranca: #compara esse valor p com a distancia de segurança(DS), se ele for menor que a DS o veiculo segue linearmente
            return True
        else: #caso contrario, o veiculo para o movimento linear e inicia o giro para evitar a colisão
            return False

class Principal(Node):
    def __init__(self):
        #publisher
        super().__init__('publisher_subscriber')
        self.__publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        periodo = 1.2
        self.timer = self.create_timer(periodo, self.timer_callback)
        #subscriber
        self.subscription = self.create_subscription(LaserScan, '/scan' , self.listener_callback, 10)
        self.subscription
        self.scan = list()

    def timer_callback(self): #gerencia a frequencia com que a informação vai ser do publisher é publicada
        msg = Twist() #topico onde a mensagem sera publicada

        if proximidade(self.scan): #utiliza a função que avalia a proximidade do veiculo para publicar a mensagem em seus devidos topicos
            msg.angular.z = vam #coloca velocidade angular no veiculo para ele realizar o giro
            msg.linear.x = 0.0 #para o movimento em linha reta do veiculo para evitar a colisão
        else:
            msg.angular.z = 0.0 #o veiculo não realiza o giro 
            msg.linear.x = vlm #mantem o movimento do veiculo em linha reta            

        self.__publisher.publish(msg)
        self.get_logger().info(f' Publicando:  {msg}')  #exibe as mensagens no terminal
    

    def listener_callback(self, msg): #gerencia a frequencia com que a informação vai ser do subscriber é publicada
        self.scan - msg.ranges
        self.get_logger().info(f'Scan: {msg}') #publica a informação dada pelo scan

def main(args=None):
    rclpy.init(args=args)
    publisher_subscriber = Principal()
    rclpy.spin(publisher_subscriber)
    publisher_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
"""Atividade de integração de sistemas:
  Ler a uma distância publicada por "scan"
  e publicar uma velocidade para desviar de objetos
  
  Para os testes, o ângulo do sensor utilizado foi
  min: -0.8; max: 0.8
  com 360 samples"""


import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class DistSensor(Node):
  def __init__(self):
    super().__init__('navegacao')
    self.subscription_ = self.create_subscription(LaserScan, 'scan', self.scan_callback, 10)
    self.subscription_
    
    
    self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
    self.publisher_
    
      
  def scan_callback(self, msg):
    self.scan = msg.ranges
    self.Detectar_obstaculo()
    
  def Detectar_obstaculo(self):
    dist_min = min(self.scan)
    index_min = self.scan.index(dist_min)
    twist = Twist()
    
    if dist_min < 0.22:
      self.Desviar(index_min)
    else:  
      twist.linear.x = 0.3
      twist.angular.z = 0.0
      self.publisher_.publish(twist)
      self.get_logger().info('Velocidade linear x: "%f", velocidade angular z:  "%f"'%(twist.linear.x, twist.angular.z))
    
  def Desviar(self, index_min):
    twist = Twist()
    twist.linear.x = 0.0
    area1 = sum(self.scan[0:index_min])
    area2 = sum(self.scan[index_min:0])
    if area1 > area2:
      twist.angular.z = -0.3
    else:
      twist.angular.z = 0.3
    
    self.publisher_.publish(twist)
    self.get_logger().info('Velocidade linear x: "%f", velocidade angular z:  "%f"'%(twist.linear.x, twist.angular.z))
    

    
def main(args=None):
  rclpy.init(args=args)
  
  disp_sub = DistSensor()
  rclpy.spin(disp_sub)
  disp_sub.destroy_node()
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()
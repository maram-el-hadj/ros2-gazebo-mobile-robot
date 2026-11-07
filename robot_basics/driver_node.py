import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class DriverNode(Node):
    def __init__(self):
        super().__init__('driver_node')

        # Publisher: on envoie des commandes de vitesse
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Subscriber: on lit la position du robot
        self.sub = self.create_subscription(Odometry, '/odom', self.odom_cb, 10)

        # Timer: on envoie une commande toutes les 0.1 s
        self.timer = self.create_timer(0.1, self.timer_cb)

        self.x = 0.0
        self.y = 0.0
        self.target_x = 2.0

    def odom_cb(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

    def timer_cb(self):
        cmd = Twist()
        if self.x < self.target_x:
            cmd.linear.x = 0.2
        else:
            cmd.linear.x = 0.0
        self.pub.publish(cmd)
        self.get_logger().info(
            f'x={self.x:.2f} y={self.y:.2f}', throttle_duration_sec=1.0)


def main():
    rclpy.init()
    node = DriverNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

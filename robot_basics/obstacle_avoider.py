import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

SAFE_DIST = 0.7        # m : obstacle devant -> on tourne
CLEAR_DIST = 0.95      # m : on arrete de tourner au-dessus
LINEAR_SPEED = 0.4     # m/s
ANGULAR_SPEED = 0.8    # rad/s


class ObstacleAvoider(Node):
    def __init__(self):
        super().__init__('obstacle_avoider')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.sub = self.create_subscription(
            LaserScan, '/scan', self.scan_cb, 10)
        self.turning = False
        self.turn_dir = 1.0

    def sector_min(self, msg, a_start, a_end):
        best = msg.range_max
        for i, r in enumerate(msg.ranges):
            angle = msg.angle_min + i * msg.angle_increment
            if a_start <= angle <= a_end:
                if math.isfinite(r) and msg.range_min <= r < best:
                    best = r
        return best

    def scan_cb(self, msg):
        front = self.sector_min(msg, math.radians(-30), math.radians(30))
        left = self.sector_min(msg, math.radians(30), math.radians(90))
        right = self.sector_min(msg, math.radians(-90), math.radians(-30))

        if self.turning:
            if front > CLEAR_DIST:
                self.turning = False
        elif front < SAFE_DIST:
            self.turning = True
            self.turn_dir = 1.0 if left > right else -1.0

        cmd = Twist()
        if self.turning:
            cmd.angular.z = ANGULAR_SPEED * self.turn_dir
            state = 'TURN'
        else:
            cmd.linear.x = LINEAR_SPEED
            state = 'FORWARD'

        self.pub.publish(cmd)
        self.get_logger().info(
            f'{state} front={front:.2f} left={left:.2f} right={right:.2f}',
            throttle_duration_sec=1.0)


def main():
    rclpy.init()
    node = ObstacleAvoider()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

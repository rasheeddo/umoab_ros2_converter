
import rclpy
from rclpy.node import Node

from std_msgs.msg import UInt8MultiArray, Int16MultiArray, Int32MultiArray, Float32MultiArray
from std_msgs.msg import Int8, Bool
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix


class PUBSUB(Node):

	def __init__(self):

		super().__init__('umoab_ros2_converter_pubsub')

		self.get_logger().info('Start UMOAB ROS2 converter node')

		# self.array_pub = self.create_publisher(Int32MultiArray, 'array', 10)
		# self.int_pub = self.create_publisher(Int32, 'int', 10)
		# self.bool_pub = self.create_publisher(Bool, 'bool', 10)

		# self.array_msg = Int32MultiArray()
		# self.int_msg = Int32()
		# self.bool_msg = Bool()

		self.ch1 = 1024
		self.ch2 = 1024
		self.ch3 = 1024

		self.i = 0
		self.togle = True

		self.cart_mode_sub = self.create_subscription(Int8, 'umoab/cart_mode', self.cart_mode_callback, 10)
		self.sbus_rc_sub = self.create_subscription(Int16MultiArray, 'umoab/sbus_rc_ch', self.sbus_rc_callback, 10)
		self.adc_sub = self.create_subscription(Float32MultiArray, 'umoab/adc', self.adc_callback, 10)
		self.hall_sub = self.create_subscription(Int32MultiArray, 'umoab/hall_count', self.hall_callback, 10)
		self.gps_sub = self.create_subscription(NavSatFix, 'umoab/gps', self.gps_callback, 10)
		self.imu_sub = self.create_subscription(Imu, 'umoab/imu', self.imu_callback, 10)
		

		self.led_pub = self.create_publisher(UInt8MultiArray, 'umoab/led', 10)
		self.cart_cmd_pub = self.create_publisher(Int16MultiArray, 'umoab/cart_cmd', 10)
		self.relay_pub = self.create_publisher(Bool, 'umoab/relay', 10)
		self.servo_pub = self.create_publisher(Int16MultiArray, 'umoab/servo', 10)


		timer_period = 0.1
		self.timer = self.create_timer(timer_period, self.timer_callback)

	def cart_mode_callback(self, msg):
		pass
		# print("cart_mode", msg.data)
		# print(msg.data[0], msg.data[1], msg.data[2])

	def sbus_rc_callback(self, msg):
		pass

	def adc_callback(self, msg):
		pass

	def hall_callback(self, msg):
		pass

	def gps_callback(self, msg):
		pass

	def imu_callback(self, msg):
		pass

	def timer_callback(self):

		pass

def main(args=None):

	rclpy.init(args=args)

	node = PUBSUB()

	rclpy.spin(node)

	node.destroy_node()
	rclpy.shutdownn()


if __name__ == "__main__":

	main()
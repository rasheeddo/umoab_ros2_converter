
import rclpy
from rclpy.node import Node
from numpy import pi
from sensor_msgs.msg import Imu
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from geometry_msgs.msg import Quaternion
from tf_transformations import quaternion_from_euler, quaternion_multiply, euler_from_quaternion
from transforms3d.quaternions import mat2quat, quat2mat

class IMU_VIS(Node):

	def __init__(self):

		super().__init__('imu_visualization_node')

		self.get_logger().info('Start IMU visualization node')
		self.get_logger().info('Open rviz2 and add MarkerArray with /umoab/imu_marker topic')

		self.imu_sub = self.create_subscription(Imu, 'umoab/imu', self.imu_callback, 10)

		# self.q_orig = Quaternion()


		self.marker_arr_pub = self.create_publisher(MarkerArray, 'umoab/imu_marker', 10)
		self.marker_arr_msg = MarkerArray()
		# self.marker_pub = self.create_publisher(Marker, 'umoab/imu_marker', 10)
		self.box_msg = Marker()
		self.box_msg.ns = "box"
		self.box_msg.header.frame_id = 'map'
		self.box_msg.header.stamp = self.get_clock().now().to_msg()
		self.box_msg.type = Marker.CUBE
		self.box_msg.id = 1
		self.box_msg.action = 0
		self.box_msg.pose.position.x = 0.0
		self.box_msg.pose.position.y = 0.0
		self.box_msg.pose.position.z = 0.0
		self.box_msg.scale.x = 1.0
		self.box_msg.scale.y = 1.0
		self.box_msg.scale.z = 1.0
		self.box_msg.color.r = 1.0
		self.box_msg.color.g = 0.0
		self.box_msg.color.b = 0.0
		self.box_msg.color.a = 1.0

		self.arrow_x_msg = Marker()
		self.arrow_x_msg.ns = "arrow_x"
		self.arrow_x_msg.header.frame_id = 'map'
		self.arrow_x_msg.header.stamp = self.get_clock().now().to_msg()
		self.arrow_x_msg.type = Marker.ARROW
		self.arrow_x_msg.id = 1
		self.arrow_x_msg.action = 0
		self.arrow_x_msg.pose.position.x = 0.0
		self.arrow_x_msg.pose.position.y = 0.0
		self.arrow_x_msg.pose.position.z = 0.0
		self.arrow_x_msg.scale.x = 2.0
		self.arrow_x_msg.scale.y = 0.2
		self.arrow_x_msg.scale.z = 0.2
		self.arrow_x_msg.color.r = 1.0
		self.arrow_x_msg.color.g = 0.0
		self.arrow_x_msg.color.b = 0.0
		self.arrow_x_msg.color.a = 1.0

		self.arrow_y_msg = Marker()
		self.arrow_y_msg.ns = "arrow_y"
		self.arrow_y_msg.header.frame_id = 'map'
		self.arrow_y_msg.header.stamp = self.get_clock().now().to_msg()
		self.arrow_y_msg.type = Marker.ARROW
		self.arrow_y_msg.id = 1
		self.arrow_y_msg.action = 0
		self.arrow_y_msg.pose.position.x = 0.0
		self.arrow_y_msg.pose.position.y = 0.0
		self.arrow_y_msg.pose.position.z = 0.0
		self.arrow_y_msg.scale.x = 2.0
		self.arrow_y_msg.scale.y = 0.2
		self.arrow_y_msg.scale.z = 0.2
		self.arrow_y_msg.color.r = 0.0
		self.arrow_y_msg.color.g = 1.0
		self.arrow_y_msg.color.b = 0.0
		self.arrow_y_msg.color.a = 1.0

		self.arrow_z_msg = Marker()
		self.arrow_z_msg.ns = "arrow_z"
		self.arrow_z_msg.header.frame_id = 'map'
		self.arrow_z_msg.header.stamp = self.get_clock().now().to_msg()
		self.arrow_z_msg.type = Marker.ARROW
		self.arrow_z_msg.id = 1
		self.arrow_z_msg.action = 0
		self.arrow_z_msg.pose.position.x = 0.0
		self.arrow_z_msg.pose.position.y = 0.0
		self.arrow_z_msg.pose.position.z = 0.0
		self.arrow_z_msg.scale.x = 2.0
		self.arrow_z_msg.scale.y = 0.2
		self.arrow_z_msg.scale.z = 0.2
		self.arrow_z_msg.color.r = 0.0
		self.arrow_z_msg.color.g = 0.0
		self.arrow_z_msg.color.b = 1.0
		self.arrow_z_msg.color.a = 1.0




		timer_period = 0.01
		# self.timer = self.create_timer(timer_period, self.timer_callback)

	# def timer_callback(self):
		#pass

	def imu_callback(self, msg):

		# self.q_orig.x = msg.orientation.x
		# self.q_orig.y = msg.orientation.y
		# self.q_orig.z = msg.orientation.z
		# self.q_orig.w = msg.orientation.w

		self.box_msg.pose.orientation.x = msg.orientation.x
		self.box_msg.pose.orientation.y = msg.orientation.y
		self.box_msg.pose.orientation.z = msg.orientation.z
		self.box_msg.pose.orientation.w = msg.orientation.w

		self.arrow_x_msg.pose.orientation.x = msg.orientation.x
		self.arrow_x_msg.pose.orientation.y = msg.orientation.y
		self.arrow_x_msg.pose.orientation.z = msg.orientation.z
		self.arrow_x_msg.pose.orientation.w = msg.orientation.w

		q_orig = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]

		q_rot_y = quaternion_from_euler(0, 0, pi/2)
		q_rot_z = quaternion_from_euler(0, -pi/2, 0)

		# If we want to get a new rotation from relative to previos axis ref, not world fix axes ref.
		# the multiply order should be original_q * rotation_of_current_axes_ref
		# But if we want to get new rotation q as rotate along world fixed axes,
		# the multiply order should be rotation_along_fixed_axes * original_q
		# check on this video below, 4:25-6:12
		# https://www.youtube.com/watch?v=0FbDyWXemLw&ab_channel=LeopoldoArmesto
		q_y =  quaternion_multiply(q_orig, q_rot_y)
		q_z =  quaternion_multiply(q_orig, q_rot_z)

		self.arrow_y_msg.pose.orientation.x = q_y[0]
		self.arrow_y_msg.pose.orientation.y = q_y[1]
		self.arrow_y_msg.pose.orientation.z = q_y[2]
		self.arrow_y_msg.pose.orientation.w = q_y[3]

		self.arrow_z_msg.pose.orientation.x = q_z[0]
		self.arrow_z_msg.pose.orientation.y = q_z[1]
		self.arrow_z_msg.pose.orientation.z = q_z[2]
		self.arrow_z_msg.pose.orientation.w = q_z[3]


		self.marker_arr_msg.markers.append(self.box_msg)
		self.marker_arr_msg.markers.append(self.arrow_x_msg)
		self.marker_arr_msg.markers.append(self.arrow_y_msg)
		self.marker_arr_msg.markers.append(self.arrow_z_msg)


		self.marker_arr_pub.publish(self.marker_arr_msg)


def main(args=None):

	rclpy.init(args=args)

	node = IMU_VIS()

	rclpy.spin(node)

	node.destroy_node()
	rclpy.shutdownn()


if __name__ == "__main__":

	main()
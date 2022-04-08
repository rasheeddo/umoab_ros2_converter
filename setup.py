from setuptools import setup

package_name = 'umoab_ros2_converter'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rasheed',
    maintainer_email='rasheedo.kit@gmail.com',
    description='A conversion package of UMOAB ROS1 to ROS2',
    license='GPLv3',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'pubsub = umoab_ros2_converter.pubsub:main',
        'imu_vis = umoab_ros2_converter.imu_vis:main'
        ],
    },
)

from setuptools import find_packages, setup
from glob import glob

package_name = 'ex01_simple_urdf'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/description',
         glob('description/*.urdf.xacro')),
        ('share/' + package_name + '/description/rviz',
         glob('description/rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ggn0',
    maintainer_email='luigi.s1994@gmail.com',
    description='Showcase a basic example URDF robot description.',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)

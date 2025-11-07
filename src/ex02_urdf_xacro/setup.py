from setuptools import find_packages, setup
from glob import glob

package_name = 'ex02_urdf_xacro'

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
         glob('description/*.xacro')),
        ('share/' + package_name + '/description/rviz',
         glob('description/rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ggn0',
    maintainer_email='luigi.s1994@gmail.com',
    description='Showcase a parametric example of URDF robot description \
        using xml macros.',
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

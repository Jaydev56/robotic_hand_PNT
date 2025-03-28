from setuptools import setup, find_packages

setup(
    name='robotic_hand_library',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A library for controlling a robotic hand using hand tracking.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/robotic_hand_library',
    packages=find_packages(),
    install_requires=[
        'mediapipe',
        'opencv-python',
        'numpy',
        'pyserial',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
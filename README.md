# Robotic Hand Library

## Overview
The Robotic Hand Library provides an easy-to-use interface for controlling a robotic hand using hand tracking technology. This library is designed for students and beginners to facilitate the integration of hand tracking with robotic hand movements.

## Features
- Connects to an Arduino to control a robotic hand.
- Processes hand landmarks using MediaPipe for real-time tracking.
- Calculates finger angles and thumb servo angles for precise control.
- Simple examples and tests to help users get started quickly.

## Installation
To install the Robotic Hand Library, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/robotic_hand_library.git
   cd robotic_hand_library
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the setup script to install the library:
   ```
   python setup.py install
   ```

## Usage
To use the Robotic Hand Library, you can refer to the `examples/basic_usage.py` file for a simple demonstration. Here’s a brief overview of how to use the `HandController` class:

```python
from robotic_hand.hand_controller import HandController

# Initialize the HandController
controller = HandController(port="COM5")

# Start capturing video and processing hand landmarks
controller.start()
```

## Testing
To run the tests for the library, navigate to the `tests` directory and execute the following command:

```
python -m unittest discover
```

## Contributing
Contributions are welcome! If you have suggestions or improvements, please create a pull request or open an issue.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
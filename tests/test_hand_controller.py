import unittest
from robotic_hand.hand_controller import HandController

class TestHandController(unittest.TestCase):

    def setUp(self):
        self.controller = HandController("COM5")

    def test_connect_arduino(self):
        self.assertIsNotNone(self.controller.arduino)

    def test_get_finger_angles(self):
        # Mock landmarks for testing
        class MockLandmarks:
            class Landmark:
                def __init__(self, x, y):
                    self.x = x
                    self.y = y
            landmark = [MockLandmarks.Landmark(0.5, 0.5) for _ in range(21)]

        angles = self.controller.get_finger_angles(MockLandmarks(), 640, 480)
        self.assertEqual(len(angles), 5)

    def test_calculate_thumb_angle(self):
        # Mock landmarks for testing
        class MockLandmarks:
            class Landmark:
                def __init__(self, x, y):
                    self.x = x
                    self.y = y
            landmark = [MockLandmarks.Landmark(0.5, 0.5) for _ in range(21)]

        thumb_angle = self.controller.calculate_thumb_angle(MockLandmarks(), 640, 480, None)
        self.assertGreaterEqual(thumb_angle, 0)
        self.assertLessEqual(thumb_angle, 90)

if __name__ == '__main__':
    unittest.main()
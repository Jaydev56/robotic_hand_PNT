import asyncio
from bleak import BleakScanner, BleakClient
import socket

BLE_DEVICE_ADDRESS = "A0:85:E3:4E:E5:FE"  # Replace with your BLE device address
CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

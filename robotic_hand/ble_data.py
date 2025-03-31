import asyncio
from bleak import BleakScanner, BleakClient

BLE_DEVICE_ADDRESS = "A0:85:E3:4E:E5:FC"  # Replace with your BLE device address
CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

class BLEData:
    def __init__(self):
        self.client = None

    async def connect_ble(self):
        """Scan and connect to BLE device."""
        print("Scanning for BLE devices...")
        devices = await BleakScanner.discover()
        for device in devices:
            print(f"Found: {device.name or 'Unknown'} - {device.address}")
            if device.address.lower() == BLE_DEVICE_ADDRESS.lower():
                self.client = BleakClient(device.address)
                await self.client.connect()
                print(f"Connected to BLE device: {device.address}")
                return True
        print("BLE device not found.")
        return False

    async def handle_ble_data(self, _, data):
        """Handle incoming BLE data and print it."""
        decoded_data = data.decode().strip()
        print(f"Received from BLE: {decoded_data}")

    async def receive_data(self):
        """Start receiving BLE data."""
        if not self.client:
            print("BLE client is not connected.")
            return

        await self.client.start_notify(CHAR_UUID, self.handle_ble_data)
        print("Listening for BLE notifications...")
        try:
            while True:
                await asyncio.sleep(1)  # Keep running
        except asyncio.CancelledError:
            print("BLE data reception stopped.")
        finally:
            await self.client.stop_notify(CHAR_UUID)

async def main():
    ble_data = BLEData()
    if await ble_data.connect_ble():
        await ble_data.receive_data()

if __name__ == "__main__":
    asyncio.run(main())

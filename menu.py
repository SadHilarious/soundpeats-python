"""
Soundpeats Capsule3 Pro+ Complete Controller v3
+ Battery Reading Fix
"""

import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime
import json

SERVICE_UUID = "0000a001-0000-1000-8000-00805f9b34fb"
WRITE_UUID = "00001001-0000-1000-8000-00805f9b34fb"
NOTIFY_UUID = "00001002-0000-1000-8000-00805f9b34fb"
BATTERY_UUID = "00000008-0000-1000-8000-00805f9b34fb"

# Discovered patterns
COMMANDS = {
    'anc': bytes([0xFF, 0x03, 0x0C, 0x01, 0x63]),
    'passthrough': bytes([0xFF, 0x03, 0x0C, 0x01, 0xA5]),
    'normal': bytes([0xFF, 0x03, 0x0C, 0x01, 0x02]),
    'game_on': bytes([0xFF, 0x03, 0x09, 0x01, 0x01]),
    'game_off': bytes([0xFF, 0x03, 0x09, 0x01, 0x02]),
}

class SoundpeatsController:
    def __init__(self):
        self.client = None
        self.device = None
        self.write_char = None
        self.battery_char = None
        self.current_mode = None
        self.battery_info = {
            'left': None,
            'right': None,
            'case': None
        }
        
    async def find_device(self):
        print("🔍 Finding earbuds...")
        devices = await BleakScanner.discover(timeout=10.0)
        for device in devices:
            if device.name and "QCY" in device.name:
                self.device = device
                print(f"✓ Found: {device.name}\n")
                return True
        return False
    
    async def connect(self):
        if not self.device and not await self.find_device():
            return False
        
        try:
            self.client = BleakClient(self.device)
            await self.client.connect()
            print("✓ Connected!\n")
            
            # Get write characteristic & battery characteristic
            for service in self.client.services:
                if service.uuid == SERVICE_UUID:
                    for char in service.characteristics:
                        if char.uuid == WRITE_UUID:
                            self.write_char = char
                        elif char.uuid == BATTERY_UUID:
                            self.battery_char = char
            
            if not self.write_char:
                print("✗ Write characteristic not found!")
                return False
            
            if not self.battery_char:
                print("⚠️  Battery characteristic not found!")
            
            return True
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    async def get_battery(self):
        """Read battery percentage - FIXED VERSION"""
        if not self.battery_char:
            print("✗ Battery characteristic not available!")
            return False
        
        try:
            data = await self.client.read_gatt_char(self.battery_char)
            
            # Format: 3 bytes [left, right, case]
            if len(data) >= 3:
                self.battery_info['left'] = data[0]
                self.battery_info['right'] = data[1]
                
                # If byte[2] = 0, case may not be sending data
                case_value = data[2]
                
                if case_value == 0:
                    self.battery_info['case'] = 0  # Case offline/off
                else:
                    self.battery_info['case'] = case_value
                
                return True
            else:
                print("✗ Invalid battery data!")
                print(f"   Received {len(data)} bytes, need 3 bytes")
                return False
        except Exception as e:
            print(f"✗ Battery read error: {e}")
            return False
    
    def show_battery(self):
        """Display battery information - UPDATED"""
        if self.battery_info['left'] is None:
            print("⚠️  Battery info not read yet. Press 'View Battery' first!\n")
            return
        
        print("\n" + "="*60)
        print("🔋 BATTERY INFORMATION")
        print("="*60 + "\n")
        
        # Display left earbud battery
        left_status = self._get_battery_status(self.battery_info['left'])
        print(f"👂 Left Earbud:   {self.battery_info['left']:3d}%  {left_status}")
        
        # Display right earbud battery
        right_status = self._get_battery_status(self.battery_info['right'])
        print(f"👂 Right Earbud:  {self.battery_info['right']:3d}%  {right_status}")
        
        # Display case battery
        case_value = self.battery_info['case']
        if case_value == 0:
            print(f"📦 Case:         --   ⚪ Offline (Case powered off)")
        else:
            case_status = self._get_battery_status(case_value)
            print(f"📦 Case:         {case_value:3d}%  {case_status}")
        
        # Calculate average battery (earbuds only if case offline)
        if case_value == 0:
            avg_battery = (self.battery_info['left'] + self.battery_info['right']) // 2
            print(f"\n   📊 Average (Earbuds): {avg_battery}%")
        else:
            avg_battery = (self.battery_info['left'] + self.battery_info['right'] + case_value) // 3
            print(f"\n   📊 Average (All): {avg_battery}%")
        
        print()
    
    def _get_battery_status(self, percentage):
        """Display icon & battery status"""
        if percentage is None or percentage < 0:
            return "❓ Unknown"
        elif percentage >= 80:
            return "🟢 Excellent"
        elif percentage >= 50:
            return "🟡 Good"
        elif percentage >= 20:
            return "🟠 Low"
        else:
            return "🔴 Critical (needs charging)"
    
    async def set_anc_mode(self, mode):
        """Change ANC mode"""
        if mode not in ['normal', 'anc', 'passthrough']:
            print(f"✗ Invalid mode: {mode}")
            return False
        
        command = COMMANDS[mode]
        hex_cmd = ' '.join(f'{b:02x}' for b in command)
        
        print(f"📤 Changing mode: {mode.upper()}")
        print(f"   Command: {hex_cmd}")
        
        try:
            await self.client.write_gatt_char(self.write_char, command)
            print(f"   ✓ Success!\n")
            self.current_mode = mode
            return True
        except Exception as e:
            print(f"   ✗ Error: {e}\n")
            return False
    
    async def set_game_mode(self, enabled):
        """Enable/Disable Game Mode"""
        mode = 'game_on' if enabled else 'game_off'
        command = COMMANDS[mode]
        hex_cmd = ' '.join(f'{b:02x}' for b in command)
        
        status = "ENABLE" if enabled else "DISABLE"
        print(f"🎮 {status} Game Mode")
        print(f"   Command: {hex_cmd}")
        
        try:
            await self.client.write_gatt_char(self.write_char, command)
            print(f"   ✓ Success!\n")
            return True
        except Exception as e:
            print(f"   ✗ Error: {e}\n")
            return False
    
    async def disconnect(self):
        if self.client:
            await self.client.disconnect()
            print("✓ Disconnected")

async def menu():
    """Interactive menu"""
    controller = SoundpeatsController()
    
    if not await controller.connect():
        return
    
    try:
        while True:
            print("="*60)
            print("🎧 SOUNDPEATS CAPSULE3 PRO+ CONTROLLER")
            print("="*60)
            print("\n📋 MENU:\n")
            print("1. ANC Mode (Noise Cancellation)")
            print("2. Passthrough Mode (Ambient Sound)")
            print("3. Normal Mode (ANC Off)")
            print("4. Enable Game Mode")
            print("5. Disable Game Mode")
            print("6. 🔋 View Battery & Charging Status")
            print("7. Exit")
            
            choice = input("\n>>> Select (1-7): ").strip()
            
            if choice == '1':
                await controller.set_anc_mode('anc')
            elif choice == '2':
                await controller.set_anc_mode('passthrough')
            elif choice == '3':
                await controller.set_anc_mode('normal')
            elif choice == '4':
                await controller.set_game_mode(True)
            elif choice == '5':
                await controller.set_game_mode(False)
            elif choice == '6':
                # Read battery
                print("\n📡 Reading battery information...")
                if await controller.get_battery():
                    controller.show_battery()
                else:
                    print("✗ Cannot read battery information!\n")
            elif choice == '7':
                print("\n👋 Exiting...")
                break
            else:
                print("✗ Invalid selection!\n")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted")
    finally:
        await controller.disconnect()

if __name__ == "__main__":
    asyncio.run(menu())

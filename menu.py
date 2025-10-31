"""
Soundpeats Capsule3 Pro+ Complete Controller v3
+ Fix Battery Reading
"""

import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime
import json

SERVICE_UUID = "0000a001-0000-1000-8000-00805f9b34fb"
WRITE_UUID = "00001001-0000-1000-8000-00805f9b34fb"
NOTIFY_UUID = "00001002-0000-1000-8000-00805f9b34fb"
BATTERY_UUID = "00000008-0000-1000-8000-00805f9b34fb"

# Patterns đã tìm được
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
        print("🔍 Tìm tai nghe...")
        devices = await BleakScanner.discover(timeout=10.0)
        for device in devices:
            if device.name and "QCY" in device.name:
                self.device = device
                print(f"✓ Tìm thấy: {device.name}\n")
                return True
        return False
    
    async def connect(self):
        if not self.device and not await self.find_device():
            return False
        
        try:
            self.client = BleakClient(self.device)
            await self.client.connect()
            print("✓ Đã kết nối!\n")
            
            # Lấy write characteristic & battery characteristic
            for service in self.client.services:
                if service.uuid == SERVICE_UUID:
                    for char in service.characteristics:
                        if char.uuid == WRITE_UUID:
                            self.write_char = char
                        elif char.uuid == BATTERY_UUID:
                            self.battery_char = char
            
            if not self.write_char:
                print("✗ Không tìm thấy write characteristic!")
                return False
            
            if not self.battery_char:
                print("⚠️  Không tìm thấy battery characteristic!")
            
            return True
        except Exception as e:
            print(f"✗ Lỗi: {e}")
            return False
    
    async def get_battery(self):
        """Đọc phần trăm pin - FIX VERSION"""
        if not self.battery_char:
            print("✗ Battery characteristic không khả dụng!")
            return False
        
        try:
            data = await self.client.read_gatt_char(self.battery_char)
            
            # Format: 3 bytes [left, right, case]
            if len(data) >= 3:
                self.battery_info['left'] = data[0]
                self.battery_info['right'] = data[1]
                
                # Nếu byte[2] = 0, có thể hộp chưa ghi dữ liệu
                # Thử chuyển đổi từ hex thành decimal đúng
                case_value = data[2]
                
                # Nếu case_value là 0, có thể nó chưa gửi
                # Hoặc nó được mã hóa khác
                if case_value == 0:
                    # Thử cách khác: lấy từ data thô
                    # Có thể là hex encoding: 0x00 = offline
                    self.battery_info['case'] = 0  # Hộp offline/off
                else:
                    self.battery_info['case'] = case_value
                
                return True
            else:
                print("✗ Dữ liệu pin không hợp lệ!")
                print(f"   Nhận được {len(data)} bytes, cần 3 bytes")
                return False
        except Exception as e:
            print(f"✗ Lỗi đọc pin: {e}")
            return False
    
    def show_battery(self):
        """Hiển thị thông tin pin - CẬP NHẬT"""
        if self.battery_info['left'] is None:
            print("⚠️  Chưa đọc được thông tin pin. Hãy bấm 'Xem Pin' trước!\n")
            return
        
        print("\n" + "="*60)
        print("🔋 THÔNG TIN PIN")
        print("="*60 + "\n")
        
        # Hiển thị pin tai trái
        left_status = self._get_battery_status(self.battery_info['left'])
        print(f"👂 Tai Trái:  {self.battery_info['left']:3d}%  {left_status}")
        
        # Hiển thị pin tai phải
        right_status = self._get_battery_status(self.battery_info['right'])
        print(f"👂 Tai Phải:  {self.battery_info['right']:3d}%  {right_status}")
        
        # Hiển thị pin hộp
        case_value = self.battery_info['case']
        if case_value == 0:
            print(f"📦 Hộp:      --   ⚪ Offline (Hộp tắt)")
        else:
            case_status = self._get_battery_status(case_value)
            print(f"📦 Hộp:      {case_value:3d}%  {case_status}")
        
        # Tính tổng pin trung bình (chỉ tính tai + hộp nếu có)
        if case_value == 0:
            avg_battery = (self.battery_info['left'] + self.battery_info['right']) // 2
            print(f"\n   📊 Trung bình (Tai): {avg_battery}%")
        else:
            avg_battery = (self.battery_info['left'] + self.battery_info['right'] + case_value) // 3
            print(f"\n   📊 Trung bình (Tất cả): {avg_battery}%")
        
        print()
    
    def _get_battery_status(self, percentage):
        """Hiển thị icon & status pin"""
        if percentage is None or percentage < 0:
            return "❓ Không xác định"
        elif percentage >= 80:
            return "🟢 Rất tốt"
        elif percentage >= 50:
            return "🟡 Bình thường"
        elif percentage >= 20:
            return "🟠 Yếu"
        else:
            return "🔴 Rất yếu (cần sạc)"
    
    async def set_anc_mode(self, mode):
        """Đổi ANC mode"""
        if mode not in ['normal', 'anc', 'passthrough']:
            print(f"✗ Mode không hợp lệ: {mode}")
            return False
        
        command = COMMANDS[mode]
        hex_cmd = ' '.join(f'{b:02x}' for b in command)
        
        print(f"📤 Đổi mode: {mode.upper()}")
        print(f"   Command: {hex_cmd}")
        
        try:
            await self.client.write_gatt_char(self.write_char, command)
            print(f"   ✓ Thành công!\n")
            self.current_mode = mode
            return True
        except Exception as e:
            print(f"   ✗ Lỗi: {e}\n")
            return False
    
    async def set_game_mode(self, enabled):
        """Bật/tắt Game Mode"""
        mode = 'game_on' if enabled else 'game_off'
        command = COMMANDS[mode]
        hex_cmd = ' '.join(f'{b:02x}' for b in command)
        
        status = "BẬT" if enabled else "TẮT"
        print(f"🎮 {status} Game Mode")
        print(f"   Command: {hex_cmd}")
        
        try:
            await self.client.write_gatt_char(self.write_char, command)
            print(f"   ✓ Thành công!\n")
            return True
        except Exception as e:
            print(f"   ✗ Lỗi: {e}\n")
            return False
    
    async def disconnect(self):
        if self.client:
            await self.client.disconnect()
            print("✓ Đã ngắt kết nối")

async def menu():
    """Menu tương tác"""
    controller = SoundpeatsController()
    
    if not await controller.connect():
        return
    
    try:
        while True:
            print("="*60)
            print("🎧 SOUNDPEATS CAPSULE3 PRO+ CONTROLLER")
            print("="*60)
            print("\n📋 MENU:\n")
            print("1. Chế độ ANC (Chặn tiếng ồn)")
            print("2. Chế độ Passthrough (Xuyên âm)")
            print("3. Chế độ Normal (Tắt ANC)")
            print("4. Bật Game Mode")
            print("5. Tắt Game Mode")
            print("6. 🔋 Xem Pin & Dọc Sạc")
            print("7. Thoát")
            
            choice = input("\n>>> Chọn (1-7): ").strip()
            
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
                # Đọc pin
                print("\n📡 Đang đọc thông tin pin...")
                if await controller.get_battery():
                    controller.show_battery()
                else:
                    print("✗ Không thể đọc thông tin pin!\n")
            elif choice == '7':
                print("\n👋 Thoát...")
                break
            else:
                print("✗ Lựa chọn không hợp lệ!\n")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Dừng")
    finally:
        await controller.disconnect()

if __name__ == "__main__":
    asyncio.run(menu())

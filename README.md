# 🎧 SoundPEATS Capsule3 Pro+ - Technical Information Summary

## ENTIRE REPOSITORY CREATED BY AI
- **Created by**: Perplexity (Claude Sonnet 4.5 reasoning)

***
## How to use this vibe coded shit
run menu.py 

## 📋 Basic Specifications

| Specification | Details |
|---|---|
| **Model** | SoundPEATS Capsule3 Pro+ |
| **Chipset** | WQ7034AX |
| **Firmware** | SPTS04PRO_20241009_V15 |
| **Driver** | xMEMS Speaker + 12mm Bio-diaphragm Dynamic Driver (Hybrid) |
| **Bluetooth** | 5.3 (A2DP/AVRCP/HFP/HSP) |
| **Codec** | LDAC (Hi-Res), AAC, SBC |
| **Frequency Response** | 20Hz - 40kHz (Hi-Res Audio Certified) |
| **Sensitivity** | 102 dB |
| **ANC** | AI Adaptive, up to 45dB (1.8kHz bandwidth) |
| **Microphones** | 6 (3 per earbud - ENC & AptX Voice) |
| **Latency** | 70ms (Game Mode) |
| **Waterproof** | IPX4 (Sweat & Water Resistant) |
| **Touch Controls** | Yes, customizable via app |
| **Multi-point Pairing** | Yes (2 devices simultaneously) |

***

## 🔋 Battery & Charging Information

| Specification | Details |
|---|---|
| **Earbud Capacity** | 35mAh × 2 |
| **Case Capacity** | 500mAh |
| **Charging Time** | < 1.5 hours (earbuds & case) |
| **Playtime** | 6.5 hours (Normal Mode) |
| **Playtime with ANC** | Up to 8 hours |
| **Total Playtime** | 43 hours (with case) |
| **Charging Port** | USB Type-C |

***

## 🔌 Addresses & Important UUIDs

### Device Info
```
MAC Address:    C4:AC:60:78:AA:89
Device Name:    QCY-APP
Model Code:     WQ00
Device Type:    QCY-APP (SoundPEATS Capsule3 Pro+)
```

### Bluetooth Services & Characteristics
```
Main Service UUID:  0000a001-0000-1000-8000-00805f9b34fb

├── Write Characteristic (Commands)
│   UUID:        00001001-0000-1000-8000-00805f9b34fb
│   Handle:      20
│   Properties:  WRITE NO RESPONSE
│   
├── Notify Characteristic (Responses)
│   UUID:        00001002-0000-1000-8000-00805f9b34fb
│   Handle:      22
│   Properties:  NOTIFY, READ
│   
├── Battery Characteristic
│   UUID:        00000008-0000-1000-8000-00805f9b34fb
│   Handle:      25
│   Properties:  READ, NOTIFY
│   Format:      3 bytes [Left%, Right%, Case%]
│   
├── Firmware Characteristic
│   UUID:        00000007-0000-1000-8000-00805f9b34fb
│   Handle:      28
│   Properties:  READ
│   
└── Model Characteristic
    UUID:        00000009-0000-1000-8000-00805f9b34fb
    Handle:      34
    Properties:  READ
```

***

## 🎚️ ANC & Mode Control Patterns

### ANC Modes (Category: 0x0C)

| Mode | Command (Hex) | Bytes | Meaning |
|---|---|---|---|
| **ANC ON** | `ff 03 0c 01 63` | `[0xFF, 0x03, 0x0C, 0x01, 0x63]` | Noise cancellation mode |
| **Passthrough** | `ff 03 0c 01 a5` | `[0xFF, 0x03, 0x0C, 0x01, 0xA5]` | Ambient sound pass-through |
| **Normal (Off)** | `ff 03 0c 01 02` | `[0xFF, 0x03, 0x0C, 0x01, 0x02]` | ANC disabled |

### Game Mode (Category: 0x09)

| Mode | Command (Hex) | Bytes | Meaning |
|---|---|---|---|
| **Game ON** | `ff 03 09 01 01` | `[0xFF, 0x03, 0x09, 0x01, 0x01]` | Game mode enabled (70ms latency) |
| **Game OFF** | `ff 03 09 01 02` | `[0xFF, 0x03, 0x09, 0x01, 0x02]` | Game mode disabled |

### Command Structure
```
Byte[0]: 0xFF   - Header
Byte[1]: 0x03   - Subheader
Byte[2]: 0x0C/0x09  - Category (0x0C=ANC, 0x09=Game)
Byte[3]: 0x01   - Subcommand/Parameter
Byte[4]: VALUE  - Mode value (0x63=ANC ON, 0xA5=Passthrough, 0x02=Normal/OFF, 0x01=Enable, 0x02=Disable)
```

***

## 📱 Interface & Control

### Touch Gestures
| Action | Result |
|---|---|
| **1x Tap (Left)** | Previous track |
| **1x Tap (Right)** | Next track |
| **2x Tap (Left/Right)** | Play/Pause |
| **3x Tap (Left/Right)** | Switch ANC Mode |
| **Long Press (Right)** | Voice Assistant |
| **Swipe Up** | Volume up |
| **Swipe Down** | Volume down |

# 🎧 SoundPEATS Capsule3 Pro+ - Technical Information Summary

## ENTIRE REPOSITORY CREATED BY AI
- **Created by**: Perplexity (Claude Sonnet 4.5 reasoning)

***

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

### Supported Apps
- **Official**: PeatsAudio (replaced old SoundPEATS app)
- **Features**: 10-band EQ, ANC control, Touch settings, Firmware update
- **Note**: Known display issues on some devices

---

## 🎵 Hi-Res Audio & LDAC

### Supported Codecs
| Codec | Bitrate | Resolution | Notes |
|---|---|---|---|
| **LDAC** | 990 kbps | 96 kHz / 24-bit | Hi-Res certified |
| **AAC** | ~256 kbps | 48 kHz | Standard |
| **SBC** | ~328 kbps | 48 kHz | Default fallback |

### LDAC Setup (Android)
```
Settings → Developer Options
→ Bluetooth Audio Codec → LDAC
→ LDAC Quality → Best (990 kbps)
→ Bluetooth Audio Sample Rate → 96 kHz
→ Bluetooth Audio Bits Per Sample → 24 bit
```

***

## 📊 Battery Information (Under Verification)

**Issue**: Battery data displays incorrectly (197%, 207%)

**Raw Data**: 3 bytes from characteristic 0x00000008
- Suspected format: BCD encoding or bit mask

**Testing methods**:
- BCD Decode: `45 57 00` → `45% 57% 0%`
- Direct bytes: `69 87 0` (needs confirmation)
- Bit mask (`& 0x7F`): Similar to direct

***

## 📝 Important Notes

1. **Battery Reading**: Currently has bugs, needs BCD encoding verification
2. **Media Controls**: Does not support play/pause/volume via Bluetooth commands
3. **App**: PeatsAudio app differs from old SoundPEATS app
4. **LDAC**: Only works on Android 8.0+
5. **Config**: Firmware v15 from October 9, 2024

***

**Last Updated**: October 31, 2025

**Source**: Official SoundPEATS + Reverse Engineering via nRF Connect + Python Bleak
(https://soundpeats.com/products/capsule3-pro-plus-ai-adaptive-active-noise-cancelling-wireless-earbuds)[11]
(https://www.thephonograph.net/soundpeats-capsule3-pro-review/)[12]
(https://www.seriousinsights.net/soundpeats-capsule3-pro-review/)[13]
(https://soundpeatsvietnam.com/san-pham/tai-nghe-bluetooth-soundpeats-capsule-3-pro-2/)[14]
(https://soundpeats.com/blogs/news/soundpeats-capsule3-pro)[15]
(https://mobileaudiophile.com/true-wireless-sound-tws-review/soundpeats-capsule3-pro-review/)[16]
(https://manuals.plus/asin/B0D62Q8NYY)[17]
(https://www.soundguys.com/soundpeats-capsule3-pro-plus-review-129410/)[18]

[1](https://soundpeats.com/products/capsule3-pro-plus-ai-adaptive-active-noise-cancelling-wireless-earbuds)
[2](https://soundpeatsvietnam.com/huong-dan-su-dung-tai-nghe-soundpeats-capsule-3-pro/)
[3](https://device.report/manual/15010150)
[4](https://www.reddit.com/r/Soundpeats/comments/1gre7kb/i_couldnt_connect_to_my_two_devices_simultaneously/)
[5](https://www.soundguys.com/soundpeats-capsule3-pro-plus-review-129410/)
[6](https://ncstore.net/product/tai-nghe-bluetooth-soundpeats-capsule-3-pro-2/)
[7](https://www.youtube.com/watch?v=FGWAgunfZOM)
[8](https://soundpeatsvietnam.com/huong-dan-su-dung-soundpeats-capsule-3-pro/)
[9](https://manuals.plus/vi/soundpeats/capsule-3-pro-true-wireless-earbuds-manual)
[10](https://www.youtube.com/watch?v=HCIArzIL_Js)
[11](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/49356808/5950194e-1007-4862-8a78-3748f8f744c1/image.jpg)
[12](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/49356808/14c3844c-7cd9-4e85-a36b-25da06121ace/Screenshot_2025-10-31-20-16-49-25_b783bf344239542886fee7b48fa4b892.jpg)
[13](https://stackoverflow.com/questions/20398581/handle-bluetooth-headset-clicks-action-voice-command-and-action-web-search-on)
[14](https://github.com/androidx/media/issues/249)
[15](https://stackoverflow.com/questions/77938733/how-to-receive-bluetooth-headset-play-pause-event-in-android-java)
[16](https://www.youtube.com/watch?v=WcL5M6NPIqE)
[17](https://fairylightsai.substack.com/p/reverse-engineer-ble-smart-lights)
[18](https://www.silabs.com/documents/public/application-notes/AN986.pdf)

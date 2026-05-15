# GNU Radio PAL Color Video Decoder

This project is a custom Software-Defined Radio (SDR) pipeline built in GNU Radio that demodulates, synchronizes, and decodes raw PAL analog video signals into viewable color RGB video.

## Features & Signal Processing
* **RF Frontend:** Configured to interface with a USRP B200 to capture raw RF data.
* **AM Demodulation & Filtering:** Uses Quadrature Demodulation and custom FIR Band-Pass/Band-Reject filters to isolate the luminance (Y) and chrominance (C) subcarriers.
* **Custom Python DSP Blocks:** 
  * **Sync & Color Burst:** Detects H-sync and V-sync pulses, extracts the PAL color burst, and applies phase-correction algorithms to separate U and V color components.
  * **Color Space Conversion:** Converts the separated YUV signals into packed RGB24 pixel data.
* **Live Video Output:** Streams the raw RGB frames over a TCP sink locally to `ffplay` for real-time viewing.

## Files Included
* `color_decoder_v3.grc`: The main GNU Radio Companion flowgraph.
* `color_decoder_v2.py`: Compiled Python script of the flowgraph.
* `*_epy_block_*.py`: Embedded Python blocks handling the complex matrix math, pulse detection, and YUV-to-RGB conversion.

## Prerequisites
* GNU Radio Companion (v3.10+)
* UHD (for USRP B200)
* FFmpeg / `ffplay` (for viewing the TCP video stream)

## Visual Proof

<img width="1528" height="755" alt="image" src="https://github.com/user-attachments/assets/d0720398-d8fe-4fad-9318-79f11b7f4739" />
<img width="828" height="550" alt="image" src="https://github.com/user-attachments/assets/df6dcc32-ca03-4849-b555-8f107cb4367b" />
<img width="1054" height="1056" alt="image" src="https://github.com/user-attachments/assets/667da359-fc2c-4c5a-92aa-ebe85ccfb102" />



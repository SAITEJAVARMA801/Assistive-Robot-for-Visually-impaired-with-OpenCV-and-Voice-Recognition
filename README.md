# Assistive-Robot-for-Visually-impaired-with-OpenCV-and-Voice-Recognition
An Assistive mobile robot for the visually impaired that combines computer vision, voice interaction, and motor control. Using Raspberry Pi 5, YOLOv11, and speech feedback, it detects obstacles, follows voice commands, accesses Google/Wikipedia/YouTube, and drives motors via Arduino + L298N for safe navigation.
---

## Features:

1. YOLOv11 Object Detection

2. Detects obstacles in real time using a USB camera.

3. Announces detected objects via voice.

4. Avoids obstacles by turning, backing up, or moving forward.

## Voice Recognition Commands:

1. search google:   Opens Google search in browser

2. search wikipedia:   Reads summary from Wikipedia

3. play a song on youtube : Plays requested video on YouTube

4. forward: Robot moves forward

5. back: Robot moves Back

6. left: Robot moves left

7. right: robot moves right

8: stop: robots stops

9: turn on/off camera: turns on and off the camera.

# Speech Feedback:
1. All actions and detections are spoken using pyttsx3.

2. Motor Control via Arduino + L298N

3. Raspberry Pi sends JSON commands over USB serial.

# Hardware Setup:

1. Raspberry Pi 4 or 5

2. USB Camera

3. Arduino UNO

4. L298N Motor Driver

5. 4 DC Motors, Wheels & Chassis

6. 12V Battery

# Wiring:
 | Arduino Pin | L298N Pin |
 | ----------- | --------- | 
 | D5          | ENA       | 
 | D8          | IN1       | 
 | D9          | IN2       | 
 | D6          | ENB       | 
 | D10         | IN3       | 
 | D11         | IN4       | 

2. Raspberry pi 5 Usb to Arduino via Uart
3. Motors to positive and negative to the l298N 


# Raspberry pi 5 Setup:
1. Download the Yolov11.pt from the Ultralytics
2. Install the necessary packages 

       pip3 install ultralytics
       pip3 install opencv-python
       pip3 install pyttsx3
---
      pip3 install SpeechRecognition
      pip3 install pyserial
      pip3 install pywhatkit
      pip3 install wikipedia
---
    sudo apt-get install -y python3-pip portaudio19-dev libasound2-dev espeak  

3. Place your YOLOv11 model at:
  /home/stv/yolov11.pt

# Running the Robot:
1. Download the Github repository and Extract it to a Workspace
2. Program the Arduino uno with the robot.ino file from the repository
3. In Raspberry pi 5, Open terminal and go to the Downloaded folder
4. Run the Program
      
        python3 assistive_robot.py

5. Robot will start the voice recognition t greet and help u to navigate.
   Announce detected obstacles,
   Avoid obstacles automatically,
   Respond to your voice commands.





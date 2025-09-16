import os
import cv2
import time
import json
import serial
import logging
import pyttsx3
import threading
import pywhatkit as kit
import wikipedia
import speech_recognition as sr
from ultralytics import YOLO

# Model and serial configuration
YOLO_MODEL_PATH = "/home/stv/yolov11.pt"
SERIAL_PORT = "/dev/ttyUSB0"   # change if Arduino is on another port
BAUDRATE = 115200
FRAME_SKIP = 2
CONF_THRESH = 0.4

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("AssistiveRobot")

engine = pyttsx3.init()
recognizer = sr.Recognizer()
model = YOLO(YOLO_MODEL_PATH)

class MotorController:
    def __init__(self, port, baud):
        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            time.sleep(2)
            log.info(f"Connected to Arduino on {port}")
        except Exception as e:
            log.error(f"Arduino connection failed: {e}")
            self.ser = None

    def send(self, command, duration=300):
        if self.ser:
            payload = {"cmd": command, "ms": duration}
            self.ser.write((json.dumps(payload) + "\n").encode())

    def forward(self): self.send("FWD", 400)
    def backward(self): self.send("BACK", 600)
    def left(self): self.send("LEFT", 350)
    def right(self): self.send("RIGHT", 350)
    def stop(self): self.send("STOP")

motor = MotorController(SERIAL_PORT, BAUDRATE)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=1)
        speak(f"According to Wikipedia, {result}")
    except Exception:
        speak("I could not fetch information from Wikipedia right now.")

def play_song_on_youtube(song):
    speak(f"Playing {song} on YouTube")
    kit.playonyt(song)

def voice_command_loop():
    global camera_on
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio).lower()
                log.info(f"Voice command: {command}")

                if "search google" in command:
                    query = command.replace("search google", "").strip()
                    kit.search(query)

                elif "search wikipedia" in command:
                    query = command.replace("search wikipedia", "").strip()
                    search_wikipedia(query)

                elif "play" in command and "youtube" in command:
                    song = command.replace("play", "").replace("on youtube", "").strip()
                    play_song_on_youtube(song)

                elif "turn on camera" in command:
                    camera_on = True
                    speak("Camera on")

                elif "turn off camera" in command:
                    camera_on = False
                    speak("Camera off")
                    cv2.destroyAllWindows()

                elif "forward" in command:
                    motor.forward()
                    speak("Moving forward")

                elif "back" in command:
                    motor.backward()
                    speak("Moving backward")

                elif "left" in command:
                    motor.left()
                    speak("Turning left")

                elif "right" in command:
                    motor.right()
                    speak("Turning right")

                elif "stop" in command:
                    motor.stop()
                    speak("Stopping")

            except sr.UnknownValueError:
                log.warning("Voice not recognized.")
            except sr.RequestError:
                log.error("Speech recognition service error.")

def vision_loop():
    global camera_on
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        log.error("Camera not available")
        return

    frame_count = 0
    while True:
        if not camera_on:
            time.sleep(0.1)
            continue

        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % FRAME_SKIP != 0:
            continue

        H, W, _ = frame.shape
        results = model(frame)
        detections = []

        for box in results[0].boxes:
            conf = box.conf[0].item()
            if conf < CONF_THRESH:
                continue
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            xc = (x1 + x2) / 2
            name = model.names[int(box.cls[0])]
            detections.append((xc, name))

            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, name, (int(x1), int(y1) - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if detections:
            names = [d[1] for d in detections]
            speak(f"I see {', '.join(names)}")

            for xc, name in detections:
                if xc < W / 3:
                    motor.right()
                    speak("Obstacle left, turning right")
                elif xc > 2 * W / 3:
                    motor.left()
                    speak("Obstacle right, turning left")
                else:
                    motor.backward()
                    speak("Obstacle ahead, moving backward")

        cv2.imshow("Assistive Robot", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_on = True
    threading.Thread(target=voice_command_loop, daemon=True).start()
    vision_loop()

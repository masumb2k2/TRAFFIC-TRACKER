8# 🚦 TRAFFIC TRACKER : Real-Time Vehicle Detection & Counting

Unleash the power of **Artificial Intelligence** and **Computer Vision** for *real-time traffic management*. This project is not just a demo; it's a **battle-tested solution** for automated vehicle counting, traffic analytics, and law enforcement. Enter the era of smart cities—**NO COMPROMISES.**

---

## ⚡ Features

- **YOLOv8 Detection** – Fast and accurate, detects cars, buses, trucks, motorcycles—the works.
- **Multi-class Counting** – Tracks *entry* and *exit* counts for each vehicle type. Be precise. Be ruthless.
- **Firebase Integration** – Pushes live stats to your Firebase RTDB for seamless cloud analytics.
- **Elegant Overlays** – Live feed shows REAL numbers, color-coded and labeled, ready for reporting.
- **Plug-and-Play** – Supports both camera input and saved video files.
- **Tracker Algorithm** – Robust custom tracking—no false positives, no mercy.

---

## 💥 DEMO

![Traffic Tracking Demo](demo-demo.gif)

---

## 🔥 Installation

1. **Clone the repo**  
git clone https://github.com/masumb2k2/traffic-tracker.git

3. **Install Dependencies**  

pip install ultralytics opencv-python pandas firebase_admin cvzone

3. **Download YOLOv8s Model**  
Place `yolov8s.pt` in the working directory.
4. **Set Up Firebase**  
- Get your `serviceAccountKey.json` from Firebase Console
- Update the database URL in the code

---

## 🧨 Usage

### Video File
python traffic_tracker.py --video tf.mp4

text

### Live Camera
python traffic_tracker.py --cam 0

text

### Output
- Live frame: Vehicle counts, classification, and tracking.
- Firebase RTDB: Real-time stats pushed every 10 seconds.

---

## 🛠️ Tech Stack

| Module           | Purpose                  |
|------------------|-------------------------|
| **YOLOv8**       | Deep Learning Detection |
| **OpenCV**       | Video & Image Processing|
| **Pandas**       | Data Management         |
| **Firebase**     | Cloud DB Integration    |
| **cvzone**       | Visualization Overlay   |
| **Custom Tracker** | Object Persistence    |

---

## 💀 Aggressive. Accurate. Authoritative.

This code was authorized by **MASUM**.

*Deploy. Analyze. Dominate. The highway is yours.*

---

## 🔗 License

MIT.  
Feel free to use—but **give credit when crushing competitors with superior tech.**

---

## 📢 Contact & Credits

**Built by MASUM**  
For extreme traffic analytics and smart city dominance.

---

**STOP WAITING. START TRACKING. OWN THE ROAD.**

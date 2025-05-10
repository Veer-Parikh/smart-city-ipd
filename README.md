# Smart Traffic Signal Control using SUMO 🚦

This project demonstrates the implementation of a smart traffic signal control system using the SUMO (Simulation of Urban MObility) simulator.

We compare a traditional fixed-time traffic signal system with an optimized signal control algorithm that utilizes detectors and Python-based real-time decision-making. The goal is to reduce average wait times and improve traffic flow at intersections.

---

## 📍 Project Overview

### ❌ Traditional Signal System

- Operates on fixed time cycles.
- No awareness of real-time traffic density.
- Used as a baseline for comparison.

### ✅ Smart Signal System

- Integrates traffic detectors via SUMO.
- Controlled using a Python algorithm.
- Dynamically adjusts green times based on traffic volume.
- Achieves noticeable improvement in traffic throughput and reduced delays.

---

## 🔁 Methodology

- Built two identical intersections in SUMO using **netconvert**.
- One network follows a **static timing plan**.
- The second includes:
  - **Induction loop detectors** (`.add.xml`)
  - **Python control logic** (`smart_traffic_control.py`)
- Both networks were fed with the **same vehicle routes** for fairness.
- Simulation time and vehicle throughput were measured.

---

## 📊 Results

### Side-by-side SUMO Comparison

**Right:** Fixed Time Signal  
**Left:** Smart Signal with Python Controller

<!-- Upload and insert images below -->
![WhatsApp Image 2025-05-10 at 01 04 21_4516a727](https://github.com/user-attachments/assets/10259cdc-1525-43c0-8f09-c113ba4969f4)
![WhatsApp Image 2025-05-10 at 01 04 21_4fb234b5](https://github.com/user-attachments/assets/2a9005f2-50f2-4c3a-a345-a25c5d694047)

---

### 📈 Output Console
![WhatsApp Image 2025-05-10 at 01 04 22_00502d60](https://github.com/user-attachments/assets/10f083ba-9feb-4f4d-9fb6-03e4cc1089c9)

---

## 🗺️ Map Integration (Optional)

We also explored using sumo WebWizard to showcase real-world applicability. The smart algorithm is adaptable to city-level junctions using real traffic layouts.

---

## 📁 Project Structure

```plaintext
├── edges.xml
├── nodes.xml
├── connections.xml
├── tls.xml
├── routes.xml
├── simulation.sumocfg
├── intersection.netccfg
├── run_simulation.py
├── smart_traffic_control.py
├── traffic_detector.add.xml
├── gui_settings.xml
└── README.md

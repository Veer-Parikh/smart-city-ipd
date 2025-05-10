# 🚦 Smart Traffic Management System Using Deep RL & Computer Vision

An AI-powered solution for intelligent traffic control in Indian cities — integrating **deep reinforcement learning**, **YOLOv8 vehicle detection**, and the **SUMO traffic simulator** to optimize signal timing, reduce congestion, and prioritize emergency vehicles in real time.

> 📍 Developed by: Vinit Shah, Veer Parikh, Vedant Khade, Rishi Shah
> 🎓 Dwarkadas J. Sanghvi College of Engineering, Mumbai

---

## 🧠 Overview

India’s traffic congestion issues demand a smarter approach than fixed-timing signals. This project proposes a **fully adaptive system** that:

- Learns traffic behavior using **Deep Q-Networks (DQN)**
- Detects vehicles in real-time using **YOLOv8**
- Simulates urban intersections using **SUMO**
- Responds to emergency vehicles with dynamic green corridors
- Shows up to **35% delay reduction** and **73% faster emergency clearance**

---

## 🧭 Project Structure

```bash
├── main/
│   ├── README.md                      
├── sumo/                        # SUMO Simulation Models
│   ├── nodes.xml
│   ├── edges.xml
│   ├── routes.xml
│   ├── tls.xml
│   ├── detectors.add.xml
│   ├── simulation.sumocfg
│   └── smart_traffic_control.py
├── vehicle_detection_finetuned/
│   ├── YOLOv8_custom/           # Trained models and datasets
│   ├── camera_pipeline.py       # Real-time object detection
│   └── emergency_priority.py    # Emergency detection and control
```

---

## 🔀 Branch Overview

### 🔧 `main`

- Contains the master documentation, paper, and visual outputs.

### 🚦 `sumo`

- SUMO-based simulation setup
- Python-based adaptive signal control using traffic density and queue estimation

### 👁️ `vehicle_detection_finetuned`

- YOLOv8 object detection fine-tuned on Indian traffic data
- Classifies vehicles and detects emergency services in real-time

---

## 🏗️ Architecture

```
 Cameras → YOLOv8 → Lane-wise vehicle data
                                ↓
       SUMO ↔ Deep Q-Network (DQN Agent)
                                ↓
        Signal Timing Updates → SUMO / Real Hardware
```

---

## 🚗 Use Cases

- 🔁 **Adaptive Signal Control:** Live lane-wise vehicle monitoring and signal adjustments
- 🚨 **Emergency Vehicle Prioritization:** Detection and fast-track signal clearance
- 🔄 **Green Wave Synchronization:** Coordination of adjacent intersections
- 🌍 **Real Intersection Mapping:** Real maps created using **WebWizard**

---

## 📊 Key Results

| Metric               | Fixed Timing | Our System | Improvement |
| -------------------- | ------------ | ---------- | ----------- |
| Avg Delay (s)        | 78.5         | 51.0       | ↓ 35%       |
| Throughput (veh/h)   | 1250         | 1650       | ↑ 32%       |
| Emergency Delay (s)  | 45.8         | 12.3       | ↓ 73%       |
| CO₂ Emissions (kg/h) | 95.2         | 76.5       | ↓ 20%       |

---

## ⚙️ Technologies Used

- [SUMO](https://www.eclipse.org/sumo/) – Traffic simulation
- [YOLOv8](https://github.com/ultralytics/ultralytics) – Vehicle detection
- [PyTorch](https://pytorch.org/) – DQN implementation
- [OpenCV](https://opencv.org/) – Real-time vision
- [Jetson NX (Edge)] – Hardware deployment for low-latency inference
- [WebWizard] – Real-world intersection mapping

---

## 🚀 Getting Started

### ▶️ Run Simulation

```bash
cd sumo
netconvert -c intersection.netccfg      # Generate .net.xml
sumo-gui -c simulation.sumocfg          # Launch static signal sim
python smart_traffic_control.py         # Launch smart signal sim
```

### 📹 Run YOLO Detection

```bash
cd vehicle_detection_finetunes
python camera_pipeline.py               # Live object detection
```

---

## 🧪 Research Contributions

- A **hybrid architecture** combining CV + RL
- Left-turn prioritization modeling
- Green corridor coordination
- Transfer learning for rapid deployment
- Smart city integration and live dashboard design

---

## 🔮 Future Scope

- Pedestrian and public transport integration
- Federated learning for distributed training
- Gamified traffic discipline system
- EV-aware traffic flow control
- Expansion to multi-intersection corridors

---

## 🙏 Acknowledgments

This project was developed as part of our final year capstone. We thank:

- **Dr. Meera Narvekar** for invaluable mentorship

---

> _“The traffic signal of tomorrow won’t just blink red and green — it will think.”_

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys 
import traci

# Add SUMO tools to path
if "SUMO_HOME" in os.environ:
    sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# Config
SIM_STEP = 0.1
MIN_GREEN = 10
MAX_GREEN = 90
PRESSURE_THRESHOLD = 2.5

LANE_WEIGHTS = {
    "N2C": 1.0,
    "S2C": 1.0,
    "E2C": 1.0,
    "W2C": 1.0
}

class AdaptiveTrafficLight:
    def __init__(self):
        self.sumo_binary = os.environ.get("SUMO_BINARY", "sumo-gui")
        self.sumo_cmd = [self.sumo_binary, "-c", "simulation.sumocfg"]
        traci.start(self.sumo_cmd)

        self.tls_id = "C"
        self.current_phase = 0
        self.time_in_phase = 0

        # Corrected phase map: green at even indices
        self.direction_to_phase = {
            "N": 0,
            "E": 2,
            "S": 4,
            "W": 6
        }

        # 6 detectors per direction (combined across both lanes)
        self.detectors = {
            "N": [f"detector_N2C_{i}" for i in range(6)],
            "S": [f"detector_S2C_{i}" for i in range(6)],
            "E": [f"detector_E2C_{i}" for i in range(6)],
            "W": [f"detector_W2C_{i}" for i in range(6)]
        }

        # Match tls.xml green/yellow durations: 8 total phases
        self.phase_durations = [30, 4, 30, 4, 30, 4, 30, 4]

    def run(self):
        try:
            while traci.simulation.getMinExpectedNumber() > 0:
                traci.simulationStep()
                self.time_in_phase += SIM_STEP

                if self._should_switch():
                    self._switch_phase()

        except KeyboardInterrupt:
            print("Simulation interrupted")
        finally:
            traci.close()

    def _get_phase_type(self, idx):
        if idx in [0, 2, 4, 6]:
            return "green"
        elif idx in [1, 3, 5, 7]:
            return "yellow"
        return "red"

    def _get_current_direction(self):
        for direction, phase in self.direction_to_phase.items():
            if self.current_phase == phase:
                return direction
        return None

    def _calculate_pressure(self):
        pressure = {}
        for direction, loop_ids in self.detectors.items():
            count = sum(len(traci.inductionloop.getLastStepVehicleIDs(det)) for det in loop_ids)
            pressure[direction] = count * LANE_WEIGHTS[f"{direction}2C"]
        return pressure

    def _should_switch(self):
        phase_type = self._get_phase_type(self.current_phase)

        if phase_type in ["yellow", "red"]:
            return self.time_in_phase >= self.phase_durations[self.current_phase]

        if phase_type == "green":
            if self.time_in_phase < MIN_GREEN:
                return False
            if self.time_in_phase >= MAX_GREEN:
                return True

            current_dir = self._get_current_direction()
            pressure = self._calculate_pressure()
            current_pressure = pressure.get(current_dir, 0)

            if current_pressure >= PRESSURE_THRESHOLD:
                return False  # Stay green

            max_other = max((v for k, v in pressure.items() if k != current_dir), default=0)
            if max_other > current_pressure * 3:
                return True

        return False

    # def _switch_phase(self):
    #     self.time_in_phase = 0
    #     if self._get_phase_type(self.current_phase) == "green":
    #         self.current_phase = (self.current_phase + 1) % 8
    #     else:
    #         pressure = self._calculate_pressure()
    #         next_dir = max(pressure, key=pressure.get, default="N")
    #         self.current_phase = self.direction_to_phase[next_dir]

    #     traci.trafficlight.setPhase(self.tls_id, self.current_phase)
    def _switch_phase(self):
        self.time_in_phase = 0

        if self._get_phase_type(self.current_phase) == "green":
            self.current_phase = (self.current_phase + 1) % 8  # go to yellow
        else:
            # Move to next green in round robin
            self.current_phase = self._get_next_green_phase()

            # Adjust green time based on pressure
            direction = self._get_current_direction()
            pressure = self._calculate_pressure()
            current_pressure = pressure.get(direction, 0)

            base_green = 30
            scale = 4  # add 1.5s per vehicle over threshold
            # print(f"Pressure: {pressure}, Current pressure: {current_pressure}")

            if current_pressure > PRESSURE_THRESHOLD:
                extra = (current_pressure - PRESSURE_THRESHOLD) * scale
                print(f"Current intensity of cars: {current_pressure}, Extra time: {extra}")
                adaptive_time = min(MAX_GREEN, base_green + extra)
            else:
                adaptive_time = base_green

            self.phase_durations[self.current_phase] = adaptive_time

        traci.trafficlight.setPhase(self.tls_id, self.current_phase)


    def _get_next_green_phase(self):
        # Rotate to the next green phase in round-robin order
        if self.current_phase in [1, 0]: return 2  # N → E
        if self.current_phase in [3, 2]: return 4  # E → S
        if self.current_phase in [5, 4]: return 6  # S → W
        if self.current_phase in [7, 6]: return 0  # W → N
        return 0

if __name__ == "__main__":
    AdaptiveTrafficLight().run()

# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# import os
# import sys
# import traci
# import numpy as np
# from collections import defaultdict

# # Ensure SUMO tools are available
# if 'SUMO_HOME' in os.environ:
#     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
#     sys.path.append(tools)
# else:
#     sys.exit("Please declare environment variable 'SUMO_HOME'")

# # Configuration
# SIM_STEP = 0.1
# MIN_GREEN = 10
# MAX_GREEN = 90
# YELLOW_DURATION = 4
# PRESSURE_THRESHOLD = 12  # Threshold pressure value to trigger green time extension

# LANE_WEIGHTS = {
#     "N2C": 1.0,
#     "S2C": 1.0,
#     "E2C": 1.0,
#     "W2C": 1.0
# }

# class AdaptiveController:
#     def __init__(self):
#         self.sumo_binary = os.environ.get("SUMO_BINARY", "sumo-gui")
#         self.sumo_cmd = [self.sumo_binary, "-c", "simulation.sumocfg"]
#         traci.start(self.sumo_cmd)

#         self.tls_id = "C"
#         self.current_phase = 0
#         self.time_in_phase = 0
#         self.phase_durations = [4, 30, 4, 4, 30, 4, 4, 30, 4, 4, 30, 4]

#         self.direction_map = {
#             "N": ["N2C_0", "N2C_1"],
#             "S": ["S2C_0", "S2C_1"],
#             "E": ["E2C_0", "E2C_1"],
#             "W": ["W2C_0", "W2C_1"]
#         }

#         # self.direction_to_phase = {
#         #     "N": 1,
#         #     "E": 4,
#         #     "S": 7,
#         #     "W": 10
#         # }

#         self.direction_to_phase = {
#             "N": 0, # N2C_0     
#             "E": 2, # E2C_0
#             "S": 4, # S2C_0
#             "W": 6 # W2C_0
#         }
#     def run(self):
#         try:
#             while traci.simulation.getMinExpectedNumber() > 0:
#                 traci.simulationStep()
#                 self.time_in_phase += SIM_STEP

#                 if self._should_switch():
#                     self._switch_phase()

#         except KeyboardInterrupt:
#             print("Simulation stopped by user.")
#         finally:
#             traci.close()

#     def _get_current_phase_type(self):
#         if self.current_phase in [1, 4, 7, 10]:
#             return "green"
#         elif self.current_phase in [0, 2, 5, 8, 11]:
#             return "yellow"
#         else:
#             return "red"

#     def _get_active_direction(self):
#         for dir_, phase in self.direction_to_phase.items():
#             if self.current_phase == phase:
#                 return dir_
#         return None

#     def _get_pressure(self):
#         pressure = {}
#         for dir_, lanes in self.direction_map.items():
#             queue_len = 0
#             for lane in lanes:
#                 veh_ids = traci.lane.getLastStepVehicleIDs(lane)
#                 queue_len += sum(1 for v in veh_ids if traci.vehicle.getSpeed(v) < 0.1)
#             weight = LANE_WEIGHTS.get(f"{dir_}2C", 1.0)
#             pressure[dir_] = queue_len * weight
#         return pressure

#     def _should_switch(self):
#         phase_type = self._get_current_phase_type()

#         if phase_type in ["yellow", "red"]:
#             return self.time_in_phase >= self.phase_durations[self.current_phase]

#         if phase_type == "green":
#             if self.time_in_phase < MIN_GREEN:
#                 return False
#             if self.time_in_phase >= MAX_GREEN:
#                 return True

#             direction = self._get_active_direction()
#             pressure = self._get_pressure()
#             current_pressure = pressure.get(direction, 0)

#             if current_pressure >= PRESSURE_THRESHOLD:
#                 # Extend green time (up to max)
#                 extra = min(MAX_GREEN - self.phase_durations[self.current_phase], 5)
#                 self.phase_durations[self.current_phase] += extra
#                 return False  # Don't switch yet

#             # Check if other direction has more need
#             other = {d: p for d, p in pressure.items() if d != direction}
#             if other and max(other.values()) > current_pressure * 1.5:
#                 return True

#         return False

#     # def _switch_phase(self):
#     #     self.time_in_phase = 0

#     #     if self._get_current_phase_type() == "green":
#     #         self.current_phase = (self.current_phase + 1) % 12  # to yellow
#     #     else:
#     #         pressure = self._get_pressure()
#     #         last_dir = self._get_active_direction()
#     #         if last_dir:
#     #             pressure.pop(last_dir, None)

#     #         if pressure:
#     #             next_dir = max(pressure, key=pressure.get)
#     #             self.current_phase = self.direction_to_phase[next_dir]
#     #         else:
#     #             self.current_phase = (self.current_phase + 1) % 12

#     #     traci.trafficlight.setPhase(self.tls_id, self.current_phase)
#     def _switch_phase(self):
#         self.time_in_phase = 0

#         if self._get_current_phase_type() == "green":
#             self.current_phase = (self.current_phase + 1) % 12  # go to yellow
#         else:
#             pressure = self._get_pressure()
#             current_dir = self._get_active_direction()

#             # Don't remove the current direction; ensure all are considered
#             next_dir = max(pressure, key=pressure.get) if pressure else None

#             # If no pressure, rotate to next green phase
#             if next_dir:
#                 self.current_phase = self.direction_to_phase.get(next_dir, (self.current_phase + 2) % 12)
#             else:
#                 # Fallback: cycle through all green phases
#                 self.current_phase = (self.current_phase + 2) % 12

#         traci.trafficlight.setPhase(self.tls_id, self.current_phase)


# if __name__ == "__main__":
#     ctrl = AdaptiveController()
#     ctrl.run()

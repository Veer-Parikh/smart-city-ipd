GREEN = []
RED = []
YELLOW = [5,5,5,5]

intersections = {
    "I1": {
        "cars": 20,
        "trucks": 3,
        "bikes": 10,
        "ambulance": 1,
        "total": 33
    },
    "I2": {
        "cars": 9,
        "trucks": 0,
        "bikes": 10,
        "ambulance": 0,
        "total": 19
    },
    "I3": {
        "cars": 5,
        "trucks": 4,
        "bikes": 1,
        "ambulance": 0,
        "total": 10
    },
    "I4": {
        "cars": 3,
        "trucks": 1,
        "bikes": 3,
        "ambulance": 0,
        "total": 7
    }
}


lanes = {
    "lane1":{
        "red":False,
        "yellow":False,
        "green":{
            "left":False,
            "right":False,
            "straight":False
        }
    },
    "lane2":{
        "red":False,
        "yellow":False,
        "green":{
            "left":False,
            "right":False,
            "straight":False
        }
    },
    "lane3":{
        "red":False,
        "yellow":False,
        "green":{
            "left":False,
            "right":False,
            "straight":False
        }
    },
    "lane4":{
        "red":False,
        "yellow":False,
        "green":{
            "left":False,
            "right":False,
            "straight":False
        }
    }
}


def ambulance_detection(intersections):
    for intersection,data in intersections.items():
        if data["ambulance"] > 0:
            while data["ambulance"] > 0:
                # GREEN[intersection] = 9999
                # for other_intersection in intersections.keys():
                #     if other_intersection != intersection:
                #         RED[other_intersection] = 9999
                lane_adjustments(intersection)


def get_max_vehicles_lane():
    max_vehicles = 0
    for intersection,data in intersections.items():
        if data["total"] > max_vehicles:
            max_vehicles = data
            max_lane = intersection
    return max_vehicles,max_lane


def time_adjustment(max_vehicles,max_lane):
    if max_vehicles >= 40:
        GREEN[max_lane] = 45 # 30 + 15
        extended_time = 15
        manage_red(max_lane)
        adjust_red(extended_time,max_lane)
        for i in range(0,4):
            if i != max_lane:
                GREEN[i] = 0
    elif 40 > max_vehicles >= 30:
        GREEN[max_lane] = 42 # 30 + 12
        extended_time = 12
        manage_red(max_lane)
        adjust_red(extended_time,max_lane)
        for i in range(0,4):
            if i != max_lane:
                GREEN[i] = 0
    elif 30 > max_vehicles >= 20:
        GREEN[max_lane] = 36 # 30 + 6
        extended_time = 6
        manage_red(max_lane)
        adjust_red(extended_time,max_lane)
        for i in range(0,4):
            if i != max_lane:
                GREEN[i] = 0
    else:
        normal_green(current)
        manage_red(current)

current = 0
def normal_green(current):
    GREEN[current] = 30
    GREEN[(current+1)%4] = GREEN[(current+2)%4] = GREEN[(current+3)%4] = 0
    current = (current+1)%4


def manage_red(max_lane):
    if max_lane == 0:
        RED[0] = 0
        RED[1] = 35  #30 + 5 of lane 1
        RED[2] = 70  #35 + 30 + 5 of lane 2
        RED[3] = 105 #70 + 30 + 5 of lane 3
    elif max_lane == 1:
        RED[1] = 0
        RED[2] = 35  
        RED[3] = 70  
        RED[0] = 105 
    elif max_lane == 2:
        RED[2] = 0
        RED[3] = 35  
        RED[0] = 70  
        RED[1] = 105 
    elif max_lane == 3:
        RED[3] = 0 
        RED[0] = 35  
        RED[1] = 70  
        RED[2] = 105    
    # return RED


def adjust_red(extended_time,max_lane):

    if extended_time == 15:
        if max_lane == 0:
            RED[1] += 5
            RED[2] += 10
            RED[3] += 15
        elif max_lane == 1:
            RED[2] += 5
            RED[3] += 10
            RED[0] += 15
        elif max_lane == 2:
            RED[3] += 5
            RED[0] += 10
            RED[1] += 15
        else:
            RED[0] += 5
            RED[1] += 10
            RED[2] += 15

    elif extended_time == 12:
        if max_lane == 0:
            RED[1] += 4
            RED[2] += 8
            RED[3] += 12
        elif max_lane == 1:
            RED[2] += 4
            RED[3] += 8
            RED[0] += 12
        elif max_lane == 2:
            RED[3] += 4
            RED[0] += 8
            RED[1] += 12
        else:
            RED[0] += 4
            RED[1] += 8
            RED[2] += 12
    
    elif extended_time == 6:
        if max_lane == 0:
            RED[1] += 2
            RED[2] += 4
            RED[3] += 6
        elif max_lane == 1:
            RED[2] += 2
            RED[3] += 4
            RED[0] += 6
        elif max_lane == 2:
            RED[3] += 2
            RED[0] += 4
            RED[1] += 6
        else:
            RED[0] += 2
            RED[1] += 4
            RED[2] += 6
    # return RED


def reset_lane(lane):
    lanes[lane]["red"] = False
    lanes[lane]["yellow"] = False
    for direction in lanes[lane]["green"]:
        lanes[lane]["green"][direction] = False


def lane_adjustments(current_lane):
    for lane in lanes:
        reset_lane(lane)
    if current_lane == 0:
        lanes["lane1"]["green"]["left"] = True
        lanes["lane1"]["green"]["right"] = True
        lanes["lane1"]["green"]["straight"] = True

        lanes["lane4"]["green"]["left"] = True
    elif current_lane == 1:
        lanes["lane2"]["green"]["left"] = True
        lanes["lane2"]["green"]["right"] = True
        lanes["lane2"]["green"]["straight"] = True

        lanes["lane1"]["green"]["left"] = True
    elif current_lane == 2:
        lanes["lane3"]["green"]["left"] = True
        lanes["lane3"]["green"]["right"] = True
        lanes["lane3"]["green"]["straight"] = True

        lanes["lane2"]["green"]["left"] = True
    else:
        lanes["lane4"]["green"]["left"] = True
        lanes["lane4"]["green"]["right"] = True
        lanes["lane4"]["green"]["straight"] = True

        lanes["lane3"]["green"]["left"] = True       


def signalling_system():
    ambulance_detection(intersections)
    max_vehicles,max_lane = get_max_vehicles_lane()
    time_adjustment(max_vehicles,max_lane)
    lane_adjustments(max_lane)
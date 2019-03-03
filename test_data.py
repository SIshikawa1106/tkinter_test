import json
from collections import namedtuple
import random
import os

CellInfo = namedtuple("CellInfo", "Name Controllers Models")
ControllerInfo = namedtuple("ControllerInfo", "Name Robots")
RobotInfo = namedtuple("RobotInfo", "Name Position Joints tcp")
ModelInfo = namedtuple("ModelInfo", "Name Position")

print(RobotInfo.Name)

def build_robot(dict):
    keys = RobotInfo._fields
    return RobotInfo(dict[keys[0]], dict[keys[1]], dict[keys[2]], dict[keys[3]])

def build_model(dict):
    keys = ModelInfo._fields
    return ModelInfo(dict[keys[0]], dict[keys[1]])

def build_controller(dict):
    keys = ControllerInfo._fields
    robots = [build_robot(value) for value in dict[keys[1]]]
    return ControllerInfo(dict[keys[0]], robots)

def build_cell(dict):
    keys = CellInfo._fields
    controllers = []
    models = []
    if keys[1] in dict:
        controllers = [build_controller(value) for value in dict[keys[1]]]
    if keys[2] in dict:
        models = [build_model(value) for value in dict[keys[2]]]
    return CellInfo(dict[keys[0]], controllers, models)

def load_info(filename):
    if os.path.isfile(filename) == False:
        return []

    with open(filename) as file:
        dict = json.load(file)

        return [build_cell(value) for value in dict]

def random_position():
    pos = []
    for idx in range(6):
        val = random.random()*2 - 1
        pos.append(val if idx<3 else val*180)
    return pos

def random_angle():
    pos = []
    for idx in range(6):
        val = random.random()*2 - 1
        pos.append(val*180)
    return pos

if __name__ == "__main__":
    robots = []
    for id in ["A", "B", "C"]:

        pos = random_position()
        angle = random_angle()
        tcp = random_position()
        robots.append(RobotInfo("Robot-" + str(id), pos, angle, tcp)._asdict())

    models = []
    for id in ["A", "B", "C", "D"]:
        pos = random_position()
        models.append(ModelInfo("Model-" + id, pos)._asdict())

    controllers = []
    for id in ["A", "B", "C", "D"]:
        controllers.append(ControllerInfo("Controller-" + str(id), robots[0:random.randrange(len(robots))])._asdict())

    cells = []
    for id in ["A", "B", "C", "D"]:
        cells.append(CellInfo("Cell-" + str(id),
                              controllers[0:random.randrange(len(controllers))],
                              models[0:random.randrange(len(models))]
                              )._asdict())


    import datetime
    now = datetime.datetime.now()
    with open("test_{}.json".format(now.strftime("%Y%m%d-%H.%M.%S")), "w") as file:
        json.dump(cells, file, indent=2)

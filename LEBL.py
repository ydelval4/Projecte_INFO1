class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []


class Terminal:
    def __init__(self, name):
        self.name = name
        self.areas = []
        self.airlines = []


class BoardingArea:
    def __init__(self, name, schengen):
        self.name = name
        self.schengen = schengen
        self.gates = []


class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.aircraft_id = ""


def SetGates(area, init_gate, end_gate, prefix):
    if end_gate <= init_gate:
        return -1
    area.gates = []
    for i in range(init_gate, end_gate + 1):
        gate = Gate(prefix + str(i))
        area.gates.append(gate)
    return 0


def LoadAirlines(terminal, t_name):
    filename = f"{t_name}_Airlines.txt"
    try:
        f = open(filename, 'r')
    except:
        return -1
    terminal.airlines = []
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            terminal.airlines.append(parts[1])  # codi ICAO
    f.close()
    return 0


def LoadAirportStructure(filename):
    try:
        f = open(filename, 'r')
    except:
        return -1

    lines = f.readlines()
    f.close()

    first = lines[0].strip().split()
    bcn = BarcelonaAP(first[0])

    current_terminal = None
    for line in lines[1:]:
        line = line.strip()
        if line.startswith("Terminal"):
            parts = line.split()
            current_terminal = Terminal(parts[1])
            LoadAirlines(current_terminal, parts[1])
            bcn.terminals.append(current_terminal)
        elif line.startswith("Area"):
            parts = line.split()
            area_name = parts[1]
            schengen = (parts[2].lower() == "schengen")
            init_gate = int(parts[4])
            end_gate = int(parts[6])
            area = BoardingArea(area_name, schengen)
            prefix = f"{current_terminal.name}-{area_name}-"
            SetGates(area, init_gate, end_gate, prefix)
            current_terminal.areas.append(area)
    return bcn
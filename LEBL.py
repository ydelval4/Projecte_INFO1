from airport import *



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

    if len(lines) == 0:
        return -1

    parts = lines[0].strip().split()
    bcn = BarcelonaAP(parts[0])

    current_terminal = None

    for line in lines[1:]:
        line = line.strip()
        if line == "":
            continue

        parts = line.split()

        # TERMINAL
        if parts[0] == "Terminal":
            t_name = parts[1]

            current_terminal = Terminal(t_name)
            LoadAirlines(current_terminal, t_name)

            bcn.terminals.append(current_terminal)

        # AREA
        elif parts[0] == "Area":
            area_name = parts[1]

            # Schengen o no
            if parts[2] == "Schengen":
                schengen = True
            else:
                schengen = False

            # Area A Schengen Gates 1 - 11
            init_gate = int(parts[4])
            end_gate = int(parts[6])
            area = BoardingArea(area_name, schengen)
            prefix = current_terminal.name + "-" + area_name + "-"
            SetGates(area, init_gate, end_gate, prefix)
            current_terminal.areas.append(area)

    return bcn


def GateOccupancy(bcn):
    occupancy_list = []

    for terminal in bcn.terminals:
        for area in terminal.areas:
            for gate in area.gates:
                # Guardamos la información de cada puerta en una tupla o lista
                gate_info = {
                    "name": gate.name,
                    "occupied": gate.occupied,
                    "aircraft_id": gate.aircraft_id}
                occupancy_list.append(gate_info)

    return occupancy_list


def IsAirlineInTerminal(terminal, name):
    if not name or name.strip() == "":
        return False

    # Comprobamos si la aerolínea está en la lista de la terminal
    if name in terminal.airlines:
        return True

    return False

def SearchTerminal(bcn, name):
    if not name or name.strip() == "":
        return ""

    for terminal in bcn.terminals:
        if IsAirlineInTerminal(terminal, name):
            return terminal.name

    return ""

def AssignGate(bcn, aircraft):
    nomterminal = SearchTerminal(bcn, aircraft.airline)

    if nomterminal == "":
        return -1  # aerolínea no encontrada

    for terminal in bcn.terminals:
        if terminal.name == nomterminal:

            for area in terminal.areas:
                # comprobar tipo Schengen
                if area.schengen == aircraft.is_schengen:

                    for gate in area.gates:
                        if not gate.occupied:
                            gate.occupied = True
                            gate.aircraft_id = aircraft.id
                            return 0

    return -1  # no portes lliures

def GateOccupancy(bcn):
    occupancy_list = []

    for terminal in bcn.terminals:
        for area in terminal.areas:
            for gate in area.gates:
                # Guardamos la información de cada puerta en una tupla o lista
                gate_info = {
                    "name": gate.name,
                    "occupied": gate.occupied,
                    "aircraft_id": gate.aircraft_id}
                occupancy_list.append(gate_info)

    return occupancy_list


def IsAirlineInTerminal(terminal, name):
    if not name or name.strip() == "":
        return False

    # Comprobamos si la aerolínea está en la lista de la terminal
    if name in terminal.airlines:
        return True

    return False

def SearchTerminal(bcn, name):
    if not name or name.strip() == "":
        return ""

    for terminal in bcn.terminals:
        if IsAirlineInTerminal(terminal, name):
            return terminal.name

    return ""

def AssignGate(bcn, aircraft):
    nomterminal = SearchTerminal(bcn, aircraft.airline)

    if nomterminal == "":
        return -1  # aerolínea no encontrada

    for terminal in bcn.terminals:
        if terminal.name == nomterminal:

            for area in terminal.areas:
                # comprobar tipo Schengen
                if area.schengen == IsSchengenAirport(aircraft.origin):

                    for gate in area.gates:
                        if not gate.occupied:
                            gate.occupied = True
                            gate.aircraft_id = aircraft.id
                            return 0

    return -1  # no portes lliures

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
        self.time = ""
        self.departuretime = ""


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
                gate_info = {
                    "name": gate.name,
                    "occupied": gate.occupied,
                    "aircraft_id": gate.aircraft_id}
                occupancy_list.append(gate_info)
    return occupancy_list


def IsAirlineInTerminal(terminal, name):
    if not name or name.strip() == "":
        return False
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
        return -1

    for terminal in bcn.terminals:
        if terminal.name == nomterminal:
            for area in terminal.areas:
                if area.schengen == IsSchengenAirport(aircraft.origin):
                    for gate in area.gates:
                        if not gate.occupied:
                            gate.occupied = True
                            gate.aircraft_id = aircraft.id
                            gate.time = aircraft.time
                            gate.departuretime = aircraft.departuretime
                            return 0
    return -1

def FreeGate(bcn, aircraft):
    for terminal in bcn.terminals:
        for area in terminal.areas:
            for gate in area.gates:
                if gate.aircraft_id == aircraft.id:
                    gate.occupied = False
                    gate.aircraft_id = ""
                    gate.time = ""
                    gate.departuretime = ""
                    return 0
    return -1

def AssignNightGates(bcn, aircrafts):
    if len(aircrafts) == 0:
        return -1
    for ac in aircrafts:
        has_arrival = (ac.origin != '-' and ac.origin != '')
        if not has_arrival:
            AssignGate(bcn, ac)
    return 0

def _time_to_minutes(time_str):
    if not time_str or time_str == '-':
        return -1
    try:
        parts = time_str.split(':')
        if len(parts) != 2:
            return -1
        h, m = int(parts[0]), int(parts[1])
        if 0 <= h <= 23 and 0 <= m <= 59:
            return h * 60 + m
        return -1
    except:
        return -1


def AssignGatesAtTime(bcn, aircrafts, time):
    franja_inici = _time_to_minutes(time)
    if franja_inici == -1:
        return -1
    franja_fi = franja_inici + 59

    # 1. Alliberar portes d'avions que ja han sortit abans d'aquesta hora
    for ac in aircrafts:
        dep_time_str = getattr(ac, 'departuretime', '00:00')
        dep_min = _time_to_minutes(dep_time_str)
        if dep_min != -1 and dep_min <= franja_inici:
            FreeGate(bcn, ac)  # ◄ CORREGIT: Passem l'objecte avió 'ac', no el text 'ac.id'

    # 2. Assignar noves portes als avions que arriben en aquesta hora
    no_assignats = 0
    for ac in aircrafts:
        arr_min = _time_to_minutes(ac.time)
        if arr_min == -1 or ac.time == '00:00':
            continue
        if franja_inici <= arr_min <= franja_fi:
            resultat = AssignGate(bcn, ac)
            if resultat == -1:
                no_assignats += 1

    return no_assignats


def PlotDayOccupancy(bcn, aircrafts):
    # ◄ AFEGIT: Resetejar totes les portes abans d'iniciar la simulació del dia complet
    for terminal in bcn.terminals:
        for area in terminal.areas:
            for gate in area.gates:
                gate.occupied = False
                gate.aircraft_id = ""
                gate.time = ""
                gate.departuretime = ""

    # Assignar primer els avions nocturnos que ja dormen a l'aeroport (V4)
    AssignNightGates(bcn, aircrafts)

    hores = list(range(24))
    dades_terminals = {t.name: [] for t in bcn.terminals}
    no_assignats_per_hora = []

    for h in hores:
        time_str = f"{h:02d}:00"
        no_ass = AssignGatesAtTime(bcn, aircrafts, time_str)
        if no_ass < 0:
            no_ass = 0
        no_assignats_per_hora.append(no_ass)

        for terminal in bcn.terminals:
            ocupades = 0
            for area in terminal.areas:
                for gate in area.gates:
                    if gate.occupied:
                        ocupades += 1
            dades_terminals[terminal.name].append(ocupades)

    # Dibuix de les dues gràfiques temporals combinades
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle("Ocupació de portes al llarg del dia - LEBL (v4)", fontsize=14)

    colors = ['#1F4E79', '#DD8452', '#55A868', '#C44E52']
    for i, (nom_terminal, ocupacions) in enumerate(dades_terminals.items()):
        ax1.plot(hores, ocupacions, marker='o', label=nom_terminal,
                 color=colors[i % len(colors)], linewidth=2)

    ax1.set_title("Portes ocupades per terminal")
    ax1.set_xlabel("Hora del dia")
    ax1.set_ylabel("Portes ocupades")
    ax1.set_xticks(hores)
    ax1.set_xticklabels([f"{h:02d}:00" for h in hores], rotation=45, fontsize=7)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.bar(hores, no_assignats_per_hora, color='#C44E52', alpha=0.7)
    ax2.set_title("Avions no assignats per falta de portes lliures")
    ax2.set_xlabel("Hora del dia")
    ax2.set_ylabel("Avions no assignats")
    ax2.set_xticks(hores)
    ax2.set_xticklabels([f"{h:02d}:00" for h in hores], rotation=45, fontsize=7)
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.show()
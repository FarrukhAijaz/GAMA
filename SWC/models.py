class Direction:
    def __init__(self, source, destination, label=None):
        self.destination = source
        self.source = destination
        self.label = label

    def __str__(self):
        return f"Direction({self.source} -> {self.destination}, Label={self.label})"

class Signal:
    def __init__(self, name, raw_name):
        self.name = name
        self.raw_name = raw_name
        self.directions = []  # List of Direction
        self.attributes = {}  # Common attributes (if any)
        self.data_type = None  # Initialize the data_type attribute

    def add_direction(self, direction):
        self.directions.append(direction)

    def set_attributes(self, attributes):
        self.attributes = attributes

    def set_data_type(self, data_type):
        """Set the data type of the signal."""
        self.data_type = data_type

    def __str__(self):
        attr_str = ', '.join(f"{k}: {v}" for k, v in self.attributes.items())
        directions_str = '\n      '.join(str(d) for d in self.directions)
        data_type_str = f"Data Type: {self.data_type}" if self.data_type else ""
        if attr_str:
            return f"Signal({self.name} [{self.raw_name}])\n      {directions_str}\n      Attributes: {attr_str}\n      {data_type_str}"
        else:
            return f"Signal({self.name} [{self.raw_name}])\n      {directions_str}\n      {data_type_str}"




class Unit:
    def __init__(self, name, unit_id):
        self.name = name
        self.unit_id = unit_id
        self.signals = []

    def add_signal(self, signal):
        self.signals.append(signal)

    def __str__(self):
        signals_str = "\n    ".join(str(sig) for sig in self.signals)
        return f"Unit({self.name}, ID={self.unit_id})\n    {signals_str}"


class SWC:
    def __init__(self, name):
        self.name = name
        self.units = {}
        self.outer_signals = []
        self.inner_signals = []

    def add_unit(self, unit):
        self.units[unit.unit_id] = unit

    def add_outer_signal(self, signal):
        self.outer_signals.append(signal)

    def add_inner_signal(self, signal):
        self.inner_signals.append(signal)

    def __str__(self):
        units_str = "\n".join(str(u) for u in self.units.values())
        return (
            f"SWC({self.name})\nUnits:\n{units_str}\n\n"
            f"Outer Signals:\n" + "\n".join(str(s) for s in self.outer_signals) +
            "\n\nInner Signals:\n" + "\n".join(str(s) for s in self.inner_signals)
        )

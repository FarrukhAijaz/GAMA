import re
from SWC.models import SWC, Unit, Signal, Direction

#from models import SWC, Unit, Signal, Direction


def parse_swc_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    swc = None
    parsing_state = None
    current_unit = None
    current_signal = None
    current_connector = None

    for line in lines:
        line = line.strip()

        if line.startswith("Package Name:"):
            swc_name = line.split(":", 1)[1].strip()
            swc = SWC(swc_name)

        elif line == "Units:":
            parsing_state = "units"

        elif line == "Connectors:":
            parsing_state = "connectors"

        elif line == "Outer Signals:":
            parsing_state = "outer_signals"

        elif line == "Inner Signals:":
            parsing_state = "inner_signals"

        # === UNITS ===
        elif parsing_state == "units":
            if line.startswith("- "):
                unit_name = line[2:].strip()
                current_unit = {"name": unit_name}
            elif "ID" in line:
                current_unit["id"] = line.split(":")[1].strip()
                unit_obj = Unit(current_unit["name"], current_unit["id"])
                swc.add_unit(unit_obj)
                current_unit = None

        # === CONNECTORS ===
        elif parsing_state == "connectors":
            if line.startswith("Connector ID:"):
                connector_id = line.split(":", 1)[1].strip()
                current_connector = {
                    "id": connector_id,
                    "start": None,
                    "end": None,
                    "label": None,
                    "signals": []
                }

            elif "Start_Component_ID" in line:
                current_connector["start"] = line.split(":", 1)[1].strip()

            elif "End_Component_ID" in line:
                current_connector["end"] = line.split(":", 1)[1].strip()

            elif "Top/Mid Label" in line:
                current_connector["label"] = line.split(":", 1)[1].strip()

            elif line.startswith("- "):
                m = re.match(r"- (\w+) \(Raw: (.*?), Direction: (.*?)\)", line)
                if m:
                    name, raw, direction_type = m.groups()
                    current_signal = {
                        "name": name,
                        "raw": raw,
                        "dir_type": direction_type,
                        "attributes": {}
                    }

            elif line.startswith("*"):
                if current_signal is not None:
                    k, v = line.strip("* ").split(":", 1)
                    current_signal["attributes"][k.strip()] = v.strip()

            elif current_signal:
                start_id = current_connector["start"]
                end_id = current_connector["end"]
                label = current_connector["label"]

                come = swc.units[end_id].name if end_id in swc.units else f"Unit_{end_id}"
                go = swc.units[start_id].name if start_id in swc.units else f"Unit_{start_id}"
                direction = Direction(come, go, label)

                # Extract data type from attributes
                data_type = current_signal["attributes"].get("data_type", "double")  # Default to double if not found

                # Reuse signal if it exists
                unit = swc.units.get(end_id)
                if unit:
                    existing = next((s for s in unit.signals if s.raw_name == current_signal["raw"]), None)
                    if not existing:
                        signal = Signal(current_signal["name"], current_signal["raw"])
                        signal.set_data_type(data_type)  # Set the extracted data type
                        signal.add_direction(direction)  # Add direction to the signal
                        signal.set_attributes(current_signal["attributes"])  # Set attributes
                        unit.add_signal(signal)
                    else:
                        existing.add_direction(direction)  # Add direction to existing signal

                current_signal = None

        # === OUTER SIGNALS ===
        elif parsing_state == "outer_signals":
            if line.startswith("- "):
                m = re.match(r"- (\w+) \(Raw: (.*?), Direction: (.*?)\)", line)
                if m:
                    name, raw, direction_type = m.groups()
                    current_signal = {
                        "name": name,
                        "raw": raw,
                        "dir_type": direction_type,
                        "attributes": {}
                    }

            elif line.startswith("*"):
                if current_signal is not None:
                    k, v = line.strip("* ").split(":", 1)
                    current_signal["attributes"][k.strip()] = v.strip()

            elif current_signal:
                direction = Direction("External", "SWC", None)
                
                # Extract data type from attributes
                data_type = current_signal["attributes"].get("data_type", "double")  # Default to double if not found

                signal = Signal(current_signal["name"], current_signal["raw"])
                signal.set_data_type(data_type)  # Set the extracted data type
                signal.add_direction(direction)  # Add direction to the signal
                signal.set_attributes(current_signal["attributes"])  # Set attributes
                swc.add_outer_signal(signal)
                current_signal = None

        # === INNER SIGNALS ===
        elif parsing_state == "inner_signals":
            if line.startswith("- "):
                m = re.match(r"- (\w+) \(Raw: (.*?), Direction: (.*?)\)", line)
                if m:
                    name, raw, direction_type = m.groups()
                    current_signal = {
                        "name": name,
                        "raw": raw,
                        "dir_type": direction_type,
                        "attributes": {}
                    }

            elif line.startswith("*"):
                if current_signal is not None:
                    k, v = line.strip("* ").split(":", 1)
                    current_signal["attributes"][k.strip()] = v.strip()

            elif current_signal:
                direction = Direction("SWC", "SWC", None)
                
                # Extract data type from attributes
                data_type = current_signal["attributes"].get("data_type", "double")  # Default to double if not found

                signal = Signal(current_signal["name"], current_signal["raw"])
                signal.set_data_type(data_type)  # Set the extracted data type
                signal.add_direction(direction)  # Add direction to the signal
                signal.set_attributes(current_signal["attributes"])  # Set attributes
                swc.add_inner_signal(signal)
                current_signal = None

    return swc
filepath= "/home/saijaz/Desktop/GAMA/GAMA/SWC/test.txt"
swc = parse_swc_file(filepath)
print (swc)
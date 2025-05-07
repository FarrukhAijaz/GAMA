import os
import matlab.engine    
#from simulink_helper import create_subcomponent_model
from SWC.parser import parse_swc_file

def get_num_subcomponents(swc):
    """Returns the number of subcomponents in the parsed SWC object."""
    return len(swc.units)
def get_num_units_for_subcomponent(swc, subcomponent_name):
    """Returns the number of units in the specified subcomponent."""
    if subcomponent_name in swc.units:
        return 1
    return 0
def create_unit_model_from_parsed(unit, subcomponent_dir, subcomponent_name, eng):
    """Create a unit model in Simulink from a parsed unit."""
    unit_name = unit.name
    unit_dir = os.path.join(subcomponent_dir, unit_name)
    os.makedirs(unit_dir, exist_ok=True)

    unit_slx = os.path.join(unit_dir, f"{unit_name}.slx")
    eng.new_system(unit_name, nargout=0)

    # Create blocks for each signal in the unit
    for signal in unit.signals:
        signal_name = signal.name
        signal_data_type = signal.data_type

        # Add Inport, Gain block (or other types depending on your needs)
        eng.add_block('simulink/Sources/In1', f"{unit_name}/{signal_name}_In1", nargout=0)
        eng.add_block('simulink/Math Operations/Gain', f"{unit_name}/{signal_name}_Gain", nargout=0)
        eng.add_block('simulink/Sinks/Out1', f"{unit_name}/{signal_name}_Out1", nargout=0)

        # Set parameters
        eng.set_param(f"{unit_name}/{signal_name}_Gain", 'Gain', '5', nargout=0)
        eng.set_param(f"{unit_name}/{signal_name}_In1", 'Position', '[100, 100, 130, 130]', nargout=0)
        eng.set_param(f"{unit_name}/{signal_name}_Gain", 'Position', '[200, 100, 230, 130]', nargout=0)
        eng.set_param(f"{unit_name}/{signal_name}_Out1", 'Position', '[300, 100, 330, 130]', nargout=0)

        # Connect blocks based on directions
        for direction in signal.directions:
            source_block = f"{unit_name}/{direction.source}_Out1"
            destination_block = f"{unit_name}/{direction.destination}_In1"
            eng.add_line(unit_name, f"{source_block}/1", f"{destination_block}/1", nargout=0)

    # Save the unit system
    eng.save_system(unit_name, unit_slx, nargout=0)

    # Add a Model Reference block in the subcomponent and reference the unit model
    add_model_reference_to_subcomponent(eng, subcomponent_name, unit_name)
def add_model_reference_to_subcomponent(eng, subcomponent_name, unit_name):
    """Add a Model Reference block to the subcomponent model."""
    model_ref_block_name = f"{subcomponent_name}/ModelReference_{unit_name}"
    eng.add_block('simulink/Ports & Subsystems/Model', model_ref_block_name, nargout=0)
    eng.set_param(model_ref_block_name, 'ModelName', unit_name, nargout=0)

    # Position the Model Reference block
    eng.set_param(model_ref_block_name, 'Position', '[100, 100, 150, 130]', nargout=0)

def create_autosar_structure(swc, base_directory=None):
    # Start MATLAB engine
    eng = matlab.engine.start_matlab()

    # Define the base directory (Desktop in Ubuntu)
    if base_directory is None:
        base_directory = os.path.expanduser('~/Desktop')
    
    # Create SWC directory
    swc_dir = os.path.join(base_directory, swc.name)
    os.makedirs(swc_dir, exist_ok=True)
    
    # Create SWC .slx file
    swc_slx = os.path.join(swc_dir, f"{swc.name}.slx")
    eng.new_system(swc.name, nargout=0)
    
    # Loop through each subcomponent
    num_subcomponents = get_num_subcomponents(swc)
    for i, subcomponent_name in enumerate(swc.units.keys(), 1):
        subcomponent_dir = os.path.join(swc_dir, f"subcomponent_{i}")
        os.makedirs(subcomponent_dir, exist_ok=True)

        # Create each unit within the subcomponent
        num_units = get_num_units_for_subcomponent(swc, subcomponent_name)
        subcomponent_slx = os.path.join(subcomponent_dir, f"{subcomponent_name}.slx")
        eng.new_system(subcomponent_name, nargout=0)

        for unit in swc.units[subcomponent_name]:
            create_unit_model_from_parsed(unit, subcomponent_dir, subcomponent_name, eng)

        # Save the subcomponent model
        eng.save_system(subcomponent_name, subcomponent_slx, nargout=0)

        # Add a Model Reference block in the SWC and reference the subcomponent model
        add_model_reference_to_subcomponent(eng, swc.name, subcomponent_name)

    # Save the main SWC model
    eng.save_system(swc.name, swc_slx, nargout=0)
    
    # Stop MATLAB engine
    eng.quit()

    print(f"Successfully created AUTOSAR structure for {swc.name} at {swc_dir}")
# Parse the SWC file
filepath = "/home/saijaz/Desktop/GAMA/GAMA/SWC/test.txt"
swc = parse_swc_file(filepath)

# Create the AUTOSAR structure using the parsed SWC object
#create_autosar_structure(swc, base_directory=None)

"""Vessel_sizing by Nikita Blinov, blinov_n_a@mail.ru,
GitHub page: https://github.com/kjkdaioh/vessel_sizing
Software for selection, sizing and completion of questionnaires for
vessels, drums and separators in chemical technology."""

import math


def k_value_calculation(carry_over, demister, surface_tension, liq1_density, vapor_density):
    """This function calculates K value depending on presence and abscence of demister.
    Function might be used for all types of vessels"""
    if demister == 'N':
        k_value = 3.145 * carry_over ** (1 / 3) * (surface_tension / 1000 / (liq1_density - vapor_density)) ** 0.25
    elif demister == 'Y':
        k_value = max(0.08, 0.15 * (liq1_density / vapor_density - 1) ** - 0.2)
    return k_value


def vertical_vessel_min_diameter(k_value, liq1_density, vapor_density, vl_safety_factor,
                                 vapor_mass_flow):
    """Calculation of minimum acceptable minimum diameter for vertical vessel.
    Take a note that to choose min diameter for 3-phases vessel, necessary to calculate requirement for LL
    separation. This function calculates VL separation only."""
    allowable_gas_velocity = k_value * (liq1_density / vapor_density - 1) ** 0.5 * vl_safety_factor
    actual_gas_rate = vapor_mass_flow / vapor_density / 3600
    required_demister_area = actual_gas_rate / allowable_gas_velocity
    min_diameter = (4 * required_demister_area / 3.1415) ** 0.5
    return min_diameter


def demister_dimensions(k_value, liq1_density, vapor_density, vl_safety_factor,
                        vapor_mass_flow):
    """Calculation of demister dimensions which can be used for any vessel, but can be used
    for circle demister only. To update for rectangular demister in future."""
    allowable_gas_velocity = k_value * (liq1_density / vapor_density - 1) ** 0.5 * vl_safety_factor
    actual_gas_rate = vapor_mass_flow / vapor_density / 3600
    required_demister_area = actual_gas_rate / allowable_gas_velocity
    demister_diameter = (4 * required_demister_area / 3.1415) ** 0.5
    return demister_diameter


def choose_bottom_to_LSAL_for_vertical_sep(head_and_bottom, vessel_diameter):
    """This function sets distance from bottom tangent line to LSAL for vertical 2-phase vessel"""
    if head_and_bottom == 'E':
        h_0 = 0.5
    elif head_and_bottom == 'S':
        h_0 = -0.25 * vessel_diameter
    return h_0


def calc_bottom_volume_for_vertical_sep(head_and_bottom, vessel_diameter, h_0):
    """ This function calculates bottom inventory for lowest part of vertical separator """
    if head_and_bottom == 'E':
        bot_vol = (0.0416667 * vessel_diameter + 0.25 * h_0) * 3.1415 * vessel_diameter ** 2
    elif head_and_bottom == 'S':
        bot_vol = 0.029889 * 3.1415 * vessel_diameter ** 3
    return bot_vol


def calc_liquid_zone_for_vertical_vessel(residence_time, vessel_diameter, zone_number,
                                         liquid_flow, liquid_density, head_and_bottom):
    """This function calculates height of zones with liquid for vertical separator.
     If spherical bottom (for zone1) formula includes addition of 0.02 * vessel_diameter."""
    if head_and_bottom == 'S' and zone_number == 1:
        zone_height = residence_time * liquid_flow / 3600 / liquid_density / 3.1415 * 4 / vessel_diameter ** 2\
                      + 0.02 * vessel_diameter
    else:
        zone_height = residence_time * liquid_flow / 3600 / liquid_density / 3.1415 * 4 / vessel_diameter ** 2
    return zone_height


def set_demister_height(vessel_orientation, demister):
    """This function sets height of demister for vertical or horizontal vessel.
    if there is no demister height is set to 0."""
    if demister == 'Y':
        if vessel_orientation == 'V':
            h_6 = 0.15
        elif vessel_orientation == 'H':
            h_6 = 0.1
    elif demister == 'N':
        h_6 = 0
    return h_6


def calculate_vertical_vessel_head_and_bottom_height(vessel_diameter, head_and_bottom):
    """This function calculates height of head and bottom for vertical vessel, depending on
    head and bottom type"""
    if head_and_bottom == 'S':
        h_8 = vessel_diameter / 2
    elif head_and_bottom == 'E':
        h_8 = vessel_diameter / 4
    return h_8


def calc_height_from_top_of_demister_to_top_of_vertical_vessel(vessel_diameter):
    """This function calculates height from the top of demister to top tangent line for vertical vessel
    with demister"""
    X = 0.4 * vessel_diameter
    return X


def calc_height_from_top_of_demister_to_tangent_of_vertical_vessel(X, h_8, vessel_diameter,
                                                                   demister_diameter, demister):
    """This function calculates height from the top of demister to top tangent line for vertical vessel"""
    if demister == 'Y':
        if vessel_diameter * 0.75 > demister_diameter:
            h_7 = max(X - h_8, 0.15)
        else:
            h_7 = 0.15
    elif demister == 'N':
        h_7 = 0
    return h_7


def calc_height_from_inlet_nozzle_for_vertical_vessel(equipment_app, h_0, demister, min_diameter, h_8,
                                                      vessel_diameter):
    """Function calculates H_5 - height from inlet nozzle to demister for vertical vessel
    with demister or height from inlet nozzle to top tangent line of vertical vessel w/o
    demister. Also for vessel with negligible gas flow it sets H_5 equal to H_8."""
    if equipment_app == "1":
        h_5 = h_0
    elif equipment_app == "2":
        if demister == 'Y':
            h_5 = max(0.6, 0.6 * min_diameter)
        elif demister == 'N':
            h_5 = max(1, vessel_diameter, 0.6 + h_8) - h_8
    return h_5


def main():
    # User needs to enter working flow, pressure and temperature:
    working_temperature = 0
    working_pressure = 0
    vapor_mass_flow = 0
    vapor_density = 0
    vapor_viscosity = 0
    vapor_molecular_weight = 0
    liq1_mass_flow = 0
    liq1_density = 0
    liq1_viscosity = 0
    liq2_mass_flow = 0
    liq2_density = 0
    liq2_viscosity = 0
    surface_tension = 0

    # User has to fill equipment_tag and equipment_name; later this data will
    # be used in equipment specification
    equipment_tag = input('Enter equipment id: ')
    equipment_name = input('Enter equipment name: ')

    # Choose equipment application
    equipment_app = ''
    while equipment_app != '1' and equipment_app != '2':
        equipment_app = input('Choose equipment application: 1 - storage/surge, 2 - separation: ')

    if equipment_app == '2':
        # Choose amount of phases: 2 or 3
        amount_of_phases = ''
        while amount_of_phases != '2' and amount_of_phases != '3':
            amount_of_phases = input('Choose amount of phases: 2 for tho-phase separation,'
                                     ' 3 for three-phase separation: ')

    # Entering working temperature, necessary for calculation
    while True:
        working_temperature = input('Enter working temperature, degC: ')
        try:
            # temperature shall be higher than 0 K
            if (float(working_temperature) + 273.15) >= 0:
                break
        except ValueError:
            continue
    working_temperature = float(working_temperature)

    # Entering working pressure, necessary for calculation
    while True:
        working_pressure = input('Enter working pressure, kg/cm^2: ')
        try:
            # We are using absolute pressure, so it shall be higher than 0
            if float(working_pressure) >= 0:
                break
        except ValueError:
            continue
    working_pressure = float(working_pressure)

    # Entering liquid 1 mass flow.
    while True:
        liq1_mass_flow = input('Enter liquid 1 mass flow, kg/h: ')
        try:
            # mass flow can not be negative
            if float(liq1_mass_flow) >= 0:
                break
        except ValueError:
            continue
    liq1_mass_flow = float(liq1_mass_flow)

    # Entering liquid 1 density.
    while True:
        liq1_density = input('Enter liquid 1 density, kg/m^3: ')
        try:
            # density can not be negative
            if float(liq1_density) >= 0:
                break
        except ValueError:
            continue
    liq1_density = float(liq1_density)

    # Entering liquid 1 viscosity.
    while True:
        liq1_viscosity = input('Enter liquid 1 viscosity, cP: ')
        try:
            # viscosity can not be negative
            if float(liq1_viscosity) >= 0:
                break
        except ValueError:
            continue
    liq1_viscosity = float(liq1_viscosity)

    # Entering surface tension:
    while True:
        surface_tension = input('Enter surface tension, dyne/cm: ')
        try:
            # surface tension can not be negative
            if float(surface_tension) >= 0:
                break
        except ValueError:
            continue
    surface_tension = float(surface_tension)

    # Conditionally if equipment application is separator, we have to add data for gas flow:
    if equipment_app == '2':
        # Entering vapor mass flow.
        while True:
            vapor_mass_flow = input('Enter vapor mass flow, kg/h: ')
            try:
                # mass flow can not be negative
                if float(vapor_mass_flow) >= 0:
                    break
            except ValueError:
                continue
        vapor_mass_flow = float(vapor_mass_flow)

        # Entering vapor density.
        while True:
            vapor_density = input('Enter vapor density, kg/m^3: ')
            try:
                # vapor density can not be negative
                if float(vapor_density) >= 0:
                    break
            except ValueError:
                continue
        vapor_density = float(vapor_density)

        # Entering vapor viscosity.
        while True:
            vapor_viscosity = input('Enter vapor viscosity, cP: ')
            try:
                # vapor can not be negative
                if float(vapor_viscosity) >= 0:
                    break
            except ValueError:
                continue
        vapor_viscosity = float(vapor_viscosity)

        # Entering vapor molecular weight.
        while True:
            vapor_molecular_weight = input('Enter vapor molecular weight, kg/kmol: ')
            try:
                # molecular weight can not be negative
                if float(vapor_molecular_weight) >= 0:
                    break
            except ValueError:
                continue
        vapor_molecular_weight = float(vapor_molecular_weight)

    # Conditionally if separator is 3-phase, we have to add properties for liquid 2:
    try:
        if amount_of_phases == '3':
            # Entering liquid 2 mass flow.
            while True:
                liq2_mass_flow = input('Enter liquid 2 mass flow, kg/h: ')
                try:
                    # mass flow can not be negative
                    if float(liq2_mass_flow) >= 0:
                        break
                except ValueError:
                    continue
            liq2_mass_flow = float(liq2_mass_flow)

            # Entering liquid 2 density.
            while True:
                liq2_density = input('Enter liquid 2 density, kg/m^3: ')
                try:
                    # density can not be negative
                    if float(liq2_density) >= 0:
                        break
                except ValueError:
                    continue
            liq2_density = float(liq2_density)

            # Entering liquid 2 viscosity.
            while True:
                liq2_viscosity = input('Enter liquid 2 viscosity, cP: ')
                try:
                    # viscosity can not be negative
                    if float(liq2_viscosity) >= 0:
                        break
                except ValueError:
                    continue
            liq2_viscosity = float(liq2_viscosity)
    except NameError:
        pass

    # Set vessel orientation
    while True:
        vessel_orientation = input('Please set vessel orientation: V for vertical, H for horizontal: ')
        if vessel_orientation.upper() == 'H' or vessel_orientation.upper() == 'V':
            break
    vessel_orientation = vessel_orientation.upper()

    # Set head and bottom:
    while True:
        head_and_bottom = input('Please set vessel head and bottom: S for spherical, E for elleptic: ')
        if head_and_bottom.upper() == 'S' or head_and_bottom.upper() == 'E':
            break
    head_and_bottom = head_and_bottom.upper()

    # Use of demister: Y - for use, N - for no use.
    while True:
        demister = input('Please set necessity of demister: Y - need, N - don\'t need: ')
        if demister.upper() == 'Y' or demister.upper() == 'N':
            break
    demister = demister.upper()

    # Choose liq2 compartment type
    while True:
        compartment_type = input('Enter compartment type for liquid 2: boot or weir: ')
        if compartment_type == 'boot' or compartment_type == 'weir':
            break

    # Specify allowable liquid carryover (0.1 - equivalent to using demister,
    # 0.3 - good separation, 0.8% - fair separation, 2.5% - good separation not required.
    while True:
        carry_over = input('Enter carry-over value in %: ')
        try:
            # temperature shall be higher than 0 K
            if 0 <= float(carry_over) <= 100:
                break
        except ValueError:
            continue
    carry_over = float(carry_over) / 100

    k_value = k_value_calculation(carry_over, demister, surface_tension, liq1_density, vapor_density)

    def diameter_calculation(vessel_orientation, demister):
        if vessel_orientation == 'V':
            if demister == 'N':
                pass
            elif demister == 'Y':
                pass
        elif vessel_orientation == 'H':

            if demister == 'N':
                pass
            elif demister == 'Y':
                pass


if __name__ == '__main__':
    main()

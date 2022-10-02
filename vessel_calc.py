"""Vessel_sizing by Nikita Blinov, blinov_n_a@mail.ru,
GitHub page: https://github.com/kjkdaioh/vessel_sizing
Software for selection, sizing and completion of questionnaires for
vessels, drums and separators in chemical technology."""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import openpyxl



def k_value_calculation(carry_over, demister, surface_tension, liq1_density, vapor_density):
    """This function calculates K value depending on presence and absence of demister.
    Function might be used for all types of vessels"""
    k_value = 0
    try:
        if demister == False:
            k_value = 3.145 * float(carry_over) ** (1 / 3) * (float(surface_tension) / 1000 /
                                                              (float(liq1_density) - float(vapor_density))) ** 0.25
        elif demister == True:
            k_value = max(0.08, 0.15 * (float(liq1_density) / float(vapor_density) - 1) ** - 0.2)
        return round(k_value, 3)
    except ValueError:
        pass


def calculate_allowable_gas_velocity(k_value, liq1_density, vapor_density, vl_safety_factor):
    """This function calculates allowable gas density for vertical separator"""
    try:
        allowable_gas_velocity = float(k_value) * (float(liq1_density) / float(vapor_density) - 1) ** 0.5 * \
                                 float(vl_safety_factor)
        return round(allowable_gas_velocity, 2)
    except ValueError:
        pass


def calculate_actual_gas_rate(vapor_mass_flow, vapor_density):
    """This function calculates actual gas rate"""
    try:
        actual_gas_rate = float(vapor_mass_flow) / float(vapor_density) / 3600
        return round(actual_gas_rate, 3)
    except ValueError:
        pass


def vertical_vessel_min_diameter(actual_gas_rate, allowable_gas_velocity):
    """Calculation of minimum acceptable minimum diameter for vertical vessel.
    Take a note that to choose min diameter for 3-phases vessel, necessary to calculate requirement for LL
    separation. This function calculates VL separation only."""
    try:
        min_diameter = (4 * float(actual_gas_rate) / float(allowable_gas_velocity) / 3.1415) ** 0.5
        return round(min_diameter, 3)
    except ValueError:
        pass


def calculate_required_demister_area(actual_gas_rate, allowable_gas_velocity, demister):
    """Calculates and returns required demister area for any type of vessel"""
    try:
        if demister == True:
            required_demister_area = float(actual_gas_rate) / float(allowable_gas_velocity)
        else:
            required_demister_area = 0
        return round(required_demister_area, 3)
    except ValueError:
        pass


def calculate_demister_dimensions(required_demister_area):
    """Calculation of demister dimensions which can be used for any vessel, but can be used
    for circle demister only. To update for rectangular demister in future."""
    try:
        demister_dimensions = (4 * float(required_demister_area) / 3.1415) ** 0.5
        return round(demister_dimensions, 3)
    except ValueError:
        pass


def calculate_cross_area(vessel_diameter):
    try:
        cross_area = 3.1415 / 4 * float(vessel_diameter) ** 2
        return round(cross_area, 3)
    except ValueError:
        pass


def calculate_actual_gas_velocity(actual_gas_rate, cross_area):
    try:
        actual_gas_velocity = float(actual_gas_rate) / float(cross_area)
        return round(actual_gas_velocity, 3)
    except ValueError:
        pass


def calculate_bottom_to_LSAL(head_and_bottom, vessel_diameter, vessel_orientation):
    """This function sets distance from bottom tangent line to LSAL for vertical 2-phase vessel,
    if vessel is not vertical - set to 0"""
    try:
        if vessel_orientation == 'V':
            if head_and_bottom == 'E':
                bottom_to_LSAL = 0.5
            else:
                bottom_to_LSAL = -0.25 * float(vessel_diameter)
        else:
            bottom_to_LSAL = 0
        return round(bottom_to_LSAL, 3)
    except ValueError:
        pass


def calc_bottom_volume_for_vertical_sep(head_and_bottom, vessel_diameter, bottom_to_LSAL, vessel_orientation):
    """ This function calculates bottom inventory for lowest part of vertical separator """
    try:
        if vessel_orientation == 'V':
            if head_and_bottom == 'E':
                bottom_vol = (0.0416667 * float(vessel_diameter) + 0.25 * float(bottom_to_LSAL)) *\
                             3.1415 * float(vessel_diameter) ** 2
            else:
                bottom_vol = 0.029889 * 3.1415 * float(vessel_diameter) ** 3
        else:
            bottom_vol = 0
        return round(bottom_vol, 3)
    except ValueError:
        pass


def calc_liquid_zone_inventory(liquid1_mass_flow, liquid1_density, residence_time):
    """This function calculates liquid zone inventory based on residence time requirement"""
    try:
        liquid_zone_inventory = float(liquid1_mass_flow) / float(liquid1_density) * float(residence_time) / 60
        return round(liquid_zone_inventory, 3)
    except ValueError:
        pass


def calc_liquid_zone_height_for_vertical_vessel(inventory, cross_area, vessel_diameter,
                                                head_and_bottom, vessel_phase, zone1):
    """This function calculates height of zones with liquid for vertical separator.
     If spherical bottom (for zone1) formula includes addition of 0.02 * vessel_diameter."""
    # TODO: Update function for horizontal vessel and add conditon for 3phase vessel.
    try:
        if head_and_bottom == 'S' and (vessel_phase == 2 and zone1 is True):
            zone_height = float(inventory) / float(cross_area) + 0.02 * float(vessel_diameter)
        else:
            zone_height = float(inventory) / float(cross_area)
        return round(zone_height, 3)
    except ValueError:
        pass


def recalculate_liquid_inventory(rewritten_height, cross_area):
    """This function recalculates liquid inventory basing on adjusted liquid height and
    vessel diameter"""
    # ToDO: check for horizontal vessel as well
    try:
        recalculated_inventory = float(rewritten_height) * float(cross_area)
        return round(recalculated_inventory, 3)
    except ValueError:
        pass


def calculate_lsah_to_inlet(vessel_diameter):
    """Function calculates height from LSAH to inlet nozzle"""
    # TODO: add for horizontal vessel!
    try:
        return round(max(0.3 * float(vessel_diameter), 0.3), 3)
    except ValueError:
        pass


def calculate_inlet_to_demister(vessel_diameter):
    """Function calculates height from LSAH to inlet nozzle"""
    # TODO: add for horizontal vessel!
    try:
        return round(max(0.3 * float(vessel_diameter), 0.3), 3)
    except ValueError:
        pass


def calc_height_from_inlet_nozzle_for_vertical_vessel(vessel_application, bottom_entry_rewrite, demister,
                                                     head_and_bottom, vessel_diameter):
    """Function calculates height from inlet nozzle to demister for vertical vessel
    with demister or height from inlet nozzle to top tangent line of vertical vessel w/o
    demister. Also for vessel with negligible gas flow it sets H_5 equal to H_8."""
    try:
        if head_and_bottom == 'E':
            head_height = float(vessel_diameter) / 4
        else:
            head_height = float(vessel_diameter) / 2
        if vessel_application == 1:
            h_5 = float(bottom_entry_rewrite)
        elif vessel_application == 2:
            if demister == True:
                h_5 = max(0.6, 0.6 * float(vessel_diameter))
            elif demister == False:
                h_5 = max(1, float(vessel_diameter), 0.6 + head_height) - head_height
        return round(h_5, 3)
    except ValueError:
        pass


def set_demister_height(vessel_orientation, demister):
    """This function sets height of demister for vertical or horizontal vessel.
    if there is no demister height is set to 0."""
    try:
        if demister is True:
            if vessel_orientation == 'V':
                h_6 = 0.15
            elif vessel_orientation == 'H':
                h_6 = 0.1
            else:
                h_6 = None
        elif demister is False:
            h_6 = 0
        return h_6
    except ValueError:
        pass


def calc_height_from_top_of_demister_to_tangent_of_vertical_vessel(vessel_diameter, head_and_bottom,
                                                                   demister_diameter, demister):
    """This function calculates height from the top of demister to top tangent line for vertical vessel"""
    try:
        if demister is True:
            if float(vessel_diameter) * 0.75 > float(demister_diameter):
                if head_and_bottom == 'E':
                    h_7 = max(0.4 * float(vessel_diameter) - float(vessel_diameter) / 4, 0.15)
                else:
                    h_7 = max(0.4 * float(vessel_diameter) - float(vessel_diameter) / 2, 0.15)
            else:
                h_7 = 0.15
        elif demister is False:
            h_7 = 0
        return round(h_7, 3)
    except ValueError:
        pass


def calc_tan_to_tan_height(*args):
    """Function calculates tangent to tangent length of vertical vessel"""
    try:
        tan_to_tan = 0
        for arg in args:
            if arg != '':
                tan_to_tan += float(arg)
        return round(tan_to_tan, 3)
    except ValueError:
        pass


def calc_nozzle_velocity(vap_mass_flow, vapor_density, liquid1_mass_flow, liquid1_density,
                         liquid2_mass_flow, liquid2_density, pipe_internal_diameter):
    """Calculation of velocity inside of the nozzle"""
    try:
        actual_vapor_flow = float(vap_mass_flow) / float(vapor_density)
        actual_liquid1_flow = float(liquid1_mass_flow) / float(liquid1_density)

        if liquid2_density == '0':
            velocity = (actual_liquid1_flow + actual_vapor_flow) / 3600 \
                       / (float(pipe_internal_diameter) ** 2 * 3.1415 / 4)
        else:
            actual_liquid2_flow = float(liquid2_mass_flow) / float(liquid2_density)
            velocity = (actual_liquid1_flow + actual_vapor_flow + actual_liquid2_flow) / 3600 \
                           / (float(pipe_internal_diameter) ** 2 * 3.1415 / 4)
        return round(velocity, 3)
    except ValueError: pass


def calc_nozzle_momentum(vap_mass_flow, vapor_density, liquid1_mass_flow, liquid1_density,
                         liquid2_mass_flow, liquid2_density, velocity):
    """Calculation of nozzle momentum"""
    try:
        actual_vapor_flow = float(vap_mass_flow) / float(vapor_density)
        actual_liquid1_flow = float(liquid1_mass_flow) / float(liquid1_density)
        if liquid2_density == '0':
            nozzle_momentum = float(velocity) ** 2 * (float(vap_mass_flow) + float(liquid1_mass_flow))/\
                                    (actual_vapor_flow + actual_liquid1_flow)
        else:
            actual_liquid2_flow = float(liquid2_mass_flow) / float(liquid2_density)
            nozzle_momentum = float(velocity) ** 2 * (float(vap_mass_flow) + float(liquid1_mass_flow) +
                              float(liquid2_mass_flow)) / (actual_vapor_flow + actual_liquid1_flow + actual_liquid2_flow)
        return round(nozzle_momentum, 1)
    except ValueError: pass


def calc_allowable_stress(design_temperature, material_list, material):
    """This function converts design temperature to F from C, creates temperature list, places
    design temperature in F to that list, finds left and right neighbour."""
    try:
        design_temperature_F = float(design_temperature) * 1.8 + 32
        t_list = [-20, 300, 400, 500, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, design_temperature_F]
        t_list.sort()
        a = t_list.index(design_temperature_F)
        t_lower, t_higher = t_list[a-1], t_list[a+1]
        try:
            all_stress_lower = float(material_list[material][str(t_lower)])
            all_stress_higher = float(material_list[material][str(t_lower)])
            prorate_stress = (design_temperature_F - t_lower) / (t_higher - t_lower) *\
                             (float(all_stress_higher) - float(all_stress_lower)) + float(all_stress_lower)
            return round(prorate_stress, 3)
        except KeyError: pass
    except ValueError: pass


def calc_design_stress(allowable_stress):
    """This function calculates design stress"""
    try:
        design_stress = float(allowable_stress) * 1000 / 14.2233
        return round(design_stress, 3)
    except ValueError: pass


def choose_material_density(material, density_list):
    try:
        material_density = density_list[material]
        return material_density
    except KeyError: pass


def calc_shell_thickness(design_pressure, vessel_diameter, design_stress, joint_eff, corr_allowance):
    try:
        shell_thickness = round(float(design_pressure) * float(vessel_diameter) / (2 * float(design_stress) *
                                                                                   float(joint_eff) - 1.2 * float(
                       design_pressure)) * 1000 + float(corr_allowance), 3)
        return max(shell_thickness, 10)
    except ValueError: pass


def calc_head_thickness(design_pressure, vessel_diameter, design_stress, joint_eff, corr_allowance, head_and_bottom):
    try:
        if head_and_bottom == 'E':
            shell_thickness = round(float(design_pressure) * float(vessel_diameter) / (2 * float(design_stress) *
                                                                                       float(joint_eff) - 0.2 * float(
                        design_pressure)) * 1000 + float(corr_allowance), 3)
            return max(shell_thickness, 10)
        elif head_and_bottom == 'S':
            shell_thickness = round(float(design_pressure) * float(vessel_diameter) / (4 * float(design_stress) *
                                                                                       float(joint_eff) - 0.4 * float(
                        design_pressure)) * 1000 + float(corr_allowance), 3)
            return max(shell_thickness, 10)
    except ValueError: pass


def calc_shell_surf_area(vessel_diameter, thickness, tan_to_tan):
    try:
        shell_surf_area = 3.1415 * (float(vessel_diameter) + float(thickness) / 2000) * float(tan_to_tan)
        return round(shell_surf_area, 3)
    except ValueError: pass


def calc_head_surf_area(vessel_diameter, thickness, head_and_bottom):
    try:
        if head_and_bottom == 'E':
            shell_surf_area = 1.09 * (float(vessel_diameter) + float(thickness) / 2000) ** 2
            return round(shell_surf_area, 3)
        elif head_and_bottom == 'S':
            shell_surf_area = 1.571 * (float(vessel_diameter) + float(thickness) / 2000) ** 2
            return round(shell_surf_area, 3)
    except ValueError:
        pass


def calc_weight(thickness, surf_area, metal_density):
    try:
        weight = float(thickness) / 1000 * float(surf_area) * float(metal_density)
        return round(weight, 3)
    except ValueError: pass


def calc_total_weight(shell_weight, head_weight):
    try:
        total_weight = float(shell_weight) + 2 * float(head_weight)
        return round(total_weight, 1)
    except ValueError: pass


def calc_vessel_volume(tan_to_tan_height, vessel_diameter, head_and_bottom):
    try:
        if head_and_bottom == 'E':
            vessel_volume = (float(tan_to_tan_height) + 1 / 3 * float(vessel_diameter)) * 3.1415 *\
                            float(vessel_diameter) ** 2 / 4
            return round(vessel_volume, 1)
        elif head_and_bottom == 'S':
            vessel_volume = (float(tan_to_tan_height) + 2 / 3 * float(vessel_diameter)) * 3.1415 * \
                            float(vessel_diameter) ** 2 / 4
            return round(vessel_volume, 1)
    except ValueError: pass


def calc_length_to_diameter_ratio(tan_to_tan_length, vessel_diameter):
    try:
        length_to_diameter_ratio = float(tan_to_tan_length) / float(vessel_diameter)
        return round(length_to_diameter_ratio, 1)
    except ValueError: pass


def get_separation_quality(vessel_diameter, min_vessel_diameter, entry):
    try:
        if vessel_diameter >= min_vessel_diameter:
            entry.configure(fg='green')
            return 'OK'
        else:
            entry.configure(fg='red')
            return 'Not OK'
    except ValueError: pass


def fetch_button_action(root, data_input_boxes):
    """This Function is for fetching data from excel file, mainly Data file.
    Data is taken from N column from certain rows. Address Data file if any
    further clarification needed."""
    root.filename = filedialog.askopenfilename(initialdir='C:/', title='Choose data file')
    wb = openpyxl.load_workbook(root.filename)
    sheet = wb.active
    for i in range(13):
        data_input_boxes[i].delete(first=0, last=None)
        cell = sheet['N' + str(i + 3)].value
        data_input_boxes[i].insert(0, str(round(cell, 3)))


def output_button_action(root, liq1_flow, liq1_density, vapor_flow, vapor_mol_weight, vapor_density,
                         oper_temp, oper_pressure, design_temperature, design_pressure, shell_id,
                         tan_to_tan_length, corr_allowance, insulation, shell_material,
                         demister):
    """This Function is for fetching data from excel file, mainly Data file.
    Data is taken from N column from certain rows. Address Data file if any
    further clarification needed."""
    root.filename = filedialog.askopenfilename(initialdir='C:/', title='Choose data file')
    wb = openpyxl.load_workbook(root.filename)
    sheet = wb.active
    sheet['F' + str(2)] = liq1_flow
    sheet['F' + str(3)] = liq1_density
    sheet['F' + str(4)] = vapor_flow
    sheet['F' + str(5)] = vapor_mol_weight
    sheet['F' + str(6)] = vapor_density
    sheet['F' + str(7)] = oper_temp
    sheet['F' + str(8)] = oper_pressure
    sheet['F' + str(9)] = design_temperature
    sheet['F' + str(10)] = design_pressure
    sheet['F' + str(12)] = float(shell_id) * 1000
    sheet['F' + str(13)] = float(tan_to_tan_length) * 1000
    sheet['F' + str(15)] = corr_allowance
    if insulation == 0:
        sheet['F' + str(17)] = 'No'
    elif insulation == 1:
        sheet['F' + str(17)] = 'PP'
    elif insulation == 2:
        sheet['F' + str(17)] = 'Hot'
    sheet['F' + str(18)] = shell_material
    if demister is True:
        sheet['F' + str(19)] = 'Yes'
    elif demister is False:
        sheet['F' + str(19)] = 'No'
    wb.save(root.filename)



def disable_compartment(value, weir_button, boot_button, compartment_type, liquid1_factor, liquid2_factor,
                        t11_box, t12_box, t13_box):
    """This function disables choice of compartment type for 2-phase separators,
    and enables for 3-phase separators, also it disables safety factors, except
    of vapor liquid safety factor and liquid 2 residence time input boxes for
    2-phase separator"""
    compartment_type.set(0)
    liquid1_factor.delete(0, END)
    liquid2_factor.delete(0, END)
    t11_box.delete(0, END)
    t12_box.delete(0, END)
    t13_box.delete(0, END)
    if value == 2:
        weir_button.configure(state=DISABLED)
        boot_button.configure(state=DISABLED)
        liquid1_factor.configure(state=DISABLED)
        liquid2_factor.configure(state=DISABLED)
        t11_box.configure(state=DISABLED)
        t12_box.configure(state=DISABLED)
        t13_box.configure(state=DISABLED)
    else:
        weir_button.configure(state=ACTIVE)
        boot_button.configure(state=ACTIVE)
        liquid1_factor.configure(state=NORMAL)
        liquid2_factor.configure(state=NORMAL)
        t11_box.configure(state=NORMAL)
        t12_box.configure(state=NORMAL)
        t13_box.configure(state=NORMAL)


def disable_demister(value, demister_box, demister):
    """This function disables demister box for storage/surge application,
    and enables for separation application"""
    demister.set(FALSE)
    if value == 1:
        demister_box.configure(state=DISABLED)
    else:
        demister_box.configure(state=ACTIVE)


def main():
    import openpyxl
    def update():
        """This function is intended for update of GUI every 1 second."""
        try:
            # for velocity variables:
            k_value_var.set(str(k_value_calculation(carry_over.get(), demister.get(), data_input_boxes[12].get(),
                                                    data_input_boxes[7].get(), data_input_boxes[3].get())))
            allowable_gas_velocity.set(str(calculate_allowable_gas_velocity(k_value.get(), data_input_boxes[7].get(),
                                                                            data_input_boxes[3].get(),
                                                                            vapor_liquid_factor.get())))
            actual_gas_rate.set(str(calculate_actual_gas_rate(data_input_boxes[2].get(), data_input_boxes[3].get())))
            minimal_vessel_diameter.set(str(vertical_vessel_min_diameter(velocity_entries[1].get(),
                                                                         velocity_entries[0].get())))
            required_demister_area.set(str(calculate_required_demister_area(velocity_entries[1].get(),
                                                                            velocity_entries[0].get(),
                                                                            demister.get())))
            demister_dimensions.set(str(calculate_demister_dimensions(velocity_entries[3].get())))
            cross_area.set(str(calculate_cross_area(vessel_diameter.get())))
            actual_gas_velocity.set(str(calculate_actual_gas_velocity(velocity_entries[1].get(),
                                                                      velocity_entries[5].get())))
            # For liquid 1 variables
            bottom_to_LSAL.set(str(calculate_bottom_to_LSAL(head_and_bottom.get(), vessel_diameter.get(),
                                                            vessel_orientation.get())))
            bottom_vol.set(str(calc_bottom_volume_for_vertical_sep(head_and_bottom.get(), vessel_diameter.get(),
                                                                   bottom_entry_rewrite.get(),
                                                                   vessel_orientation.get())))
            lsalToLalHeight.set(str(calc_liquid_zone_height_for_vertical_vessel
                                    (lsalToLalInv.get(), cross_area.get(), vessel_diameter.get(),
                                     head_and_bottom.get(), vessel_phase.get(), True)))
            lsalToLalInv.set(str(calc_liquid_zone_inventory(data_input_boxes[6].get(), data_input_boxes[7].get(),
                                                            t1_box.get())))
            lalToLahHeight.set(str(calc_liquid_zone_height_for_vertical_vessel
                                   (lalToLahInv.get(), cross_area.get(), vessel_diameter.get(),
                                    head_and_bottom.get(), vessel_phase.get(), False)))
            lalToLahInv.set(str(calc_liquid_zone_inventory(data_input_boxes[6].get(), data_input_boxes[7].get(),
                                                           t2_box.get())))
            lahToLsahHeight.set(str(calc_liquid_zone_height_for_vertical_vessel
                                    (lahToLsahInv.get(), cross_area.get(), vessel_diameter.get(),
                                     head_and_bottom.get(), vessel_phase.get(), False)))
            lahToLsahInv.set(str(calc_liquid_zone_inventory(data_input_boxes[6].get(), data_input_boxes[7].get(),
                                                             t3_box.get())))
            lsalToLalInvRecalc.set(str(recalculate_liquid_inventory(lsalToLalHeightRewrite.get(), cross_area.get())))
            lalToLahInvRecalc.set(str(recalculate_liquid_inventory(lalToLahHeightRewrite.get(), cross_area.get())))
            lahToLsahInvRecalc.set(str(recalculate_liquid_inventory(lahToLsahHeightRewrite.get(), cross_area.get())))
            lsahToInlet.set(str(calculate_lsah_to_inlet(vessel_diameter.get())))
            if vessel_orientation.get() == 'V':
                inletToDemister.set(str(calc_height_from_inlet_nozzle_for_vertical_vessel
                                        (vessel_application.get(), bottom_entry_rewrite.get(), demister.get(),
                                         head_and_bottom.get(), vessel_diameter.get())))
            demisterHeight.set(str(set_demister_height(vessel_orientation.get(), demister.get())))
            demisterToTangent.set(str(calc_height_from_top_of_demister_to_tangent_of_vertical_vessel
                                      (vessel_diameter.get(), head_and_bottom.get(), demister_dimensions.get(),
                                       demister.get())))
            tan_to_tan.set(str(calc_tan_to_tan_height(bottom_entry_rewrite.get(), lsalToLalHeightRewrite.get(),
                                                      lalToLahHeightRewrite.get(), lahToLsahHeightRewrite.get(),
                                                      lsahToInletEntryRewrite.get(), inletToDemisterEntryRewrite.get(),
                                                      demisterHeight.get(), demisterToTangentRewrite.get())))
            # Update schedule dropdown menu to include only existing schedules for certain diameter
            try:
                for i in sch_menus:
                    sch_menus[i] = OptionMenu(my_tab2, sch_var_list[i], *nd_voc[dn_var_list[i].get()])
                    sch_menus[i].grid(column=10, row=3 + i)
            except KeyError: pass
            # nozzle data updates:
            for i, variable in enumerate(internalDiameterVarList):
                try:
                    variable.set('')
                    variable.set(nd_voc[dn_var_list[i].get()][sch_var_list[i].get()])
                except KeyError: pass
            # Nozzle velocity updates
            speedVarList[0].set(str(calc_nozzle_velocity(data_input_boxes[2].get(), data_input_boxes[3].get(),
                                                         data_input_boxes[6].get(), data_input_boxes[7].get(),
                                                         data_input_boxes[9].get(), data_input_boxes[10].get(),
                                                         internalDiameterEntries[0].get())))
            speedVarList[1].set(str(calc_nozzle_velocity(data_input_boxes[2].get(), data_input_boxes[3].get(),
                                                         '0', data_input_boxes[7].get(),
                                                         '0', data_input_boxes[10].get(),
                                                         internalDiameterEntries[1].get())))
            speedVarList[2].set(str(calc_nozzle_velocity('0', data_input_boxes[3].get(),
                                                         data_input_boxes[6].get(), data_input_boxes[7].get(),
                                                         '0', data_input_boxes[10].get(),
                                                         internalDiameterEntries[2].get())))
            speedVarList[3].set(str(calc_nozzle_velocity('0', data_input_boxes[3].get(),
                                                         '0', data_input_boxes[7].get(),
                                                         data_input_boxes[9].get(), data_input_boxes[10].get(),
                                                         internalDiameterEntries[3].get())))
            # inlet nozzle momentum update
            rhoVsqrVarList[0].set(str(calc_nozzle_momentum(data_input_boxes[2].get(), data_input_boxes[3].get(),
                                                           data_input_boxes[6].get(), data_input_boxes[7].get(),
                                                           data_input_boxes[9].get(), data_input_boxes[10].get(),
                                                           speedEntries[0].get())))
            rhoVsqrVarList[1].set(str(calc_nozzle_momentum(data_input_boxes[2].get(), data_input_boxes[3].get(),
                                                           '0', data_input_boxes[7].get(),
                                                           '0', data_input_boxes[10].get(),
                                                           speedEntries[1].get())))
            rhoVsqrVarList[2].set(str(calc_nozzle_momentum('0', data_input_boxes[3].get(),
                                                           data_input_boxes[6].get(), data_input_boxes[7].get(),
                                                           '0', data_input_boxes[10].get(),
                                                           speedEntries[2].get())))
            rhoVsqrVarList[3].set(str(calc_nozzle_momentum('0', data_input_boxes[3].get(),
                                                           '0', data_input_boxes[7].get(),
                                                           data_input_boxes[9].get(), data_input_boxes[10].get(),
                                                           speedEntries[3].get())))
            allowable_stress.set(str(calc_allowable_stress(mech_entries[1].get(), metal_stress,
                                                           material_var.get())))
            design_stress.set(str(calc_design_stress(allowable_stress.get())))
            material_density.set(choose_material_density(material_var.get(), metal_density))
            # Thickness, area and weight updates:
            shell_var_list[0].set(str(calc_shell_thickness(mech_entries[0].get(), vessel_diameter.get(),
                                                           design_stress_entry.get(), mech_entries[3].get(),
                                                           mech_entries[2].get())))
            head_var_list[0].set(str(calc_head_thickness(mech_entries[0].get(), vessel_diameter.get(),
                                                         design_stress_entry.get(), mech_entries[3].get(),
                                                         mech_entries[2].get(), head_and_bottom.get())))
            shell_var_list[1].set(str(calc_shell_surf_area(vessel_diameter.get(), shell_var_list[0].get(),
                                                           tan_to_tan_rewrite.get())))
            head_var_list[1].set(str(calc_head_surf_area(vessel_diameter.get(), shell_var_list[0].get(),
                                                         head_and_bottom.get())))
            shell_var_list[2].set(str(calc_weight(shell_var_list[0].get(), shell_var_list[1].get(),
                                                  material_density_entry.get())))
            head_var_list[2].set(str(calc_weight(head_var_list[0].get(), head_var_list[1].get(),
                                                 material_density_entry.get())))
            head_var_list[3].set(str(calc_total_weight(shell_var_list[2].get(), head_var_list[2].get())))
            # Filling results tab:
            result_vars[0].set(vessel_diameter.get())
            result_vars[1].set(tan_to_tan_rewrite.get())
            result_vars[2].set(str(calc_length_to_diameter_ratio(result_vars[1].get(), result_vars[0].get())))
            result_vars[3].set(get_separation_quality(vessel_diameter.get(), minimal_vessel_diameter.get(),
                                                      result_entries[3]))
            result_vars[4].set(str(calc_vessel_volume(result_vars[1].get(), result_vars[0].get(),
                                                      head_and_bottom.get())))
            result_vars[5].set(head_var_list[3].get())

        except ZeroDivisionError:
            pass
        root.after(500, update)

    # Initializing tkinter, setting title and window size:
    root = Tk()
    root.title("Vessel sizing")
    root.geometry("1200x800")

    # Configure columns and rows in grid to automatically resize window:
    Grid.columnconfigure(root, 0, weight=1)
    Grid.rowconfigure(root, 0, weight=1)

    # Adding menu:
    my_menu = Menu(root)
    root.config(menu=my_menu)
    file_menu = Menu(my_menu)
    help_menu = Menu(my_menu)
    my_menu.add_cascade(label='File', menu=file_menu)
    my_menu.add_cascade(label='Help', menu=help_menu)
    file_menu.add_command(label='Exit', command=root.quit)

    # Adding tabs
    my_tabs = ttk.Notebook(root)
    my_tabs.grid(sticky="nsew")

    my_tab1 = Frame(my_tabs, width=1024, height=800)
    my_tab2 = Frame(my_tabs, width=1024, height=800)
    my_tab3 = Frame(my_tabs, width=1024, height=800)
    my_tab4 = Frame(my_tabs, width=1024, height=800)

    my_tab1.grid(sticky="nsew")
    my_tab2.grid(sticky="nsew")
    my_tab3.grid(sticky="nsew")
    my_tab4.grid(sticky="nsew")

    my_tabs.add(my_tab1, text='Data')
    my_tabs.add(my_tab2, text='Calculation')
    my_tabs.add(my_tab3, text='Result')
    my_tabs.add(my_tab4, text='Drawing')

    # Filling Data tab (my_tab1):
    # Creating header for initial data
    dataHeader = Label(my_tab1, text='Initial data:', pady=5, font=('Helvetica 10 bold'), padx=10)
    dataHeader.grid(column=0, row=0, sticky=W)

    # Listing all required parameters and units of measure to make labels:
    vocabulary_of_data = {'Parameter': 'UOM',
                          'Temperature': '°C',
                          'Pressure': 'kg/cm^2',
                          'Vapor mass flow': 'kg/h',
                          'Vapor density': 'kg/m^3',
                          'Vapor viscosity': 'cP',
                          'Vapor MW': 'kg/kmol',
                          'Liquid 1 mass flow': 'kg/h',
                          'Liquid 1 density': 'kg/m^3',
                          'Liquid 1 viscosity': 'cP',
                          'Liquid 2 mass flow': 'kg/h',
                          'Liquid 2 density': 'kg/m^3',
                          'Liquid 2 viscosity': 'cP',
                          'Surface tension': 'dyne/cm'}
    data_labels = {}
    for i, (k, v) in enumerate(vocabulary_of_data.items()):
        data_labels[k] = Label(my_tab1, text=k, padx=10, pady=2)
        data_labels[k].grid(column=0, row=i + 1, sticky=W)
        data_labels[v] = Label(my_tab1, text=v)
        data_labels[v].grid(column=1, row=i + 1)

    # Adding header for data inputs:
    header_for_data_inputs = Label(my_tab1, text='Value')
    header_for_data_inputs.grid(column=2, row=1, padx=10)

    # Adding multiple input boxes for initial data entering/fetching:
    data_input_boxes = {}
    for i in range(13):
        data_input_boxes[i] = Entry(my_tab1, width=10, justify=CENTER)
        data_input_boxes[i].grid(column=2, row=i + 2)

    # Adding fetch button, to be able to get data from excel data file:
    fetch_button = Button(my_tab1, text='Fetch', width=10, command=lambda: fetch_button_action(my_tab1,
                                                                                               data_input_boxes))
    fetch_button.grid(column=2)

    # Adding header for vessel choice:
    vessel_choice_header = Label(my_tab1, text='Vessel choice:', pady=5, font=('Helvetica 10 bold'), padx=10)
    vessel_choice_header.grid(sticky=W)
    # Header for vessel application
    vessel_application_header = Label(my_tab1, text='Vessel application', padx=10)
    vessel_application_header.grid(sticky=W)
    # Adding radio buttons for storage/surge and separation
    vessel_application = IntVar()
    Radiobutton(my_tab1, text='Storage/surge', variable=vessel_application, value=1,
                command=lambda: disable_demister(vessel_application.get(), demister_box, demister)) \
        .grid(column=0, row=18, sticky=W)
    Radiobutton(my_tab1, text='Separation', variable=vessel_application, value=2,
                command=lambda: disable_demister(vessel_application.get(), demister_box, demister)) \
        .grid(column=1, row=18)

    # Header for vessel orientation
    vessel_orientation_header = Label(my_tab1, text='Vessel orientation', padx=10)
    vessel_orientation_header.grid(sticky=W)
    # Adding radio buttons for vessel orientation
    vessel_orientation = StringVar()
    vessel_orientation.set('None')
    Radiobutton(my_tab1, text='Vertical', variable=vessel_orientation, value='V').grid(column=0, row=20, sticky=W)
    # Horizontal vessel calculations are not implemented yet, so it is disabled
    Radiobutton(my_tab1, text='Horizontal', variable=vessel_orientation, value='H',
                state=DISABLED).grid(column=1, row=20, sticky=W)

    # Header for amount of phases:
    vessel_phase_header = Label(my_tab1, text='Vessel phases', padx=10)
    vessel_phase_header.grid(sticky=W)
    # Adding radio buttons for phases
    vessel_phase = IntVar()
    Radiobutton(my_tab1, text='2 phases', variable=vessel_phase, value=2,
                command=lambda: disable_compartment(vessel_phase.get(), weir_button, boot_button, compartment_type,
                                                    liquid1_factor, liquid2_factor, t11_box, t12_box, t13_box)) \
        .grid(column=0, row=22, sticky=W)
    # Calculations for 3 phase vessel are not implemented yet, so it is disabled for the time being
    Radiobutton(my_tab1, text='3 phases', variable=vessel_phase, value=3,
                command=lambda: disable_compartment(vessel_phase.get(), weir_button, boot_button, compartment_type,
                                                    liquid1_factor, liquid2_factor, t11_box, t12_box, t13_box),
                state=DISABLED) \
        .grid(column=1, row=22, sticky=W)

    # Header for demister:
    demister_header = Label(my_tab1, text='Demister', padx=10)
    demister_header.grid(sticky=W, row=23)
    # Adding checkbox for demister
    demister = BooleanVar()
    demister_box = Checkbutton(my_tab1, variable=demister, onvalue=True, offvalue=False)
    demister_box.grid(row=23, column=1)

    # Header for compartment type:
    compartment_type_header = Label(my_tab1, text='Compartment type', padx=10)
    compartment_type_header.grid(sticky=W)
    # Adding radio buttons for phases
    compartment_type = StringVar()
    compartment_type.set('None')
    weir_button = Radiobutton(my_tab1, text='Weir', variable=compartment_type, value='Weir')
    boot_button = Radiobutton(my_tab1, text='Boot', variable=compartment_type, value='Boot')
    weir_button.grid(column=0, row=25, sticky=W)
    boot_button.grid(column=1, row=25, sticky=W)

    # Header for head and bottom type:
    head_bottom_header = Label(my_tab1, text='Head and bottom type', padx=10).grid(sticky=W)
    # Adding radio buttons for head and bottom type
    head_and_bottom = StringVar()
    head_and_bottom.set('None')
    elliptical = Radiobutton(my_tab1, text='Elliptical', variable=head_and_bottom, value='E')
    spherical = Radiobutton(my_tab1, text='Spherical', variable=head_and_bottom, value='S')
    elliptical.grid(column=0, sticky=W, row=27)
    spherical.grid(column=1, sticky=W, row=27)

    # Header for insulation type:
    insulation_type_header = Label(my_tab1, text='Insulation type', padx=10).grid(sticky=W)
    # Adding radio buttons for phases
    insulation_type = IntVar()
    no_insulation = Radiobutton(my_tab1, text='None', variable=insulation_type, value=0)
    pp_insulation = Radiobutton(my_tab1, text='PP', variable=insulation_type, value=1)
    hot_insulation = Radiobutton(my_tab1, text='Hot', variable=insulation_type, value=2)
    no_insulation.grid(column=0, row=29, sticky=W)
    pp_insulation.grid(column=1, row=29, sticky=W)
    hot_insulation.grid(column=2, row=29, sticky=W)

    # Header for vessel credentials:
    vessel_credentials = Label(my_tab1, text='Project information:', pady=5, font=('Helvetica 10 bold'), padx=25)
    vessel_credentials.grid(column=4, row=0, sticky=W, columnspan=2)
    # Adding labels for vor project and client
    project_name = Label(my_tab1, text='Project', padx=25).grid(column=4, row=1, sticky=W, columnspan=2)
    client_name = Label(my_tab1, text='Client', padx=25).grid(column=4, row=2, sticky=W, columnspan=2)
    # Adding input boxes for project and client
    project_name_box = Entry(my_tab1, width=33, justify=CENTER).grid(column=5, row=1, columnspan=2)
    client_name_box = Entry(my_tab1, width=33, justify=CENTER).grid(column=5, row=2, columnspan=2)
    # Adding labels for vor vessel name and tag
    vessel_name = Label(my_tab1, text='Vessel name', padx=25).grid(column=4, row=3, sticky=W, columnspan=2)
    vessel_id = Label(my_tab1, text='Vessel ID', padx=25).grid(column=4, row=4, sticky=W)
    # Adding input boxes for vessel name and tag
    vessel_name_box = Entry(my_tab1, width=33, justify=CENTER).grid(column=5, row=3, columnspan=2)
    vessel_id_box = Entry(my_tab1, width=33, justify=CENTER).grid(column=5, row=4, columnspan=2)

    # Header for safety factors:
    safety_factors = Label(my_tab1, text='Safety factors:', font=('Helvetica 10 bold'), padx=25)
    safety_factors.grid(column=4, row=5, sticky=W, columnspan=2)
    # Adding labels for safety factors:
    vapor_liquid_factor_label = Label(my_tab1, text='Safety factor for liquid vapor separation', padx=25) \
        .grid(column=4, row=6, sticky=W, columnspan=2)
    liquid1_factor_label = Label(my_tab1, text='Safety factor for liquid 1 separation', padx=25) \
        .grid(column=4, row=7, sticky=W, columnspan=2)
    liquid2_factor_label = Label(my_tab1, text='Safety factor for liquid 2 separation', padx=25) \
        .grid(column=4, row=8, sticky=W, columnspan=2)
    # Adding input boxes for safety factors:
    vapor_liquid_factor = Entry(my_tab1, width=8, justify=CENTER)
    vapor_liquid_factor.grid(column=6, row=6)
    liquid1_factor = Entry(my_tab1, width=8, justify=CENTER)
    liquid1_factor.grid(column=6, row=7)
    liquid2_factor = Entry(my_tab1, width=8, justify=CENTER)
    liquid2_factor.grid(column=6, row=8)

    # Residence times header
    residence_time_header = Label(my_tab1, text='Residence time:', font=('Helvetica 10 bold'),
                                  padx=25).grid(column=4, row=16, sticky=W, columnspan=2)
    # Adding labels for residence time for liquid 1:
    liquid1_label = Label(my_tab1, text='For liquid 1:', padx=25)
    t1_label = Label(my_tab1, text='Between LZAL and LAL, minutes') \
        .grid(column=4, row=18, sticky=W, columnspan=2, padx=25)
    t2_label = Label(my_tab1, text='Between LAL and LAH, minutes') \
        .grid(column=4, row=19, sticky=W, columnspan=2, padx=25)
    t3_label = Label(my_tab1, text='Between LAH and LZAH, minutes') \
        .grid(column=4, row=20, sticky=W, columnspan=2, padx=25)
    liquid1_label.grid(column=4, row=17, sticky=W, columnspan=1)
    # Adding input boxes for residence time for liquid 2:
    t1_box = Entry(my_tab1, justify=CENTER, width=8)
    t1_box.grid(column=6, row=18)
    t2_box = Entry(my_tab1, justify=CENTER, width=8)
    t2_box.grid(column=6, row=19)
    t3_box = Entry(my_tab1, justify=CENTER, width=8)
    t3_box.grid(column=6, row=20)
    # Adding labels for residence time for liquid 2, which shall be available only for vessel
    # with 3-phases
    liquid2_label = Label(my_tab1, text='For liquid 2:', padx=25) \
        .grid(column=4, row=21, sticky=W, columnspan=1)
    t11_label = Label(my_tab1, text='Between LZAL and LAL, minutes') \
        .grid(column=4, row=22, sticky=W, columnspan=2, padx=25)
    t12_label = Label(my_tab1, text='Between LAL and LAH, minutes') \
        .grid(column=4, row=23, sticky=W, columnspan=2, padx=25)
    t13_label = Label(my_tab1, text='Between LAH and LZAH, minutes') \
        .grid(column=4, row=24, sticky=W, columnspan=2, padx=25)
    # Adding input boxes for residence time for liquid 2:
    t11_box = Entry(my_tab1, justify=CENTER, width=8)
    t11_box.grid(column=6, row=22)
    t12_box = Entry(my_tab1, justify=CENTER, width=8)
    t12_box.grid(column=6, row=23)
    t13_box = Entry(my_tab1, justify=CENTER, width=8)
    t13_box.grid(column=6, row=24)

    # Filling calculation tab
    # Adding label and input for vessel diameter.
    vessel_diameter_label = Label(my_tab2, padx=10, text='Vessel diameter', pady=10)
    vessel_diameter_label.grid(column=0, row=0, sticky=W)
    vessel_diameter = Entry(my_tab2, width=8, justify=CENTER)
    vessel_diameter.grid(column=1, row=0, sticky=W)
    diameter_uom = Label(my_tab2, text='m').grid(column=3, row=0)

    # Adding velocity calculation:
    # Adding label for velocity calculation:
    velocity_calculation_header = Label(my_tab2, text='Velocity calculation:',
                                        pady=5, font=('Helvetica 10 bold'), padx=10)
    velocity_calculation_header.grid(sticky=W, columnspan=2)
    # Adding label and input box for carry-over:
    carry_over_label = Label(my_tab2, text='Carry-over', padx=10)
    carry_over_label.grid(sticky=W, column=0, row=2)
    carry_over = Entry(my_tab2, justify=CENTER, width=8)
    carry_over.grid(column=1, row=2)
    # Adding label and input box for Sounder-browns const:
    k_value_label = Label(my_tab2, text='K value', padx=10)
    k_value_label.grid(sticky=W, column=0, row=3)
    k_value_var = StringVar()
    k_value_input = Entry(my_tab2, width=8, justify=CENTER, textvariable=k_value_var, state=DISABLED)
    k_value_input.grid(column=1, row=3)
    # Adding possibility to overwrite k-value:
    k_value = Entry(my_tab2, width=8, justify=CENTER)
    k_value.grid(column=2, row=3)
    # Display of allowable gas velocity, actual gas rate, minimal vessel diameter, required demister area and
    # demister diameter
    velocity_parameters = {'Allowable gas velocity': 'm/s', 'Actual gas rate': 'm^3/s',
                           'Minimal vessel diameter': 'm', 'Required demister area': 'm^2',
                           'Demister diameter': 'm', 'Cross area': 'm^2', 'Actual gas velocity': 'm/s'}
    velocity_items_storage = {}
    velocity_entries = {}
    # Setting variables and making variable list:
    allowable_gas_velocity = StringVar()
    actual_gas_rate = StringVar()
    minimal_vessel_diameter = StringVar()
    required_demister_area = StringVar()
    demister_dimensions = StringVar()
    cross_area = StringVar()
    actual_gas_velocity = StringVar()
    variable_list = [allowable_gas_velocity, actual_gas_rate, minimal_vessel_diameter, required_demister_area,
                     demister_dimensions, cross_area, actual_gas_velocity]
    for i, (key, value) in enumerate(velocity_parameters.items()):
        velocity_items_storage[k] = Label(my_tab2, text=key, padx=10, pady=2)
        velocity_items_storage[k].grid(column=0, row=i + 4, sticky=W)
        velocity_items_storage[v] = Label(my_tab2, text=value)
        velocity_items_storage[v].grid(column=3, row=i + 4)
    for i in range(7):
        velocity_entries[i] = Entry(my_tab2, width=8, textvariable=variable_list[i], justify=CENTER, state=DISABLED)
        velocity_entries[i].grid(column=1, row=i + 4)

    # Calculation of height for various zones:
    # Adding label for height zones:
    height_zones_label = Label(my_tab2, text='Zones and inventory:',
                                        pady=5, font=('Helvetica 10 bold'), padx=10)
    height_zones_label.grid(sticky=W, columnspan=2, column=4, row=1)
    # Creating main labels:
    label_names_for_zones = {'Bottom zone liquid 2': 2, 'Liquid 2 zone': 5, 'Bottom zone liquid 1': 12,
                             'Liquid 1 zone': 15, 'Vapor zone': 22, 'Demister': 25, 'Tangent to tangent': 28}
    for key, value in label_names_for_zones.items():
        Label(my_tab2, text=key, font=('Helvetica 8 bold'), padx=10, pady=5).grid(column=4, sticky=W, row=value)
    # filling bottom zone for liquid 2 - for now program is only for 2phase separator so no functions here
    label_for_bottom = Label(my_tab2, text='Bottom to LSAL', padx=10).grid(column=4, sticky=W, row=3)
    labe_for_bottom_uom = Label(my_tab2, text='m', justify=CENTER).grid(column=7, row=3)
    label_for_bottom_vol = Label(my_tab2, text='Bottom inventory', padx=10).grid(column=4, sticky=W, row=4)
    labe_for_bottom_vol_uom = Label(my_tab2, text='m^3', justify=CENTER).grid(column=7, row=4)

    # Filling liquid 2 zone - for now program is only for 2 phase separator, so no functions here
    liquid2_zones_labels_and_uom = {'LSAL to LAL height': 'm', 'LSAL to LAL inventory': 'm^3',
                                    'LAL to LAH height': 'm', 'LAL to LAH inventory': 'm^3',
                                    'LAH to LSAH height': 'm', 'LAH to LSAH inventory': 'm^3'}
    for i, (k, v) in enumerate(liquid2_zones_labels_and_uom.items()):
        Label(my_tab2, text=k, padx=10).grid(column=4, sticky=W, row=6 + i)
        Label(my_tab2, text=v, padx=10).grid(column=7, sticky=W, row=6 + i)

    # filling bottom zone for liquid 1
    bottom_to_LSAL = StringVar()
    label_for_bottom = Label(my_tab2, text='Bottom to LSAL', padx=10).grid(column=4, sticky=W, row=13)
    labe_for_bottom_uom = Label(my_tab2, text='m', justify=CENTER).grid(column=7, row=13)
    bottom_entry = Entry(my_tab2, textvariable=bottom_to_LSAL, justify=CENTER, width=8, state=DISABLED)
    bottom_entry.grid(column=5, sticky=W, row=13)
    bottom_entry_rewrite = Entry(my_tab2, justify=CENTER, width=8)
    bottom_entry_rewrite.grid(column=6, sticky=W, row=13)
    bottom_vol = StringVar()
    label_for_bottom_vol = Label(my_tab2, text='Bottom inventory', padx=10).grid(column=4, sticky=W, row=14)
    labe_for_bottom_vol_uom = Label(my_tab2, text='m^3', justify=CENTER).grid(column=7, row=14)
    bottom_vol_entry = Entry(my_tab2, textvariable=bottom_vol, justify=CENTER, width=8, state=DISABLED)
    bottom_vol_entry.grid(column=5, sticky=W, row=14)

    # Filling liquid 1 zone
    liquid1_zones_labels_and_uom = {'LSAL to LAL height': 'm', 'LSAL to LAL inventory': 'm^3',
                                    'LAL to LAH height': 'm', 'LAL to LAH inventory': 'm^3',
                                    'LAH to LSAH height': 'm', 'LAH to LSAH inventory': 'm^3'}
    entry_list_for_liq1 = {}
    # Creating variables:
    lsalToLalHeight = StringVar()
    lsalToLalHeightRewrite = StringVar()
    lsalToLalInv = StringVar()
    lalToLahHeight = StringVar()
    lalToLahHeightRewrite = StringVar()
    lalToLahInv = StringVar()
    lahToLsahHeight = StringVar()
    lahToLsahHeightRewrite = StringVar()
    lahToLsahInv = StringVar()
    lsalToLalInvRecalc = StringVar()
    lalToLahInvRecalc = StringVar()
    lahToLsahInvRecalc = StringVar()

    list_of_variables_for_liq1 = [lsalToLalHeight, lsalToLalInv, lalToLahHeight,
                                  lalToLahInv, lahToLsahHeight, lahToLsahInv,
                                  lsalToLalHeightRewrite, lsalToLalInvRecalc, lalToLahHeightRewrite,
                                  lalToLahInvRecalc, lahToLsahHeightRewrite, lahToLsahInvRecalc]
    for i, (k, v) in enumerate(liquid1_zones_labels_and_uom.items()):
        Label(my_tab2, text=k, padx=10).grid(column=4, sticky=W, row=16 + i)
        Label(my_tab2, text=v, padx=10).grid(column=7, sticky=W, row=16 + i)
    for i in range(12):
        entry_list_for_liq1[i] = Entry(my_tab2, textvariable=list_of_variables_for_liq1[i], justify=CENTER, width=8)
        if i < 6:
            entry_list_for_liq1[i].configure(state=DISABLED)
            entry_list_for_liq1[i].grid(column=5, row=16 + i)
        else:
            entry_list_for_liq1[i].grid(column=6, row=16 + i - 6)
        if i != 6 and i != 8 and i != 10:
            entry_list_for_liq1[i].configure(state=DISABLED)

    # Filling vapor zone:
    vapor_zones_labels_and_uom = {'LSAH to inlet': 'm', 'inlet to demister': 'm'}
    for i, (k, v) in enumerate(vapor_zones_labels_and_uom.items()):
        Label(my_tab2, text=k, padx=10).grid(column=4, sticky=W, row=23 + i)
        Label(my_tab2, text=v, padx=10).grid(column=7, sticky=W, row=23 + i)
    lsahToInlet = StringVar()
    inletToDemister = StringVar()
    lsahToInletEntry = Entry(my_tab2, textvariable=lsahToInlet, justify=CENTER, width=8, state=DISABLED)
    inletToDemisterEntry = Entry(my_tab2, textvariable=inletToDemister, justify=CENTER, width=8, state=DISABLED)
    lsahToInletEntryRewrite = Entry(my_tab2, justify=CENTER, width=8)
    inletToDemisterEntryRewrite = Entry(my_tab2, justify=CENTER, width=8)
    lsahToInletEntry.grid(column=5, row=23)
    inletToDemisterEntry.grid(column=5, row=24)
    lsahToInletEntryRewrite.grid(column=6, row=23)
    inletToDemisterEntryRewrite.grid(column=6, row=24)

    # Filling demister:
    demister_zones_labels_and_uom = {'Demister thickness': 'm', 'Demister to head': 'm'}
    for i, (k, v) in enumerate(demister_zones_labels_and_uom.items()):
        Label(my_tab2, text=k, padx=10).grid(column=4, sticky=W, row=26 + i)
        Label(my_tab2, text=v, padx=10).grid(column=7, sticky=W, row=26 + i)
    demisterHeight = StringVar()
    demisterToTangent = StringVar()
    demisterHeightEntry = Entry(my_tab2, textvariable=demisterHeight, justify=CENTER, width=8, state=DISABLED)
    demisterToTangentEntry = Entry(my_tab2, textvariable=demisterToTangent, justify=CENTER, width=8, state=DISABLED)
    demisterHeightRewrite = Entry(my_tab2, justify=CENTER, width=8)
    demisterToTangentRewrite = Entry(my_tab2, justify=CENTER, width=8)
    demisterHeightEntry.grid(column=5, row=26)
    demisterToTangentEntry.grid(column=5, row=27)
    demisterHeightRewrite.grid(column=6, row=26)
    demisterToTangentRewrite.grid(column=6, row=27)

    # Filling tangent to tangent length:
    tan_to_tan = StringVar()
    tan_to_tan_entry = Entry(my_tab2, width=8, justify=CENTER, state=DISABLED, textvariable=tan_to_tan)
    tan_to_tan_entry.grid(column=5, row=28)
    tan_to_tan_rewrite = Entry(my_tab2, width=8, justify=CENTER)
    tan_to_tan_rewrite.grid(column=6, row=28)
    tan_to_tan_uom = Label(my_tab2, text='m').grid(column=7, row=28, sticky=W, padx=10)

    # Nozzle data
    # Creating nominal_diameter_vocabulary to be able to find inner diameter of different pipes:
    nd_voc = {'1.5': {'5S': '0.045', '10S': '0.0427', 'std': '0.0409', '40': '0.0409',
                      'XS': '0.0381', '80': '0.0381', '160': '0.034', 'XXS': '0.028'},
              '2': {'5S': '0.057', '10S': '0.0548', 'std': '0.0525', '40': '0.0525',
                    'XS': '0.0493', '80': '0.0493', '160': '0.0428', 'XXS': '0.038'},
              '3': {'5S': '0.0847', '10S': '0.0828', 'std': '0.0779', '40': '0.0779',
                    'XS': '0.0737', '80': '0.0737', '160': '0.0666', 'XXS': '0.058'},
              '4': {'5S': '0.11', '10S': '0.108', 'std': '0.102', '40': '0.102',
                    'XS': '0.0972', '80': '0.0972', '120': '0.092', '160': '0.0873', 'XXS': '0.08'},
              '6': {'5S': '0.163', '10S': '0.161', 'std': '0.154', '40': '0.154',
                    'XS': '0.146', '80': '0.146', '120': '0.14', '160': '0.132', 'XXS': '0.124'},
              '8': {'5S': '0.214', '10S': '0.212', '20': '0.206', '30': '0.205', 'std': '0.203',
                    '40': '0.203', '60': '0.198', 'XS': '0.194', '80': '0.194', '100': '0.189',
                    '120': '0.183', '140': '0.178', '160': '0.173', 'XXS': '0.175'},
              '10': {'5S': '0.266', '10S': '0.265', '20': '0.26', '30': '0.257', 'std': '0.255',
                     '40': '0.255', '60': '0.248', 'XS': '0.248', '80': '0.243', '100': '0.237',
                     '120': '0.23', '140': '0.222', '160': '0.216', 'XXS': '0.222'},
              '12': {'5S': '0.316', '10S': '0.315', '20': '0.311', '30': '0.307', 'std': '0.305',
                     '40': '0.303', '60': '0.295', 'XS': '0.298', '80': '0.289', '100': '0.281',
                     '120': '0.273', '140': '0.267', '160': '0.257', 'XXS': '0.237'},
              '14': {'5S': '0.348', '10S': '0.346', '10': '0.343', '20': '0.34', '30': '0.337',
                     'std': '0.337', '40': '0.333', '60': '0.325', 'XS': '0.33', '80': '0.318',
                     '100': '0.308', '120': '0.3', '140': '0.292', '160': '0.284'},
              '16': {'5S': '0.398', '10S': '0.398', '10': '0.394', '20': '0.391', '30': '0.387',
                     'std': '0.387', '40': '0.381', '60': '0.373', 'XS': '0.381', '80': '0.364',
                     '100': '0.354', '120': '0.344', '140': '0.333', '160': '0.325'},
              '18': {'5S': '0.449', '10S': '0.448', '10': '0.445', '20': '0.441', '30': '0.435',
                     'std': '0.438', '40': '0.429', '60': '0.419', 'XS': '0.432', '80': '0.41',
                     '100': '0.398', '120': '0.387', '140': '0.378', '160': '0.367'},
              '20': {'5S': '0.498', '10S': '0.497', '10': '0.495', '20': '0.489', '30': '0.483',
                     'std': '0.489', '40': '0.478', '60': '0.467', 'XS': '0.483', '80': '0.456',
                     '100': '0.443', '120': '0.432', '140': '0.419', '160': '0.408'},
              '24': {'5S': '0.599', '10S': '0.597', '10': '0.597', '20': '0.591', '30': '0.581',
                     'std': '0.581', '40': '0.575', '60': '0.56', 'XS': '0.584', '80': '0.548',
                     '100': '0.532', '120': '0.518', '140': '0.505', '160': '0.491'},
              '26': {'10': '0.645', '20': '0.635', 'std': '0.641', 'XS': '0.635'},
              '28': {'10': '0.695', '20': '0.686', '30': '0.679', 'std': '0.692', 'XS': '0.686'},
              '30': {'5S': '0.749', '10S': '0.746', '10': '0.746', '20': '0.737', '30': '0.73',
                     'std': '0.743', 'XS': '0.737'},
              '32': {'10': '0.797', '20': '0.784', '30': '0.781', 'std': '0.794', '40': '0.778',
                     'XS': '0.787'},
              '34': {'10': '0.848', '20': '0.838', '30': '0.832', 'std': '0.845', '40': '0.829',
                     'XS': '0.838'},
              '36': {'10': '0.899', '20': '0.889', '30': '0.883', 'std': '0.895', '40': '0.876',
                     'XS': '0.889'},
              '42': {'std': '1.048', 'XS': '1.041'}}
    # Creating list of nominal diameters and list of schedules for pipes:
    dn_list = ['1.5', '2', '3', '4', '6', '8', '10', '12', '14', '16', '18', '20', '24','26', '28', '30',
               '32', '34', '36', '42']
    sch_list = ['5S', '10S', '10', '20', '30', 'std', '40', '60', 'XS', '80', '100', '120', '140', '160', 'XS']
    dn_menus = {}
    sch_menus = {}
    # Creating variables and list of variables for drop down menus:
    inletDN = StringVar()
    vaporOutletDN = StringVar()
    liquid1OutletDN = StringVar()
    liquid2OutletDN = StringVar()
    dn_var_list = [inletDN, vaporOutletDN, liquid1OutletDN, liquid2OutletDN]
    inletSch = StringVar()
    vaporOutletSch = StringVar()
    liquid1OutletSch = StringVar()
    liquid2OutletSch = StringVar()
    sch_var_list = [inletSch, vaporOutletSch, liquid1OutletSch, liquid2OutletSch]

    # Creating a header for nozzle data:
    Label(my_tab2, text='Nozzle data:', pady=5, font=('Helvetica 10 bold'), padx=10)\
        .grid(sticky=W, columnspan=2, column=8, row=1)
    # Crating labels for inlet, vapor outlet, liquid 1 outlet and liquid 2 outlet:
    nozzle_list = ['Inlet', 'Vapor outlet', 'Liquid 1 outlet', 'Liquid 2 outlet']
    for i, nozzle in enumerate(nozzle_list):
        Label(my_tab2, text=nozzle, padx=10).grid(sticky=W, column=8, row=3 + i)
        dn_menus[i] = OptionMenu(my_tab2, dn_var_list[i], *dn_list)
        dn_menus[i].grid(column=9, row=3 + i)
        sch_menus[i] = OptionMenu(my_tab2, sch_var_list[i], *sch_list)
        sch_menus[i].grid(column=10, row=3 + i)

    # Adding rows for calculation:
    rows_list = ['DN, in', 'Sch', 'ID, m', 'V, m/s', 'Rho*V^2']
    for i, row in enumerate(rows_list):
        Label(my_tab2, text=row, pady=5, padx=10).grid(sticky=W, column=9 + i, row=2)
    # Creating variable lists and empty vocabularies for internal diameter, speed and inlet nozzle momentum entries:
    internalDiameterEntries, speedEntries, rhoVsqrEntries = {}, {}, {}
    internalDiameterVarList = [StringVar(), StringVar(), StringVar(), StringVar()]
    speedVarList = [StringVar(), StringVar(), StringVar(), StringVar()]
    rhoVsqrVarList = [StringVar(), StringVar(), StringVar(), StringVar()]
    # Filling interface with entries for internal diameters, speed and inlet nozzle momentums:
    for i, nozzle in enumerate(nozzle_list):
        internalDiameterEntries[i] = Entry(my_tab2, width=8, textvariable=internalDiameterVarList[i],
                                           justify=CENTER, state=DISABLED)
        internalDiameterEntries[i].grid(column=11, row=3 + i)
        speedEntries[i] = Entry(my_tab2, width=8, textvariable=speedVarList[i],
                                justify=CENTER, state=DISABLED)
        speedEntries[i].grid(column=12, row=3 + i)
        rhoVsqrEntries[i] = Entry(my_tab2, width=8, textvariable=rhoVsqrVarList[i],
                                  justify=CENTER, state=DISABLED)
        rhoVsqrEntries[i].grid(column=13, row=3 + i)

    # Estimation of wall thickness and vessel weight
    metal_stress = {'CS': {'-20': '17.1', '300': '17.1', '400': '17.1', '500': '17.1', '600': '16.4', '650': '15.8',
                           '700': '15.3', '750': '13', '800': '10.8', '850': '8.7', '900': '5.9', '950': '4',
                           '1000': '2.5', '1050': '0.1'},
                    'KCS': {'-20': '20', '300': '20', '400': '20', '500': '20', '600': '19.4', '650': '18.8',
                                  '700': '18.1', '750': '14.8', '800': '12', '850': '9.3', '900': '6.7', '950': '4',
                                  '1000': '2.5', '1050': '0'},
                    '0.5Mo': {'-20': '21.4', '300': '21.4', '400': '21.4', '500': '21.4', '600': '21.4', '650': '21.4',
                              '700': '21.4', '750': '21.4', '800': '21.4', '850': '20', '900': '13.7', '950': '8.2',
                              '1000': '4.8', '1050': '0'},
                    '1.25Cr-0.5Mo': {'-20': '21.4', '300': '21.4', '400': '21.4', '500': '21.4', '600': '21.4',
                                     '650': '21.4', '700': '21.4', '750': '21.4', '800': '21.4', '850': '20.2',
                                     '900': '13.7', '950': '9.3','1000': '6.3', '1050': '4.2'},
                    '2.25Cr-1Mo': {'-20': '21.4', '300': '20.9', '400': '20.6', '500': '20.5', '600': '20.4',
                                   '650': '20.2', '700': '20', '750': '19.7', '800': '19.3', '850': '18.7',
                                   '900': '15.8', '950': '11.4', '1000': '7.8', '1050': '5.1'},
                    '5Cr-0.5Mo': {'-20': '21.4', '300': '20.8', '400': '20.6', '500': '20.5', '600': '20.2',
                                  '650': '19.9', '700': '19.5', '750': '18.9', '800': '18.2', '850': '14.3',
                                  '900': '10.9', '950': '8','1000': '5.8', '1050': '4.2'},
                    'SS316': {'-20': '20', '300': '15.6', '400': '14.3', '500': '13.3', '600': '12.6', '650': '12.3',
                              '700': '12.1', '750': '11.9', '800': '11.8', '850': '11.6', '900': '11.5', '950': '11.4',
                              '1000': '11.3', '1050': '11.2'},
                    'SS321': {'-20': '20', '300': '16.5', '400': '15.3', '500': '14.3', '600': '13.5', '650': '13.2',
                              '700': '13', '750': '12.7', '800': '12.6', '850': '12.4', '900': '12.3', '950': '12.1',
                              '1000': '12', '1050': '9.6'},
                    'SS347': {'-20': '20', '300': '17.1', '400': '16', '500': '15', '600': '14.3', '650': '14',
                              '700': '13.8', '750': '13.7', '800': '13.6', '850': '13.5', '900': '13.4', '950': '13.4',
                              '1000': '13.4', '1050': '12.1'}}
    metal_density = {'CS': '7840', 'KCS': '7840', '0.5Mo': '7840', '1.25Cr-0.5Mo': '7840', '2.25Cr-1Mo': '7800',
                     '5Cr-0.5Mo': '7750', 'SS316': '7990', 'SS321': '9010', 'SS347': '8000'}
    # Create header:
    Label(my_tab2, text='Wall thickness and vessel weight:', font=('Helvetica 10 bold'), padx=10) \
        .grid(sticky=W, columnspan=4, column=8, row=7)
    # Create variables and uom for them:
    mech_uom_voc = {'Design pressure': 'kg/cm^2', 'Design temperature': '°C', 'Corrosion allow.': 'mm',
                    'Joint eff.': '', 'Shell MOC': '', 'Allow. stress': '1000psi', 'Design stress': 'kg/cm^2',
                    'Mat. density': 'kg/m^3'}
    mech_entries = {}
    for i, (k, v) in enumerate(mech_uom_voc.items()):
        Label(my_tab2, text=k, padx=10).grid(sticky=W, column=8, row=8 + i, columnspan=2)
        Label(my_tab2, text=v, padx=10).grid(sticky=W, column=11, row=8 + i)
        if i < 4:
            mech_entries[i] = Entry(my_tab2, justify=CENTER, width=8)
            mech_entries[i].grid(column=10, row=8 + i)
    material_var = StringVar()
    material_menu = OptionMenu(my_tab2, material_var, *metal_stress.keys())
    material_menu.grid(column=10, row=12)
    material_menu.config(width=1)
    # Add entry for allowable stress
    allowable_stress = StringVar()
    allowable_stress_entry = Entry(my_tab2, justify=CENTER, width=8, textvariable=allowable_stress, state=DISABLED)
    allowable_stress_entry.grid(column=10, row=13)
    # Entry for design stress
    design_stress = StringVar()
    design_stress_entry = Entry(my_tab2, justify=CENTER, width=8, textvariable=design_stress, state=DISABLED)
    design_stress_entry.grid(column=10, row=14)
    # Entry for material density
    material_density = StringVar()
    material_density_entry = Entry(my_tab2, justify=CENTER, width=8, state=DISABLED, textvariable=material_density)
    material_density_entry.grid(column=10, row=15)

    # Adding frames for weight estimation:
    vessel_parts_list = ['Shell', 'Head']
    weight_parameters = {'Thickness': 'mm', 'Surface area': 'm^2', 'Weight': 'kg', 'Total': 'kg'}
    head_parameters_entries = {}
    shell_parameters_entries = {}
    # Creating labels for weight parameters:
    for i, (k, v) in enumerate(weight_parameters.items()):
        Label(my_tab2, text=k, padx=10).grid(column=8, row=18 + i, columnspan=2, sticky=W)
        Label(my_tab2, text=v, padx=10).grid(column=11, row=18 + i, columnspan=2, sticky=W)
    # Creating labels for vessel parts:
    for i in range(2):
        Label(my_tab2, text=vessel_parts_list[i], padx=10).grid(column=9 + i, row=17)
    # Creating variables:
    head_var_list = [StringVar(), StringVar(), StringVar(), StringVar()]
    shell_var_list = [StringVar(), StringVar(), StringVar()]
    # Creating entries
    for i in range(3):
        shell_parameters_entries[i] = Entry(my_tab2, justify=CENTER, width=8, textvariable=shell_var_list[i],
                                            state=DISABLED)
        shell_parameters_entries[i].grid(column=9, row=18+i)
    for i in range(4):
        head_parameters_entries[i] = Entry(my_tab2, justify=CENTER, width=8, textvariable=head_var_list[i],
                                           state=DISABLED)
        head_parameters_entries[i].grid(column=10, row=18+i)

    # Filling the result tab:
    Label(my_tab3, text='Results:', pady=5, font=('Helvetica 10 bold'), padx=10) \
        .grid(sticky=W, columnspan=2, column=0, row=0)
    # Creating labels for results and uoms
    result_voc = {'Vessel diameter': 'm', 'Height T-T': 'm', 'L/D ratio': '', 'Separation': '',
                  'Vessel volume': 'm^3', 'Estimated weight': 'kg'}
    for i, (k, v) in enumerate(result_voc.items()):
        Label(my_tab3, text=k, padx=10).grid(column=0, row=1 + i, sticky=W)
        Label(my_tab3, text=v, padx=10).grid(column=2, row=1 + i)
    # Creating entries and variables:
    result_vars = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
    result_entries = {}
    for i in range(len(result_voc)):
        result_entries[i] = Entry(my_tab3, width=8, textvariable=result_vars[i], justify=CENTER)
        result_entries[i].grid(column=1, row=1+i)
    # Adding output button:
    output_button = Button(my_tab3, text='Output', width=10, command=lambda: output_button_action
        (my_tab3, data_input_boxes[6].get(), data_input_boxes[7].get(), data_input_boxes[2].get(),
         data_input_boxes[5].get(), data_input_boxes[3].get(), data_input_boxes[0].get(),
         data_input_boxes[1].get(), mech_entries[1].get(), mech_entries[0].get(),
         result_entries[0].get(), result_entries[1].get(), mech_entries[2].get(),
         insulation_type.get(), material_var.get(), demister.get()))
    output_button.grid(column=1)




    # Adding status box
    status_box = Label(root, text='', bd=1, relief=SUNKEN, anchor=W)
    status_box.grid(sticky=W + E)
    # Running update function to check and update all calculated values every 1 sec
    update()
    # starting main loop
    root.mainloop()


if __name__ == '__main__':
    main()

import os, sys, subprocess
from schematic_builder import SchematicBuilder

def build():
    sch = SchematicBuilder(title="AIRMODA SoC8767 Mixed-Signal Test & Characterization PCB")

    # 1. Register all symbols from KiCad libraries and local project library
    symbols_to_register = [
        ("local:hardware_test_pcb/SoC8767.kicad_sym", "SoC8767", "SoC8767:SoC8767"),
        ("local:hardware_test_pcb/SoC8767.kicad_sym", "OPA320", "SoC8767:OPA320"),
        ("local:hardware_test_pcb/SoC8767.kicad_sym", "BSS138", "SoC8767:BSS138"),
        ("Device", "R", "Device:R"),
        ("Device", "C", "Device:C"),
        ("Device", "LED", "Device:LED"),
        ("Connector_Generic", "Conn_01x02", "Connector_Generic:Conn_01x02"),
        ("Connector_Generic", "Conn_01x03", "Connector_Generic:Conn_01x03"),
        ("Connector_Generic", "Conn_01x04", "Connector_Generic:Conn_01x04"),
        ("Connector_Generic", "Conn_02x06_Odd_Even", "Connector_Generic:Conn_02x06_Odd_Even"),
        ("Connector", "Conn_Coaxial", "Connector:Conn_Coaxial"),
        ("Connector", "TestPoint", "Connector:TestPoint"),
        ("power", "GND", "power:GND"),
        ("power", "+3V3", "power:+3V3"),
        ("power", "+1V2", "power:+1V2"),
        ("power", "PWR_FLAG", "power:PWR_FLAG"),
        ("Logic_LevelTranslator", "TXU0304PW", "Logic_LevelTranslator:TXU0304PW"),
        ("Regulator_Linear", "TPS7A0512PDBV", "Regulator_Linear:TPS7A0512PDBV"),
        ("Sensor_Temperature", "TMP117xxDRV", "Sensor_Temperature:TMP117xxDRV"),
        ("Oscillator", "XO91", "Oscillator:XO91"),
    ]

    for lib_file, sym_name, new_lib_id in symbols_to_register:
        sch.register_symbol(lib_file, sym_name, new_lib_id)

    # --------------------------------------------------------------------------
    # Block 1: Target IC (U1 - SoC8767) at center (203.2, 152.4)
    # --------------------------------------------------------------------------
    u1_x, u1_y = 203.2, 152.4
    sch.add_instance(
        "U1", "SoC8767:SoC8767", "SoC8767", u1_x, u1_y, 0,
        "SoC8767:SoC8767_QFN24", "Combustible Gas Monitoring Mixed-Signal SoC"
    )

    # Corner Pins -> NC
    for p in [1, 6, 7, 12, 13, 18, 19, 24]:
        sch.connect_pin_nc("U1", p)

    # Ground pins
    sch.connect_pin_to_power("U1", 3, "GND", "L", 5.08)
    sch.connect_pin_to_power("U1", 25, "GND", "D", 5.08)

    # Functional Pins
    sch.connect_pin("U1", 2, "BGR_1V0", "L", 5.08)
    sch.connect_pin("U1", 4, "IN_SENS_SOC", "L", 5.08)
    sch.connect_pin("U1", 5, "ALARM_1V2", "L", 5.08)

    sch.connect_pin("U1", 8, "RESET_SOC", "D", 5.08)
    sch.connect_pin("U1", 9, "VDD_1V2_DIG", "D", 5.08)
    sch.connect_pin("U1", 10, "AD0_SOC", "D", 5.08)
    sch.connect_pin("U1", 11, "ENABLE_SOC", "D", 5.08)

    sch.connect_pin("U1", 14, "I_SDA_SOC", "R", 5.08)
    sch.connect_pin("U1", 15, "I_SCL_SOC", "R", 5.08)
    sch.connect_pin("U1", 16, "O_SDA_SOC", "R", 5.08)
    sch.connect_pin("U1", 17, "O_SCL_SOC", "R", 5.08)

    sch.connect_pin("U1", 20, "CLK_D_SOC", "U", 5.08)
    sch.connect_pin("U1", 21, "CLK_A_SOC", "U", 5.08)
    sch.connect_pin("U1", 22, "VDD_1V2_ANA", "U", 5.08)
    sch.connect_pin("U1", 23, "VDD_3V3_SOC", "U", 5.08)

    # --------------------------------------------------------------------------
    # Block 2: Decoupling Capacitors for SoC8767
    # --------------------------------------------------------------------------
    # Local caps on Pin 2 (BGR_1V0)
    sch.add_instance("C_BGR1", "Device:C", "100nF", 142.24, 137.16, 0, "Capacitor_SMD:C_0402_1005Metric", "BGR Local Decoupling")
    sch.connect_pin("C_BGR1", 1, "BGR_1V0", "U", 2.54)
    sch.connect_pin_to_power("C_BGR1", 2, "GND", "D", 2.54)

    sch.add_instance("C_BGR2", "Device:C", "1uF", 152.4, 137.16, 0, "Capacitor_SMD:C_0603_1608Metric", "BGR Bulk Decoupling")
    sch.connect_pin("C_BGR2", 1, "BGR_1V0", "U", 2.54)
    sch.connect_pin_to_power("C_BGR2", 2, "GND", "D", 2.54)

    # Local caps on Pin 9 (VDD_1V2_DIG)
    sch.add_instance("C_DIG1", "Device:C", "100nF", 182.88, 203.2, 0, "Capacitor_SMD:C_0402_1005Metric", "VDD_DIG Local Decoupling")
    sch.connect_pin("C_DIG1", 1, "VDD_1V2_DIG", "U", 2.54)
    sch.connect_pin_to_power("C_DIG1", 2, "GND", "D", 2.54)

    sch.add_instance("C_DIG2", "Device:C", "1uF", 193.04, 203.2, 0, "Capacitor_SMD:C_0603_1608Metric", "VDD_DIG Bulk Decoupling")
    sch.connect_pin("C_DIG2", 1, "VDD_1V2_DIG", "U", 2.54)
    sch.connect_pin_to_power("C_DIG2", 2, "GND", "D", 2.54)

    # Local caps on Pin 22 (VDD_1V2_ANA)
    sch.add_instance("C_ANA1", "Device:C", "100nF", 182.88, 101.6, 0, "Capacitor_SMD:C_0402_1005Metric", "VDD_ANA Local Decoupling")
    sch.connect_pin("C_ANA1", 1, "VDD_1V2_ANA", "U", 2.54)
    sch.connect_pin_to_power("C_ANA1", 2, "GND", "D", 2.54)

    sch.add_instance("C_ANA2", "Device:C", "1uF", 193.04, 101.6, 0, "Capacitor_SMD:C_0603_1608Metric", "VDD_ANA Bulk Decoupling")
    sch.connect_pin("C_ANA2", 1, "VDD_1V2_ANA", "U", 2.54)
    sch.connect_pin_to_power("C_ANA2", 2, "GND", "D", 2.54)

    # Local caps on Pin 23 (VDD_3V3_SOC)
    sch.add_instance("C_3V3_1", "Device:C", "100nF", 152.4, 101.6, 0, "Capacitor_SMD:C_0402_1005Metric", "VDD_3V3 Local Decoupling")
    sch.connect_pin("C_3V3_1", 1, "VDD_3V3_SOC", "U", 2.54)
    sch.connect_pin_to_power("C_3V3_1", 2, "GND", "D", 2.54)

    sch.add_instance("C_3V3_2", "Device:C", "1uF", 162.56, 101.6, 0, "Capacitor_SMD:C_0603_1608Metric", "VDD_3V3 Mid Decoupling")
    sch.connect_pin("C_3V3_2", 1, "VDD_3V3_SOC", "U", 2.54)
    sch.connect_pin_to_power("C_3V3_2", 2, "GND", "D", 2.54)

    sch.add_instance("C_3V3_BULK", "Device:C", "10uF", 172.72, 101.6, 0, "Capacitor_SMD:C_0805_2012Metric", "VDD_3V3 Bulk Decoupling")
    sch.connect_pin("C_3V3_BULK", 1, "VDD_3V3_SOC", "U", 2.54)
    sch.connect_pin_to_power("C_3V3_BULK", 2, "GND", "D", 2.54)

    # --------------------------------------------------------------------------
    # Block 3: Power Isolation & Current Sense (VDD_3V3, VDD_1V2_DIG, VDD_1V2_ANA)
    # --------------------------------------------------------------------------
    # VDD_3V3 Main Power Shunt & Jumper
    sch.add_instance("R_SENSE_MAIN", "Device:R", "1R_1%", 111.76, 88.9, 0, "Resistor_SMD:R_0805_2012Metric", "Main 3.3V Current Sense Shunt")
    sch.connect_pin_to_power("R_SENSE_MAIN", 1, "+3V3", "U", 2.54)
    sch.connect_pin("R_SENSE_MAIN", 2, "VDD_3V3_SOC", "D", 2.54)

    sch.add_instance("J_PWR_MAIN", "Connector_Generic:Conn_01x02", "J_PWR_MAIN", 127.0, 88.9, 0, "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", "Main Power Shorting / Profiling Jumper")
    sch.connect_pin_to_power("J_PWR_MAIN", 1, "+3V3", "U", 2.54)
    sch.connect_pin("J_PWR_MAIN", 2, "VDD_3V3_SOC", "D", 2.54)

    sch.add_instance("TP_PWR_IN", "Connector:TestPoint", "TP_PWR_3V3", 101.6, 83.82, 0, "TestPoint:TestPoint_Pad_D1.5mm", "3.3V In Test Point")
    sch.connect_pin_to_power("TP_PWR_IN", 1, "+3V3", "L", 2.54)

    sch.add_instance("TP_VDD_SOC", "Connector:TestPoint", "TP_VDD_3V3", 101.6, 96.52, 0, "TestPoint:TestPoint_Pad_D1.5mm", "VDD_3V3_SOC Test Point")
    sch.connect_pin("TP_VDD_SOC", 1, "VDD_3V3_SOC", "L", 2.54)

    # Power flag for VDD_3V3_SOC (driven through R_SENSE_MAIN from +3V3)
    sch.add_pwr_flag("VDD_3V3_SOC", 91.44, 96.52)

    # VDD_1V2_DIG LDO Isolation & Current Sense Shunt
    sch.add_instance("J_LDO_DIG", "Connector_Generic:Conn_01x03", "J_LDO_DIG", 147.32, 228.6, 0, "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", "Digital LDO Selector (1-2: Int, 2-3: Ext)")
    sch.connect_pin("J_LDO_DIG", 1, "VDD_1V2_DIG", "L", 2.54)
    sch.connect_pin("J_LDO_DIG", 2, "DIG_SENSE_MID", "L", 2.54)
    sch.connect_pin_to_power("J_LDO_DIG", 3, "+1V2", "L", 2.54)

    sch.add_instance("R_SENSE_DIG", "Device:R", "1R_1%", 162.56, 228.6, 0, "Resistor_SMD:R_0603_1608Metric", "Digital Core Current Sense Shunt")
    sch.connect_pin("R_SENSE_DIG", 1, "DIG_SENSE_MID", "U", 2.54)
    sch.connect_pin_to_power("R_SENSE_DIG", 2, "+1V2", "D", 2.54)

    sch.add_instance("TP_DIG_INT", "Connector:TestPoint", "TP_DIG_INT", 137.16, 226.06, 0, "TestPoint:TestPoint_Pad_D1.5mm", "Internal Digital LDO Test Point")
    sch.connect_pin("TP_DIG_INT", 1, "VDD_1V2_DIG", "L", 2.54)

    # VDD_1V2_ANA LDO Isolation & Current Sense Shunt
    sch.add_instance("J_LDO_ANA", "Connector_Generic:Conn_01x03", "J_LDO_ANA", 218.44, 76.2, 0, "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", "Analog LDO Selector (1-2: Int, 2-3: Ext)")
    sch.connect_pin("J_LDO_ANA", 1, "VDD_1V2_ANA", "L", 2.54)
    sch.connect_pin("J_LDO_ANA", 2, "ANA_SENSE_MID", "L", 2.54)
    sch.connect_pin_to_power("J_LDO_ANA", 3, "+1V2", "L", 2.54)

    sch.add_instance("R_SENSE_ANA", "Device:R", "1R_1%", 233.68, 76.2, 0, "Resistor_SMD:R_0603_1608Metric", "Analog Core Current Sense Shunt")
    sch.connect_pin("R_SENSE_ANA", 1, "ANA_SENSE_MID", "U", 2.54)
    sch.connect_pin_to_power("R_SENSE_ANA", 2, "+1V2", "D", 2.54)

    sch.add_instance("TP_ANA_INT", "Connector:TestPoint", "TP_ANA_INT", 208.28, 73.66, 0, "TestPoint:TestPoint_Pad_D1.5mm", "Internal Analog LDO Test Point")
    sch.connect_pin("TP_ANA_INT", 1, "VDD_1V2_ANA", "L", 2.54)

    # --------------------------------------------------------------------------
    # Block 4: External 1.2V Backup LDO (U_LDO - TPS7A0512PDBV)
    # --------------------------------------------------------------------------
    ldo_x, ldo_y = 66.04, 88.9
    sch.add_instance("U_LDO", "Regulator_Linear:TPS7A0512PDBV", "TPS7A0512", ldo_x, ldo_y, 0, "Package_TO_SOT_SMD:SOT-23-5", "External 1.2V 200mA Ultra-Low-Noise LDO")
    sch.connect_pin_to_power("U_LDO", 1, "+3V3", "L", 2.54)
    sch.connect_pin_to_power("U_LDO", 2, "GND", "D", 2.54)
    sch.connect_pin_to_power("U_LDO", 3, "+3V3", "L", 2.54)
    sch.connect_pin_nc("U_LDO", 4)
    sch.connect_pin_to_power("U_LDO", 5, "+1V2", "R", 2.54) # Pin 5 is Power Output, natively powers +1V2!

    sch.add_instance("C_LDO_IN", "Device:C", "1uF", 50.8, 88.9, 0, "Capacitor_SMD:C_0603_1608Metric", "LDO Input Capacitor")
    sch.connect_pin_to_power("C_LDO_IN", 1, "+3V3", "U", 2.54)
    sch.connect_pin_to_power("C_LDO_IN", 2, "GND", "D", 2.54)

    sch.add_instance("C_LDO_OUT", "Device:C", "2.2uF", 83.82, 88.9, 0, "Capacitor_SMD:C_0603_1608Metric", "LDO Output Capacitor")
    sch.connect_pin_to_power("C_LDO_OUT", 1, "+1V2", "U", 2.54)
    sch.connect_pin_to_power("C_LDO_OUT", 2, "GND", "D", 2.54)

    sch.add_instance("TP_1V2", "Connector:TestPoint", "TP_1V2", 83.82, 73.66, 0, "TestPoint:TestPoint_Pad_D1.5mm", "1.2V Rail Test Point")
    sch.connect_pin_to_power("TP_1V2", 1, "+1V2", "L", 2.54)

    # --------------------------------------------------------------------------
    # Block 5: BGR Isolation, External Overdrive & Active Buffer (OPA320)
    # --------------------------------------------------------------------------
    # J_BGR (2-pin header)
    sch.add_instance("J_BGR", "Connector_Generic:Conn_01x02", "J_BGR", 114.3, 137.16, 0, "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", "BGR Isolation & External Overdrive Jumper")
    sch.connect_pin("J_BGR", 1, "BGR_1V0", "L", 2.54)
    sch.connect_pin("J_BGR", 2, "BGR_EXT_IN", "L", 2.54)

    sch.add_instance("TP_BGR", "Connector:TestPoint", "TP_BGR", 101.6, 137.16, 0, "TestPoint:TestPoint_Pad_D1.5mm", "BGR Raw Test Point")
    sch.connect_pin("TP_BGR", 1, "BGR_1V0", "L", 2.54)

    sch.add_instance("TP_BGR_EXT", "Connector:TestPoint", "TP_BGR_EXT", 101.6, 144.78, 0, "TestPoint:TestPoint_Pad_D1.5mm", "BGR External SMU Overdrive Test Point")
    sch.connect_pin("TP_BGR_EXT", 1, "BGR_EXT_IN", "L", 2.54)

    # U_BUF1 (OPA320 Buffer for BGR)
    buf1_x, buf1_y = 66.04, 137.16
    sch.add_instance("U_BUF1", "SoC8767:OPA320", "OPA320", buf1_x, buf1_y, 0, "Package_TO_SOT_SMD:SOT-23-5", "BGR Precision CMOS Unity-Gain Buffer")
    sch.connect_pin("U_BUF1", 1, "BGR_BUF_OUT", "R", 2.54)
    sch.connect_pin_to_power("U_BUF1", 2, "GND", "D", 2.54)
    sch.connect_pin("U_BUF1", 3, "BGR_1V0", "L", 2.54)
    sch.connect_pin("U_BUF1", 4, "BGR_BUF_OUT", "L", 2.54)
    sch.connect_pin_to_power("U_BUF1", 5, "+3V3", "U", 2.54)

    sch.add_instance("C_BUF1", "Device:C", "100nF", 50.8, 127.0, 0, "Capacitor_SMD:C_0402_1005Metric", "Buffer 1 Decoupling")
    sch.connect_pin_to_power("C_BUF1", 1, "+3V3", "U", 2.54)
    sch.connect_pin_to_power("C_BUF1", 2, "GND", "D", 2.54)

    sch.add_instance("SMA_BGR", "Connector:Conn_Coaxial", "SMA_BGR", 88.9, 137.16, 0, "Connector_Coaxial:SMA_Amphenol_132134_Vertical", "Buffered BGR Output SMA")
    sch.connect_pin("SMA_BGR", 1, "BGR_BUF_OUT", "L", 2.54)
    sch.connect_pin_to_power("SMA_BGR", 2, "GND", "D", 2.54)

    sch.add_instance("TP_BGR_BUF", "Connector:TestPoint", "TP_BGR_BUF", 88.9, 127.0, 0, "TestPoint:TestPoint_Pad_D1.5mm", "Buffered BGR Test Point")
    sch.connect_pin("TP_BGR_BUF", 1, "BGR_BUF_OUT", "L", 2.54)

    # --------------------------------------------------------------------------
    # Block 6: Analog Clock (CLK_A, Pin 21) Active Op-Amp Buffer (OPA320)
    # --------------------------------------------------------------------------
    buf2_x, buf2_y = 269.24, 76.2
    sch.add_instance("U_BUF2", "SoC8767:OPA320", "OPA320", buf2_x, buf2_y, 0, "Package_TO_SOT_SMD:SOT-23-5", "CLK_A Precision CMOS Buffer")
    sch.connect_pin("U_BUF2", 1, "CLKA_BUF_OUT", "R", 2.54)
    sch.connect_pin_to_power("U_BUF2", 2, "GND", "D", 2.54)
    sch.connect_pin("U_BUF2", 3, "CLK_A_SOC", "L", 2.54)
    sch.connect_pin("U_BUF2", 4, "CLKA_BUF_OUT", "L", 2.54)
    sch.connect_pin_to_power("U_BUF2", 5, "+3V3", "U", 2.54)

    sch.add_instance("C_BUF2", "Device:C", "100nF", 254.0, 66.04, 0, "Capacitor_SMD:C_0402_1005Metric", "Buffer 2 Decoupling")
    sch.connect_pin_to_power("C_BUF2", 1, "+3V3", "U", 2.54)
    sch.connect_pin_to_power("C_BUF2", 2, "GND", "D", 2.54)

    sch.add_instance("SMA_CLK_A", "Connector:Conn_Coaxial", "SMA_CLK_A", 292.1, 76.2, 0, "Connector_Coaxial:SMA_Amphenol_132134_Vertical", "Buffered CLK_A SMA Output")
    sch.connect_pin("SMA_CLK_A", 1, "CLKA_BUF_OUT", "L", 2.54)
    sch.connect_pin_to_power("SMA_CLK_A", 2, "GND", "D", 2.54)

    sch.add_instance("TP_CLKA_BUF", "Connector:TestPoint", "TP_CLK_A", 292.1, 66.04, 0, "TestPoint:TestPoint_Pad_D1.5mm", "Buffered CLK_A Test Point")
    sch.connect_pin("TP_CLKA_BUF", 1, "CLKA_BUF_OUT", "L", 2.54)

    # --------------------------------------------------------------------------
    # Block 7: Digital Clock (CLK_D, Pin 20) 50 Ohm Network, Oscillator & Jumpers
    # --------------------------------------------------------------------------
    # External SMA Clock Input
    sch.add_instance("SMA_CLK_D", "Connector:Conn_Coaxial", "SMA_CLK_D", 35.56, 177.8, 0, "Connector_Coaxial:SMA_Amphenol_132134_Vertical", "External Clock Input SMA")
    sch.connect_pin("SMA_CLK_D", 1, "CLK_SMA_IN", "L", 2.54)
    sch.connect_pin_to_power("SMA_CLK_D", 2, "GND", "D", 2.54)

    # 50 Ohm Termination Network
    sch.add_instance("R_TERM_CLK", "Device:R", "49R9_1%", 50.8, 177.8, 0, "Resistor_SMD:R_0603_1608Metric", "50 Ohm Clock Termination")
    sch.connect_pin("R_TERM_CLK", 1, "CLK_SMA_IN", "U", 2.54)
    sch.connect_pin("R_TERM_CLK", 2, "CLK_TERM_JMP", "D", 2.54)

    sch.add_instance("J_TERM_CLK", "Connector_Generic:Conn_01x02", "J_TERM", 63.5, 177.8, 0, "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", "50 Ohm Termination Enable Jumper")
    sch.connect_pin("J_TERM_CLK", 1, "CLK_TERM_JMP", "L", 2.54)
    sch.connect_pin_to_power("J_TERM_CLK", 2, "GND", "D", 2.54)

    # Onboard 1.2V 8MHz CMOS Oscillator (U_OSC - XO91)
    osc_x, osc_y = 50.8, 208.28
    sch.add_instance("U_OSC", "Oscillator:XO91", "8MHz_1.2V", osc_x, osc_y, 0, "Oscillator:Oscillator_SMD_EuroQuartz_XO91-4Pin_7.0x5.0mm", "1.2V CMOS Clock Oscillator")
    sch.connect_pin_to_power("U_OSC", 1, "+1V2", "L", 2.54)
    sch.connect_pin_to_power("U_OSC", 2, "GND", "D", 2.54)
    sch.connect_pin("U_OSC", 3, "OSC_OUT_1V2", "R", 2.54)
    sch.connect_pin_to_power("U_OSC", 4, "+1V2", "U", 2.54)

    sch.add_instance("C_OSC", "Device:C", "100nF", 35.56, 208.28, 0, "Capacitor_SMD:C_0402_1005Metric", "Oscillator Decoupling")
    sch.connect_pin_to_power("C_OSC", 1, "+1V2", "U", 2.54)
    sch.connect_pin_to_power("C_OSC", 2, "GND", "D", 2.54)

    # Clock Source Selector Jumper (J_CLK_SRC - 4-pin: 1: SMA, 2: Clock Common Out, 3: Oscillator, 4: Host MCU via Level Shifter)
    sch.add_instance("J_CLK_SRC", "Connector_Generic:Conn_01x04", "J_CLK_SRC", 76.2, 198.12, 0, "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", "Clock Source Selector (1: SMA, 3: OSC, 4: MCU)")
    sch.connect_pin("J_CLK_SRC", 1, "CLK_SMA_IN", "L", 2.54)
    sch.connect_pin("J_CLK_SRC", 2, "CLK_D_SRC", "L", 2.54)
    sch.connect_pin("J_CLK_SRC", 3, "OSC_OUT_1V2", "L", 2.54)
    sch.connect_pin("J_CLK_SRC", 4, "CLK_D_LS_1V2", "L", 2.54)

    # Series Damping Resistor (27 Ohm)
    sch.add_instance("R_DAMP", "Device:R", "27R_1%", 96.52, 198.12, 0, "Resistor_SMD:R_0603_1608Metric", "Clock Series Damping Resistor")
    sch.connect_pin("R_DAMP", 1, "CLK_D_SRC", "U", 2.54)
    sch.connect_pin("R_DAMP", 2, "CLK_D_SRC_DAMPED", "D", 2.54)

    # J_CLK_D Isolation Jumper to SoC Pin 20
    sch.add_instance("J_CLK_D", "Connector_Generic:Conn_01x02", "J_CLK_D", 114.3, 198.12, 0, "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", "CLK_D Isolation Jumper")
    sch.connect_pin("J_CLK_D", 1, "CLK_D_SRC_DAMPED", "L", 2.54)
    sch.connect_pin("J_CLK_D", 2, "CLK_D_SOC", "L", 2.54)

    sch.add_instance("TP_CLK_D", "Connector:TestPoint", "TP_CLK_D", 114.3, 208.28, 0, "TestPoint:TestPoint_Pad_D1.5mm", "CLK_D Test Point")
    sch.connect_pin("TP_CLK_D", 1, "CLK_D_SOC", "L", 2.54)

    sch.add_instance("TP_CLK_LS", "Connector:TestPoint", "TP_CLK_LS", 76.2, 218.44, 0, "TestPoint:TestPoint_Pad_D1.5mm", "Host MCU Translated Clock Test Point")
    sch.connect_pin("TP_CLK_LS", 1, "CLK_D_LS_1V2", "L", 2.54)

    # --------------------------------------------------------------------------
    # Block 8: Sensor Conditioning, Calibration SMA & Anti-Aliasing Filter
    # --------------------------------------------------------------------------
    # Calibration SMA
    sch.add_instance("SMA_CAL", "Connector:Conn_Coaxial", "SMA_CAL", 35.56, 137.16, 0, "Connector_Coaxial:SMA_Amphenol_132134_Vertical", "Precision Calibration Input SMA")
    sch.connect_pin("SMA_CAL", 1, "SMA_CAL_RAW", "L", 2.54)
    sch.connect_pin_to_power("SMA_CAL", 2, "GND", "D", 2.54)

    # Anti-Aliasing RC Filter (Moved to X=58.42 to ensure ample clearance from C_BUF1)
    sch.add_instance("R_AAF", "Device:R", "100R_1%", 58.42, 137.16, 0, "Resistor_SMD:R_0603_1608Metric", "Anti-Aliasing Filter Resistor")
    sch.connect_pin("R_AAF", 1, "SMA_CAL_RAW", "U", 2.54)
    sch.connect_pin("R_AAF", 2, "SMA_CAL_FILT", "D", 2.54)

    sch.add_instance("C_AAF", "Device:C", "1nF", 71.12, 137.16, 0, "Capacitor_SMD:C_0603_1608Metric", "Anti-Aliasing Filter Capacitor")
    sch.connect_pin("C_AAF", 1, "SMA_CAL_FILT", "U", 2.54)
    sch.connect_pin_to_power("C_AAF", 2, "GND", "D", 2.54)

    # Gas Sensor Header (J_SENSOR - 4-pin header)
    sch.add_instance("J_SENSOR", "Connector_Generic:Conn_01x04", "J_SENSOR", 35.56, 101.6, 0, "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", "Real Gas Sensor Conditioning Header")
    sch.connect_pin_to_power("J_SENSOR", 1, "+3V3", "L", 2.54)
    sch.connect_pin("J_SENSOR", 2, "SENSOR_MOD_IN", "L", 2.54)
    sch.connect_pin("J_SENSOR", 3, "SENSOR_RL_TAP", "L", 2.54)
    sch.connect_pin_to_power("J_SENSOR", 4, "GND", "L", 2.54)

    # Sensor Load Resistor (Separated at X = 60.96 to avoid wire collisions)
    sch.add_instance("R_SENS_LOAD", "Device:R", "10k", 60.96, 101.6, 0, "Resistor_SMD:R_0603_1608Metric", "Sensor Load / Divider Resistor")
    sch.connect_pin("R_SENS_LOAD", 1, "SENSOR_RL_TAP", "U", 2.54)
    sch.connect_pin_to_power("R_SENS_LOAD", 2, "GND", "D", 2.54)

    # J_SENS_SRC Selector (1: SMA Cal, 2: IN_SENS_SOC, 3: Gas Sensor Header)
    sch.add_instance("J_SENS_SRC", "Connector_Generic:Conn_01x03", "J_SENS_SRC", 76.2, 114.3, 0, "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", "Sensor Input Selector (1: Cal, 3: Sensor)")
    sch.connect_pin("J_SENS_SRC", 1, "SMA_CAL_FILT", "L", 2.54)
    sch.connect_pin("J_SENS_SRC", 2, "IN_SENS_SOC", "L", 2.54)
    sch.connect_pin("J_SENS_SRC", 3, "SENSOR_MOD_IN", "L", 2.54)

    sch.add_instance("TP_IN_SENS", "Connector:TestPoint", "TP_IN_SENS", 91.44, 114.3, 0, "TestPoint:TestPoint_Pad_D1.5mm", "IN_SENS Test Point")
    sch.connect_pin("TP_IN_SENS", 1, "IN_SENS_SOC", "L", 2.54)

    # --------------------------------------------------------------------------
    # Block 9: Unidirectional Level Shifter (U_LS - TXU0304PW)
    # --------------------------------------------------------------------------
    ls_x, ls_y = 269.24, 152.4
    sch.add_instance("U_LS", "Logic_LevelTranslator:TXU0304PW", "TXU0304", ls_x, ls_y, 0, "Package_SO:TSSOP-14_4.4x5mm_P0.65mm", "4-Channel Dual-Supply Level Translator (3.3V <-> 1.2V)")
    sch.connect_pin_to_power("U_LS", 1, "+3V3", "U", 2.54)
    sch.connect_pin("U_LS", 2, "CLK_D_3V3", "L", 2.54)
    sch.connect_pin("U_LS", 3, "RESET_3V3", "L", 2.54)
    sch.connect_pin("U_LS", 4, "ENABLE_3V3", "L", 2.54)
    sch.connect_pin("U_LS", 5, "ALARM_3V3", "L", 2.54)
    sch.connect_pin_nc("U_LS", 6)
    sch.connect_pin_to_power("U_LS", 7, "GND", "D", 2.54)
    sch.connect_pin_to_power("U_LS", 8, "+3V3", "L", 2.54)
    sch.connect_pin_nc("U_LS", 9)
    sch.connect_pin("U_LS", 10, "ALARM_1V2", "R", 2.54)
    sch.connect_pin("U_LS", 11, "ENABLE_1V2", "R", 2.54)
    sch.connect_pin("U_LS", 12, "RESET_1V2", "R", 2.54)
    sch.connect_pin("U_LS", 13, "CLK_D_LS_1V2", "R", 2.54)
    sch.connect_pin_to_power("U_LS", 14, "+1V2", "U", 2.54)

    sch.add_instance("C_LS_A", "Device:C", "100nF", 254.0, 132.08, 0, "Capacitor_SMD:C_0402_1005Metric", "Level Shifter VCCA Decoupling")
    sch.connect_pin_to_power("C_LS_A", 1, "+3V3", "U", 2.54)
    sch.connect_pin_to_power("C_LS_A", 2, "GND", "D", 2.54)

    sch.add_instance("C_LS_B", "Device:C", "100nF", 284.48, 132.08, 0, "Capacitor_SMD:C_0402_1005Metric", "Level Shifter VCCB Decoupling")
    sch.connect_pin_to_power("C_LS_B", 1, "+1V2", "U", 2.54)
    sch.connect_pin_to_power("C_LS_B", 2, "GND", "D", 2.54)

    # Pull-up on RESET_3V3 & Pull-down on ENABLE_3V3
    sch.add_instance("R_PU_RST", "Device:R", "10k", 254.0, 147.32, 0, "Resistor_SMD:R_0603_1608Metric", "RESET Pull-Up")
    sch.connect_pin_to_power("R_PU_RST", 1, "+3V3", "U", 2.54)
    sch.connect_pin("R_PU_RST", 2, "RESET_3V3", "D", 2.54)

    sch.add_instance("R_PD_EN", "Device:R", "10k", 254.0, 162.56, 0, "Resistor_SMD:R_0603_1608Metric", "ENABLE Pull-Down")
    sch.connect_pin("R_PD_EN", 1, "ENABLE_3V3", "U", 2.54)
    sch.connect_pin_to_power("R_PD_EN", 2, "GND", "D", 2.54)

    # --------------------------------------------------------------------------
    # Block 10: Control & I2C Individual Isolation Jumpers
    # --------------------------------------------------------------------------
    # J_EN (2-pin header)
    sch.add_instance("J_EN", "Connector_Generic:Conn_01x02", "J_EN", 228.6, 218.44, 0, "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", "ENABLE Isolation Jumper")
    sch.connect_pin("J_EN", 1, "ENABLE_SOC", "L", 2.54)
    sch.connect_pin("J_EN", 2, "ENABLE_1V2", "L", 2.54)

    # J_RST (2-pin header)
    sch.add_instance("J_RST", "Connector_Generic:Conn_01x02", "J_RST", 213.36, 218.44, 0, "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", "RESET Isolation Jumper")
    sch.connect_pin("J_RST", 1, "RESET_SOC", "L", 2.54)
    sch.connect_pin("J_RST", 2, "RESET_1V2", "L", 2.54)

    # J_AD0 (3-pin header: 1: +1V2, 2: AD0_SOC, 3: GND)
    sch.add_instance("J_AD0", "Connector_Generic:Conn_01x03", "J_AD0", 198.12, 228.6, 0, "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", "I2C Address Select (1: 1.2V->0x49, 3: GND->0x48)")
    sch.connect_pin_to_power("J_AD0", 1, "+1V2", "L", 2.54)
    sch.connect_pin("J_AD0", 2, "AD0_SOC", "L", 2.54)
    sch.connect_pin_to_power("J_AD0", 3, "GND", "L", 2.54)

    # J_ISDA, J_OSDA, J_ISCL, J_OSCL (2-pin headers)
    sch.add_instance("J_ISDA", "Connector_Generic:Conn_01x02", "J_ISDA", 254.0, 187.96, 0, "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", "I_SDA Isolation Jumper")
    sch.connect_pin("J_ISDA", 1, "I_SDA_SOC", "L", 2.54)
    sch.connect_pin("J_ISDA", 2, "SDA_1V2", "L", 2.54)

    sch.add_instance("J_OSDA", "Connector_Generic:Conn_01x02", "J_OSDA", 269.24, 187.96, 0, "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", "O_SDA Isolation Jumper")
    sch.connect_pin("J_OSDA", 1, "O_SDA_SOC", "L", 2.54)
    sch.connect_pin("J_OSDA", 2, "SDA_1V2", "L", 2.54)

    sch.add_instance("J_ISCL", "Connector_Generic:Conn_01x02", "J_ISCL", 254.0, 203.2, 0, "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", "I_SCL Isolation Jumper")
    sch.connect_pin("J_ISCL", 1, "I_SCL_SOC", "L", 2.54)
    sch.connect_pin("J_ISCL", 2, "SCL_1V2", "L", 2.54)

    sch.add_instance("J_OSCL", "Connector_Generic:Conn_01x02", "J_OSCL", 269.24, 203.2, 0, "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", "O_SCL Isolation Jumper")
    sch.connect_pin("J_OSCL", 1, "O_SCL_SOC", "L", 2.54)
    sch.connect_pin("J_OSCL", 2, "SCL_1V2", "L", 2.54)

    # --------------------------------------------------------------------------
    # Block 11: Split-I2C Bidirectional Level Translator (BSS138) & Pull-Ups
    # --------------------------------------------------------------------------
    # 1.2V Pull-Ups
    sch.add_instance("R_PU_SDA1", "Device:R", "3k3_1%", 294.64, 167.64, 0, "Resistor_SMD:R_0603_1608Metric", "1.2V SDA Pull-Up")
    sch.connect_pin_to_power("R_PU_SDA1", 1, "+1V2", "U", 2.54)
    sch.connect_pin("R_PU_SDA1", 2, "SDA_1V2", "D", 2.54)

    sch.add_instance("R_PU_SCL1", "Device:R", "3k3_1%", 294.64, 203.2, 0, "Resistor_SMD:R_0603_1608Metric", "1.2V SCL Pull-Up")
    sch.connect_pin_to_power("R_PU_SCL1", 1, "+1V2", "U", 2.54)
    sch.connect_pin("R_PU_SCL1", 2, "SCL_1V2", "D", 2.54)

    # Level Shifter N-MOSFETs (Q1 at Y=172.72, Q2 at Y=208.28 - ample separation)
    q1_x, q1_y = 314.96, 172.72
    sch.add_instance("Q1", "SoC8767:BSS138", "BSS138", q1_x, q1_y, 0, "Package_TO_SOT_SMD:SOT-23", "SDA Bidirectional Level Shifter N-FET")
    sch.connect_pin_to_power("Q1", 1, "+1V2", "L", 2.54) # Gate to 1.2V
    sch.connect_pin("Q1", 2, "SDA_1V2", "D", 2.54)       # Source to 1.2V side
    sch.connect_pin("Q1", 3, "SDA_3V3", "U", 2.54)       # Drain to 3.3V side

    q2_x, q2_y = 314.96, 208.28
    sch.add_instance("Q2", "SoC8767:BSS138", "BSS138", q2_x, q2_y, 0, "Package_TO_SOT_SMD:SOT-23", "SCL Bidirectional Level Shifter N-FET")
    sch.connect_pin_to_power("Q2", 1, "+1V2", "L", 2.54) # Gate to 1.2V
    sch.connect_pin("Q2", 2, "SCL_1V2", "D", 2.54)       # Source to 1.2V side
    sch.connect_pin("Q2", 3, "SCL_3V3", "U", 2.54)       # Drain to 3.3V side

    # 3.3V Pull-Ups
    sch.add_instance("R_PU_SDA2", "Device:R", "4k7_1%", 330.2, 167.64, 0, "Resistor_SMD:R_0603_1608Metric", "3.3V SDA Pull-Up")
    sch.connect_pin_to_power("R_PU_SDA2", 1, "+3V3", "U", 2.54)
    sch.connect_pin("R_PU_SDA2", 2, "SDA_3V3", "D", 2.54)

    sch.add_instance("R_PU_SCL2", "Device:R", "4k7_1%", 330.2, 203.2, 0, "Resistor_SMD:R_0603_1608Metric", "3.3V SCL Pull-Up")
    sch.connect_pin_to_power("R_PU_SCL2", 1, "+3V3", "U", 2.54)
    sch.connect_pin("R_PU_SCL2", 2, "SCL_3V3", "D", 2.54)

    sch.add_instance("TP_SDA_1V2", "Connector:TestPoint", "TP_SDA_1V2", 284.48, 177.8, 0, "TestPoint:TestPoint_Pad_D1.5mm", "1.2V SDA Test Point")
    sch.connect_pin("TP_SDA_1V2", 1, "SDA_1V2", "L", 2.54)

    sch.add_instance("TP_SCL_1V2", "Connector:TestPoint", "TP_SCL_1V2", 284.48, 213.36, 0, "TestPoint:TestPoint_Pad_D1.5mm", "1.2V SCL Test Point")
    sch.connect_pin("TP_SCL_1V2", 1, "SCL_1V2", "L", 2.54)

    sch.add_instance("TP_SDA_3V3", "Connector:TestPoint", "TP_SDA_3V3", 345.44, 167.64, 0, "TestPoint:TestPoint_Pad_D1.5mm", "3.3V SDA Test Point")
    sch.connect_pin("TP_SDA_3V3", 1, "SDA_3V3", "L", 2.54)

    sch.add_instance("TP_SCL_3V3", "Connector:TestPoint", "TP_SCL_3V3", 345.44, 203.2, 0, "TestPoint:TestPoint_Pad_D1.5mm", "3.3V SCL Test Point")
    sch.connect_pin("TP_SCL_3V3", 1, "SCL_3V3", "L", 2.54)

    # --------------------------------------------------------------------------
    # Block 12: TMP117 High-Precision Temperature Sensor (Near QFN DAP)
    # --------------------------------------------------------------------------
    t_x, t_y = 203.2, 88.9
    sch.add_instance("U_TEMP", "Sensor_Temperature:TMP117xxDRV", "TMP117", t_x, t_y, 0, "Package_SON:WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm", "+-0.1C High-Precision Digital Temperature Sensor")
    sch.connect_pin("U_TEMP", 1, "SCL_3V3", "L", 2.54)
    sch.connect_pin_to_power("U_TEMP", 2, "GND", "D", 2.54)
    sch.connect_pin("U_TEMP", 3, "TEMP_ALERT_3V3", "R", 2.54)
    sch.connect_pin_to_power("U_TEMP", 4, "GND", "L", 2.54) # Address 0x48
    sch.connect_pin_to_power("U_TEMP", 5, "+3V3", "U", 2.54)
    sch.connect_pin("U_TEMP", 6, "SDA_3V3", "L", 2.54)

    sch.add_instance("C_TEMP", "Device:C", "100nF", 187.96, 88.9, 0, "Capacitor_SMD:C_0402_1005Metric", "TMP117 Decoupling")
    sch.connect_pin_to_power("C_TEMP", 1, "+3V3", "U", 2.54)
    sch.connect_pin_to_power("C_TEMP", 2, "GND", "D", 2.54)

    sch.add_instance("R_PU_ALRT", "Device:R", "10k", 218.44, 88.9, 0, "Resistor_SMD:R_0603_1608Metric", "TMP117 Alert Pull-Up")
    sch.connect_pin_to_power("R_PU_ALRT", 1, "+3V3", "U", 2.54)
    sch.connect_pin("R_PU_ALRT", 2, "TEMP_ALERT_3V3", "D", 2.54)

    sch.add_instance("TP_ALRT", "Connector:TestPoint", "TP_ALRT", 228.6, 88.9, 0, "TestPoint:TestPoint_Pad_D1.5mm", "TMP117 Alert Test Point")
    sch.connect_pin("TP_ALRT", 1, "TEMP_ALERT_3V3", "L", 2.54)

    # --------------------------------------------------------------------------
    # Block 13: Host Microcontroller / FPGA Interface Header (J_HOST - 2x6)
    # --------------------------------------------------------------------------
    jh_x, jh_y = 381.0, 152.4
    sch.add_instance("J_HOST", "Connector_Generic:Conn_02x06_Odd_Even", "J_HOST", jh_x, jh_y, 0, "Connector_PinHeader_2.54mm:PinHeader_2x06_P2.54mm_Vertical", "Host MCU / FPGA / SMU Digital & Power Interface")
    sch.connect_pin_to_power("J_HOST", 1, "+3V3", "L", 2.54)
    sch.connect_pin_to_power("J_HOST", 2, "+3V3", "R", 2.54)
    sch.connect_pin_to_power("J_HOST", 3, "GND", "L", 2.54)
    sch.connect_pin_to_power("J_HOST", 4, "GND", "R", 2.54)
    sch.connect_pin("J_HOST", 5, "SDA_3V3", "L", 2.54)
    sch.connect_pin("J_HOST", 6, "SCL_3V3", "R", 2.54)
    sch.connect_pin("J_HOST", 7, "RESET_3V3", "L", 2.54)
    sch.connect_pin("J_HOST", 8, "ENABLE_3V3", "R", 2.54)
    sch.connect_pin("J_HOST", 9, "ALARM_3V3", "L", 2.54)
    sch.connect_pin("J_HOST", 10, "CLK_D_3V3", "R", 2.54)
    sch.connect_pin("J_HOST", 11, "TEMP_ALERT_3V3", "L", 2.54)
    sch.connect_pin_to_power("J_HOST", 12, "GND", "R", 2.54)

    # --------------------------------------------------------------------------
    # Block 14: Power Input, Status LEDs & Ground Loops
    # --------------------------------------------------------------------------
    # Power Input Connector (J_PWR_IN - 2-pin)
    sch.add_instance("J_PWR_IN", "Connector_Generic:Conn_01x02", "J_PWR_IN", 35.56, 40.64, 0, "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", "External Bench +3.3V Power / SMU Input")
    sch.connect_pin_to_power("J_PWR_IN", 1, "+3V3", "L", 2.54)
    sch.connect_pin_to_power("J_PWR_IN", 2, "GND", "L", 2.54)

    sch.add_instance("C_MAIN_BULK", "Device:C", "10uF", 50.8, 40.64, 0, "Capacitor_SMD:C_0805_2012Metric", "Board Bulk 3.3V Capacitor")
    sch.connect_pin_to_power("C_MAIN_BULK", 1, "+3V3", "U", 2.54)
    sch.connect_pin_to_power("C_MAIN_BULK", 2, "GND", "D", 2.54)

    # 3.3V Power LED (Green)
    sch.add_instance("R_LED_3V3", "Device:R", "1k", 71.12, 35.56, 0, "Resistor_SMD:R_0603_1608Metric", "3.3V LED Resistor")
    sch.connect_pin_to_power("R_LED_3V3", 1, "+3V3", "U", 2.54)
    sch.connect_pin("R_LED_3V3", 2, "LED_3V3_ANODE", "D", 2.54)

    sch.add_instance("D_PWR_3V3", "Device:LED", "GREEN", 71.12, 45.72, 90, "LED_SMD:LED_0603_1608Metric", "3.3V Power Good Indicator")
    sch.connect_pin("D_PWR_3V3", 2, "LED_3V3_ANODE", "U", 2.54)
    sch.connect_pin_to_power("D_PWR_3V3", 1, "GND", "D", 2.54)

    # 1.2V Power LED (Green)
    sch.add_instance("R_LED_1V2", "Device:R", "470R", 88.9, 35.56, 0, "Resistor_SMD:R_0603_1608Metric", "1.2V LED Resistor")
    sch.connect_pin_to_power("R_LED_1V2", 1, "+1V2", "U", 2.54)
    sch.connect_pin("R_LED_1V2", 2, "LED_1V2_ANODE", "D", 2.54)

    sch.add_instance("D_PWR_1V2", "Device:LED", "GREEN", 88.9, 45.72, 90, "LED_SMD:LED_0603_1608Metric", "1.2V Power Good Indicator")
    sch.connect_pin("D_PWR_1V2", 2, "LED_1V2_ANODE", "U", 2.54)
    sch.connect_pin_to_power("D_PWR_1V2", 1, "GND", "D", 2.54)

    # ALARM Asserted LED (Red)
    sch.add_instance("R_LED_ALM", "Device:R", "1k", 106.68, 35.56, 0, "Resistor_SMD:R_0603_1608Metric", "Alarm LED Resistor")
    sch.connect_pin("R_LED_ALM", 1, "ALARM_3V3", "U", 2.54)
    sch.connect_pin("R_LED_ALM", 2, "LED_ALM_ANODE", "D", 2.54)

    sch.add_instance("D_ALARM", "Device:LED", "RED", 106.68, 45.72, 90, "LED_SMD:LED_0603_1608Metric", "Alarm Asserted Indicator")
    sch.connect_pin("D_ALARM", 2, "LED_ALM_ANODE", "U", 2.54)
    sch.connect_pin_to_power("D_ALARM", 1, "GND", "D", 2.54)

    # Scope Ground Loops (Keystone 5015)
    sch.add_instance("TP_GND_SMA1", "Connector:TestPoint", "GND_LOOP", 88.9, 147.32, 0, "TestPoint:TestPoint_Keystone_5015_Micro_Mini", "Scope Ground Loop near SMA_BGR")
    sch.connect_pin_to_power("TP_GND_SMA1", 1, "GND", "D", 2.54)

    sch.add_instance("TP_GND_SMA2", "Connector:TestPoint", "GND_LOOP", 35.56, 147.32, 0, "TestPoint:TestPoint_Keystone_5015_Micro_Mini", "Scope Ground Loop near SMA_CAL")
    sch.connect_pin_to_power("TP_GND_SMA2", 1, "GND", "D", 2.54)

    sch.add_instance("TP_GND_SMA3", "Connector:TestPoint", "GND_LOOP", 35.56, 187.96, 0, "TestPoint:TestPoint_Keystone_5015_Micro_Mini", "Scope Ground Loop near SMA_CLK_D")
    sch.connect_pin_to_power("TP_GND_SMA3", 1, "GND", "D", 2.54)

    sch.add_instance("TP_GND_SMA4", "Connector:TestPoint", "GND_LOOP", 292.1, 86.36, 0, "TestPoint:TestPoint_Keystone_5015_Micro_Mini", "Scope Ground Loop near SMA_CLK_A")
    sch.connect_pin_to_power("TP_GND_SMA4", 1, "GND", "D", 2.54)

    sch.add_instance("TP_GND_MAIN", "Connector:TestPoint", "GND_LOOP", 35.56, 50.8, 0, "TestPoint:TestPoint_Keystone_5015_Micro_Mini", "Scope Ground Loop near Main Power")
    sch.connect_pin_to_power("TP_GND_MAIN", 1, "GND", "D", 2.54)

    # --------------------------------------------------------------------------
    # Block 15: Power Flags for ERC (on +3V3 and GND)
    # --------------------------------------------------------------------------
    sch.add_pwr_flag("+3V3", 25.4, 30.48)
    sch.add_pwr_flag("GND", 25.4, 50.8)

    # Save to file
    out_file = "hardware_test_pcb/SoC8767_Test_PCB.kicad_sch"
    sch.generate_schematic(out_file)

if __name__ == "__main__":
    build()

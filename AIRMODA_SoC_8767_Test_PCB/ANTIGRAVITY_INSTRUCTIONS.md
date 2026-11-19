Antigravity Agent Instructions — SoC8767 (AIRMODA Gas Sensor SoC) Test PCB

1. Project Overview & Repository Context

Target IC: SoC8767 (AIRMODA Gas Sensor System-on-Chip, Release v1.0.0) [cite: 2]

Process Technology: IHP SG13G2 130 nm BiCMOS [cite: 2]

Package: QFN-24 (4 mm × 4 mm, 0.5 mm pitch, 6 leads per side, exposed die attach paddle / DAP) [cite: 2]

GitHub Repository: https://github.com/CDTA-DMN/IHP__SoC8767/tree/main [cite: 2, 3]

Goal for Antigravity Agent: Automate KiCad symbol/footprint generation, review/optimize the schematic (.kicad_sch) and 4-layer PCB layout (.kicad_pcb), enforce mixed-signal IC testability rules, run kicad-cli ERC/DRC checks, and prepare manufacturing outputs (Gerbers, Drill, BOM, Pick & Place).

2. Authoritative Pinout & Electrical Constraints (QFN-24)

CRITICAL: Antigravity MUST enforce these exact pin mappings and voltage domains during KiCad symbol creation, schematic review, and ERC/DRC validation [cite: 1, 2]:

| QFN-24 Pin | Die Pad | Signal Name | Type | Voltage / Domain | Mandatory PCB & Schematic Rules |

| --- | --- | --- | --- | --- | --- |

| 1 | — | NC | Unconnected | Floating | Leave unbonded/floating; do NOT route traces under or to this pin [cite: 1, 2]. |

| 2 | P1 | BGR_1V0 | Analog Out/In | 1.0 V (High-Z) | Place 100 nF (0402 X7R) + 1 µF (0603 X7R) < 2 mm from pin [cite: 1, 2]. Route to unity-gain op-amp buffer (e.g., OPA320) + SMA/TP for SMU overdrive or probing [cite: 1]. |

| 3 | P2 | VSS | Ground | 0 V (Substrate) | Direct via to solid Layer 2 GND plane (down-bonded to DAP) [cite: 2]. |

| 4 | P3 | IN_SENS | Analog Input | Analog ADC In | Surround trace with stitched VSS guard ring (vias every 1.5–2 mm) [cite: 1]. Connect to SMA connector + optional RC anti-aliasing filter + sensor header [cite: 1, 2]. |

| 5 | P4 | ALARM | Digital Out | 1.2 V CMOS | Level-shift (1.2 V -> 3.3 V) before driving host MCU/FPGA or indicator LED [cite: 1, 2]. |

| 6 | — | NC | Unconnected | Floating | Leave floating [cite: 1, 2]. |

| 7 | — | NC | Unconnected | Floating | Leave floating [cite: 1, 2]. |

| 8 | P5 | RESET | Digital In | 1.2 V CMOS | Level-shift (3.3 V -> 1.2 V) + 2-pin isolation jumper + tactile switch + 10 kΩ pull resistor [cite: 1, 2]. |

| 9 | P6 | VDD_1V2 | Power / Out | 1.2 V LDO (Low-Z) | Place 100 nF + 1 µF X7R < 2 mm from pin [cite: 1]. Include 0 Ω isolation jumper to external backup 1.2 V LDO (NEVER force external voltage while internal LDO is active) [cite: 1]. |

| 10 | P7 | AD0 | Digital In | 1.2 V CMOS | 2-pin jumper / DIP switch to select GND (0 V) or 1.2 V [cite: 2]. |

| 11 | P8 | ENABLE | Digital In | 1.2 V CMOS | Level-shift (3.3 V -> 1.2 V) + 2-pin isolation jumper / switch for power-down & startup testing [cite: 1, 2]. |

| 12 | — | NC | Unconnected | Floating | Leave floating [cite: 1, 2]. |

| 13 | — | NC | Unconnected | Floating | Leave floating [cite: 1, 2]. |

| 14 | P9 | I_SDA | Digital In | 1.2 V CMOS | Split-pin I2C input; merge with O_SDA via open-drain level shifter (1.2 V <-> 3.3 V, e.g., BSS138 or TCA9406) + 2.2 kΩ–4.7 kΩ pull-up to 1.2 V + 2-pin jumper [cite: 1, 2]. |

| 15 | P10 | I_SCL | Digital In | 1.2 V CMOS | Split-pin I2C input; merge with O_SCL via open-drain level shifter + 2.2 kΩ–4.7 kΩ pull-up to 1.2 V + 2-pin jumper [cite: 1, 2]. |

| 16 | P11 | O_SDA | Digital Out | 1.2 V CMOS | Split-pin I2C output; open-drain combine with I_SDA + 2-pin isolation jumper [cite: 1, 2]. |

| 17 | P12 | O_SCL | Digital Out | 1.2 V CMOS | Split-pin I2C output; open-drain combine with I_SCL + 2-pin isolation jumper [cite: 1, 2]. |

| 18 | — | NC | Unconnected | Floating | Leave floating [cite: 1, 2]. |

| 19 | — | NC | Unconnected | Floating | Leave floating [cite: 1, 2]. |

| 20 | P13 | CLK_D | Digital In | 1.2 V CMOS | Route as short 50 Ω single-ended microstrip from SMA / 1.2 V oscillator (via 0 Ω selector) with 22 Ω–33 Ω series damping resistor at source [cite: 1, 2]. |

| 21 | P14 | CLK_A | Analog Out | Analog Clock | Buffer through high-impedance unity-gain op-amp before SMA/oscilloscope probing (do NOT load directly with passive 10× probe) [cite: 1, 2]. |

| 22 | P15 | VDD_1V2 | Power / Out | 1.2 V LDO (Low-Z) | Place 100 nF + 1 µF X7R < 2 mm from pin; isolate/star-connect with Pin 9 via 0 Ω jumper [cite: 1, 2]. |

| 23 | P16 | VDD_3V3 | Power In | 1.8 V – 3.3 V | Place 10 µF bulk + 1 µF + 100 nF X7R caps + 1 Ω / 10 Ω precision current-sense shunt resistor (with 2-pin shorting jumper) [cite: 1, 2]. |

| 24 | — | NC | Unconnected | Floating | Leave floating [cite: 1, 2]. |

| DAP | P2 | VSS | Thermal/GND | 0 V (Substrate) | 2.6 mm × 2.6 mm exposed pad with 3×3 array of 0.3 mm thermal/ground vias to Layer 2 GND; 60–70% solder paste coverage [cite: 1, 2]. |

3. Step-by-Step Execution Workflow for Antigravity

When working inside the KiCad project directory (synced with https://github.com/CDTA-DMN/IHP__SoC8767/tree/main), follow this exact sequence [cite: 2, 3]:

Step 1: Repository Inspection & Symbol/Footprint Generation

Inspect the cloned GitHub repository (IHP__SoC8767) for existing .kicad_sym, .kicad_mod, .kicad_sch, .kicad_pcb, pinout tables, or RTL/Verilog testbench files.

Generate or verify the SoC8767 QFN-24 (4×4 mm, 0.5 mm pitch) symbol and footprint [cite: 2]:

Ensure Pin 25 (DAP) is mapped to VSS [cite: 2].

Mark Pins 1, 6, 7, 12, 13, 18, 19, 24 explicitly as No Connect (NC) in the schematic symbol [cite: 1, 2].

Step 2: Schematic Design & Audit (.kicad_sch)

Verify and insert the following mandatory subcircuits:

Voltage Level Translators (1.2 V <-> 3.3 V):

Never allow any 3.3 V net to connect directly to SoC8767 pins 4, 5, 8, 9, 10, 11, 14, 15, 16, 17, 20, 21, 22 [cite: 1, 2].

Use dual-supply level shifters (SN74AXC4T774 / TXU0304) for unidirectional control/clock lines (CLK_D, RESET, ENABLE, ALARM) [cite: 1].

Implement split-I2C merging (I_SDA + O_SDA -> SDA_1V2 -> SDA_3V3, and I_SCL + O_SCL -> SCL_1V2 -> SCL_3V3) with 2.2 kΩ–4.7 kΩ pull-ups to 1.2 V on the SoC side and 3.3 V on the MCU/FPGA header [cite: 1].

Power Isolation & Current Profiling:

Add a 1 Ω (or 10 Ω) shunt resistor with a parallel 2-pin shorting header in series with VDD_3V3 (Pin 23) for µA/mA SMU profiling [cite: 1].

Add 0 Ω isolation resistors (or 2-pin jumpers) on Pins 9 and 22 (VDD_1V2) separating the internal LDO outputs from an optional external 1.2 V lab LDO (TPS7A2012) to prevent LDO contention [cite: 1].

Analog Front-End & Active Probing:

Add an SMA connector + optional RC filter footprint + gas sensor daughterboard header on IN_SENS (Pin 4) [cite: 1].

Add unity-gain CMOS op-amp buffers (OPA320 or TLV9062) on BGR_1V0 (Pin 2) and CLK_A (Pin 21) driving SMA/test points so oscilloscope probes do not load high-impedance nodes [cite: 1].

Testability Jumpers:

Place 2-pin test/isolation headers on I_SDA, O_SDA, I_SCL, O_SCL, ENABLE, RESET, and AD0, plus SMD ground loops (Keystone 5015) near every SMA connector [cite: 1].

Step 3: 4-Layer PCB Layout & Routing Rules (.kicad_pcb)

Configure and verify the 4-layer stackup and routing constraints [cite: 1]:

Layer 1 (F.Cu): Component placement, short controlled-impedance clock/analog traces, local VSS guard rings [cite: 1].

Layer 2 (In1.Cu): Solid, uninterrupted VSS (GND) reference plane [cite: 1].

Layer 3 (In2.Cu): Power distribution (VDD_3V3, VDD_1V2_EXT, 3V3_HOST) [cite: 1].

Layer 4 (B.Cu): Low-speed digital routing, test headers, silkscreen labels [cite: 1].

Critical Layout Checks:

Decoupling caps (100 nF 0402 + 1 µF 0603) placed < 2 mm from Pins 2, 9, 22, 23 with direct vias to In1.Cu (VSS) [cite: 1].

IN_SENS (Pin 4) surrounded by a stitched VSS guard ring (via pitch 1.5–2 mm) [cite: 1].

CLK_D (Pin 20) routed as a 50 Ω single-ended microstrip with a 22 Ω–33 Ω series resistor at the driver [cite: 1].

QFN-24 DAP populated with a 3×3 array of 0.3 mm vias to In1.Cu (VSS) and stencil paste reduced to 60–70% [cite: 1].

Step 4: Automated Verification & Fab Export (kicad-cli)

Before finishing any task, Antigravity MUST execute via terminal / kicad-cli:

ERC (Electrical Rules Check):

kicad-cli sch erc --severity-all --exit-code-violations <project>.kicad_sch



DRC (Design Rules Check):

kicad-cli pcb drc --severity-all --exit-code-violations <project>.kicad_pcb



Manufacturing Outputs (only after 0 ERC/DRC errors):

Generate Gerbers (F.Cu, In1.Cu, In2.Cu, B.Cu, F.Mask, B.Mask, F.SilkS, B.SilkS, F.Paste, Edge.Cuts), Excellon drill files, Pick-and-Place (.pos), and BOM (.csv) matched to JLCPCB/LCSC or DigiKey part numbers.

4. Reference Documents in This Project Workspace

01_Layout_and_Pinout_Specs/SoC8767_Pinout_and_Characteristics.md — Complete QFN-24 pin mapping, die pad coordinates, and electrical specs [cite: 2].

02_Test_PCB_Good_Practices_and_RTL/SoC8767_Test_PCB_Good_Practices_and_RTL.md — Detailed PCB guidelines, CDTA/Infineon lab bring-up methodology rules, and Verilog FPGA split-I2C test bridge (soc8767_fpga_test_bridge) [cite: 1].

5. Modular Block-by-Block & Full-Chip Isolation Architecture

The Test PCB MUST support two distinct operating modes without board rework:

Mode A (Block-by-Block Characterization): Isolate each internal SoC block (Bandgap, Digital LDO, Analog LDO, Digital Core/I2C, AFE/ADC) so it can be stimulated and measured independently, or bypassed/overdriven externally if a preceding block fails during bring-up.

Mode B (Full-Chip System Integration): Close internal power/reference paths and connect the real AIRMODA gas sensor daughterboard to validate end-to-end operation from gas stimulus to I2C readout and ALARM trigger.

5.1 Required PCB Isolation Jumpers & Bypass Switches

Antigravity MUST include the following labeled 2-pin/3-pin jumpers (2.54 mm pitch) and shunt resistors in the KiCad schematic and silkscreen:

J_BGR (Pin 2 — BGR_1V0): Isolates BGR_1V0 from external SMU overdrive. Keep OPA320 unity-gain buffer permanently attached for non-invasive oscilloscope/DMM probing.

J_LDO_DIG (Pin 9 — VDD_1V2 Digital): 3-pin selector or dual 0 Ω/jumper bridge selecting between internal Digital LDO output and external 1.2 V lab supply (TPS7A2012), plus a 1 Ω series current-sense shunt resistor.

J_LDO_ANA (Pin 22 — VDD_1V2 Analog): 3-pin selector or dual 0 Ω/jumper bridge selecting between internal Analog LDO output and external 1.2 V lab supply, plus a 1 Ω series current-sense shunt resistor. (CRITICAL: Never enable internal LDO while external 1.2 V is connected).

J_PWR_MAIN (Pin 23 — VDD_3V3): Series 1 Ω / 10 Ω precision shunt resistor with parallel shorting jumper + electronic current limiter (≤ 10 mA bring-up compliance).

J_SENS_SRC (Pin 4 — IN_SENS): Selects between precision calibration input (SMA / onboard 16-bit DAC) and real gas sensor conditioning header (TIA / Wheatstone bridge with digital potentiometer).

J_I2C_SPLIT (Pins 14, 15, 16, 17): 4 individual 2-pin isolation jumpers on I_SDA, I_SCL, O_SDA, and O_SCL to break the bus and probe input vs. output signals separately.

5.2 Smart On-Board Characterization Add-Ons

Modular Carrier Option: Support either direct QFN-24 mounting or a pluggable 3 cm × 3 cm DUT carrier board so the SoC can be tested inside a thermal (-40 °C to +125 °C) or gas chamber while host electronics remain outside.

Analog MUX (TMUX1108 / ADG708): Route BGR_1V0, VDD_1V2 (Pin 9 & Pin 22), and VDD_3V3 through a low-leakage analog multiplexer for automated multi-node SMU/DMM sweeps.

On-Board Thermal & Light Shielding: Place a digital temperature sensor (TMP117) within 2 mm of the QFN-24 DAP, and include a grounded removable metallic/opaque EMI + light-tight shield frame over the SoC8767 area to eliminate photovoltaic drift on BGR_1V0.

6-Stage Bring-Up Verification Checklist:

Quiescent leakage check (ENABLE = 0, current limit ≤ 10 mA).

Standalone BGR_1V0 check (ENABLE = 1, RESET = 1, light shield closed).

Standalone VDD_1V2 LDO line/load & PSRR sweep (VDD_3V3 from 1.8 V to 3.3 V).

Standalone Digital Core & split-I2C register read/write + AD0 & ALARM verification.

Standalone AFE/ADC dynamic & static characterization (IN_SENS via SMA/DAC, CLK_A buffered).

Full-chip closed-loop gas sensor test with real AIRMODA sensor and ALARM latency capture.
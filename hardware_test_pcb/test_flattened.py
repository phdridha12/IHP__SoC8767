import subprocess

# Test Device:R embedded in lib_symbols
sch = f'''(kicad_sch
\t(version 20250114)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "00000000-0000-0000-0000-000000000001")
\t(paper "A4")
\t(lib_symbols
\t\t(symbol "Device:R"
\t\t\t(pin_numbers hide)
\t\t\t(pin_names (offset 0))
\t\t\t(exclude_from_sim no) (in_bom yes) (on_board yes)
\t\t\t(property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
\t\t\t(property "Value" "R" (at 0 0 90) (effects (font (size 1.27 1.27))))
\t\t\t(property "Footprint" "" (at -1.778 0 90) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t\t(property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t\t(symbol "R_0_1"
\t\t\t\t(rectangle (start -1.016 -2.54) (end 1.016 2.54)
\t\t\t\t\t(stroke (width 0.254) (type default))
\t\t\t\t\t(fill (type none))
\t\t\t\t)
\t\t\t)
\t\t\t(symbol "R_1_1"
\t\t\t\t(pin passive line (at 0 3.81 270) (length 1.27)
\t\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "1" (effects (font (size 1.27 1.27))))
\t\t\t\t)
\t\t\t\t(pin passive line (at 0 -3.81 90) (length 1.27)
\t\t\t\t\t(name "~" (effects (font (size 1.27 1.27))))
\t\t\t\t\t(number "2" (effects (font (size 1.27 1.27))))
\t\t\t\t)
\t\t\t)
\t\t)
\t)
\t(symbol (lib_id "Device:R") (at 101.6 101.6 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
\t\t(uuid "00000000-0000-0000-0000-000000000002")
\t\t(property "Reference" "R1" (at 101.6 99.06 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "1k" (at 101.6 104.14 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 101.6 101.6 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t(property "Datasheet" "~" (at 101.6 101.6 0) (effects (font (size 1.27 1.27)) (hide yes)))
\t\t(pin "1" (uuid "00000000-0000-0000-0000-000000000003"))
\t\t(pin "2" (uuid "00000000-0000-0000-0000-000000000004"))
\t)
)'''

with open("hardware_test_pcb/test_flattened.kicad_sch", "w", encoding="utf-8") as f:
    f.write(sch)

res = subprocess.run([
    r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe", "sch", "erc",
    "--severity-all", "hardware_test_pcb/test_flattened.kicad_sch"
], capture_output=True, text=True)

print("Return code:", res.returncode)
print("Stderr:", res.stderr)
with open("test_flattened-erc.rpt", "r", encoding="utf-8") as f:
    rpt = f.read()
print("Report:")
print(rpt)

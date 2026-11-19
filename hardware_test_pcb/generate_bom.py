import re

with open("hardware_test_pcb/SoC8767_Test_PCB.net", "r", encoding="utf-8") as f:
    text = f.read()

comp_sec = re.search(r'\(components(.*?)\n\t\)', text, re.DOTALL)
if comp_sec:
    comps = re.findall(r'\(comp\s+\(ref\s+"([^"]+)"\)\s+\(value\s+"([^"]+)"\)\s+\(footprint\s+"([^"]*)"\)', comp_sec.group(1))
    # Exclude power flags
    real_comps = [(r, v, fp) for r, v, fp in comps if not r.startswith('#')]
    print(f"Total Bill of Materials: {len(real_comps)} components\n")
    print(f"{'Designator':<16} | {'Value':<14} | {'Footprint'}")
    print("-" * 80)
    for r, v, fp in sorted(real_comps, key=lambda x: (x[0][0], int(re.search(r'\d+', x[0]).group()) if re.search(r'\d+', x[0]) else 0, x[0])):
        print(f"{r:<16} | {v:<14} | {fp}")

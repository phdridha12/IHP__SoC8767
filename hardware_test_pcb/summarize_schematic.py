import re

with open("hardware_test_pcb/SoC8767_Test_PCB.net", "r", encoding="utf-8") as f:
    text = f.read()

# Parse components
# (comp (ref "...") (value "...") (footprint "...") ... (property "Description" "..."))
comp_pattern = re.compile(r'\(comp\s+\(ref\s+"([^"]+)"\)\s+\(value\s+"([^"]+)"\)\s+\(footprint\s+"([^"]*)"\).*?\(property\s+"Description"\s+"([^"]*)"\)', re.DOTALL)
components = []
for m in comp_pattern.finditer(text):
    ref, val, fp, desc = m.groups()
    if not ref.startswith('#'):
        components.append((ref, val, fp, desc))

print(f"=== Total Components: {len(components)} ===")
for ref, val, fp, desc in sorted(components, key=lambda x: (x[0][0], int(re.search(r'\d+', x[0]).group()) if re.search(r'\d+', x[0]) else 0)):
    print(f"{ref:<14} | {val:<12} | {fp:<45} | {desc}")

# Parse nets
# (net (code "...") (name "...") (node (ref "...") (pin "...")) ...)
net_blocks = re.findall(r'\(net\s+\(code\s+"[^"]+"\)\s+\(name\s+"([^"]+)"\)(.*?)\n\t\t\)', text, re.DOTALL)
print(f"\n=== Total Nets: {len(net_blocks)} ===")
for name, nodes_str in sorted(net_blocks, key=lambda x: x[0]):
    nodes = re.findall(r'\(node\s+\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"\)', nodes_str)
    node_str = ", ".join([f"{r}.{p}" for r, p in nodes if not r.startswith('#')])
    print(f"Net {name:<18} ({len(nodes):2d} pins): {node_str}")

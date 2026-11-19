import os, re, uuid

def new_uuid():
    return str(uuid.uuid4())

kicad_sym_dir = r"C:\Program Files\KiCad\10.0\share\kicad\symbols"

def extract_flattened_symbol(lib_file, sym_name, new_lib_id):
    if lib_file.startswith("local:"):
        path = lib_file.replace("local:", "")
    else:
        path = os.path.join(kicad_sym_dir, f"{lib_file}.kicad_sym")
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    def get_symbol_text(name):
        idx = content.find(f'(symbol "{name}"')
        if idx == -1:
            raise ValueError(f"Symbol {name} not found in {lib_file}")
        i = idx + len(f'(symbol "{name}"')
        d = 1
        while d > 0 and i < len(content):
            if content[i] == '(': d += 1
            elif content[i] == ')': d -= 1
            i += 1
        return content[idx:i]

    sym_text = get_symbol_text(sym_name)
    m_ext = re.search(r'\(extends\s+"([^"]+)"\)', sym_text)
    if not m_ext:
        return re.sub(r'\(symbol\s+"' + re.escape(sym_name) + r'"', f'(symbol "{new_lib_id}"', sym_text, count=1)
    
    parent_name = m_ext.group(1)
    parent_text = get_symbol_text(parent_name)
    sub_syms = re.findall(r'(\(symbol\s+"' + re.escape(parent_name) + r'_\d+_\d+".*?\n\t\t\))', parent_text, re.DOTALL)
    
    prefix = new_lib_id.split(":")[-1]
    sub_syms_renamed = []
    for ss in sub_syms:
        renamed = re.sub(r'\(symbol\s+"' + re.escape(parent_name) + r'_', f'(symbol "{prefix}_', ss)
        sub_syms_renamed.append(renamed)
    
    child_clean = re.sub(r'\s*\(extends\s+"[^"]+"\)', '', sym_text)
    child_clean = re.sub(r'\(symbol\s+"' + re.escape(sym_name) + r'"', f'(symbol "{new_lib_id}"', child_clean, count=1)
    child_clean = child_clean.rstrip()
    if child_clean.endswith(')'):
        child_clean = child_clean[:-1].rstrip()
    
    return child_clean + "\n" + "\n".join(sub_syms_renamed) + "\n\t)"


class SchematicBuilder:
    def __init__(self, title="SoC8767 Test PCB"):
        self.title = title
        self.sch_uuid = new_uuid()
        self.lib_symbols = {}
        self.symbol_pins = {}
        self.instances = []
        self.wires = []
        self.labels = []
        self.no_connects = []
        self.junctions = []
        self.power_symbols = []
        self.pwr_flag_count = 0
        self.pwr_sym_count = 0

    def register_symbol(self, lib_file, sym_name, new_lib_id):
        s_def = extract_flattened_symbol(lib_file, sym_name, new_lib_id)
        self.lib_symbols[new_lib_id] = s_def
        
        # Parse pins: (num, name, px, py, pa, ptype)
        pin_matches = re.findall(
            r'\(pin\s+(\w+)\s+(\w+)\s+\(at\s+([-\d\.]+)\s+([-\d\.]+)\s+([-\d\.]+)\)\s+\(length\s+([-\d\.]+)\).*?\(name\s+"([^"]*)".*?\(number\s+"([^"]*)"',
            s_def, re.DOTALL
        )
        pins = {num: (name, float(px), float(py), float(pa), ptype) for ptype, pshape, px, py, pa, pl, name, num in pin_matches}
        self.symbol_pins[new_lib_id] = pins

    def add_instance(self, ref, lib_id, value, x, y, rot=0, footprint="", desc=""):
        inst_uuid = new_uuid()
        pin_uuids = {}
        for pin_num in self.symbol_pins[lib_id].keys():
            pin_uuids[pin_num] = new_uuid()
        
        inst = {
            "ref": ref,
            "lib_id": lib_id,
            "value": value,
            "x": round(x, 4),
            "y": round(y, 4),
            "rot": rot,
            "footprint": footprint,
            "desc": desc,
            "uuid": inst_uuid,
            "pin_uuids": pin_uuids
        }
        self.instances.append(inst)
        return inst

    def get_instance(self, ref):
        for inst in self.instances:
            if inst["ref"] == ref:
                return inst
        raise ValueError(f"Instance {ref} not found")

    def get_pin_pos(self, ref, pin_num):
        inst = self.get_instance(ref)
        pins = self.symbol_pins[inst["lib_id"]]
        if str(pin_num) not in pins:
            raise ValueError(f"Pin {pin_num} not found on {ref} ({inst['lib_id']})")
        
        name, px, py, pa, ptype = pins[str(pin_num)]
        rot = inst["rot"]
        sx, sy = inst["x"], inst["y"]
        
        if rot == 0:
            wx, wy = sx + px, sy - py
        elif rot == 90:
            wx, wy = sx - py, sy - px
        elif rot == 180:
            wx, wy = sx - px, sy + py
        elif rot == 270:
            wx, wy = sx + py, sy + px
        else:
            raise ValueError(f"Unsupported rotation {rot}")
        
        return round(wx, 4), round(wy, 4)

    def connect_pin(self, ref, pin_num, net_name, wire_dir=None, wire_len=2.54):
        wx, wy = self.get_pin_pos(ref, pin_num)
        if wire_dir is None or wire_len == 0:
            # Direct label on pin
            self.labels.append({
                "name": net_name, "x": wx, "y": wy, "rot": 0, "uuid": new_uuid()
            })
            return wx, wy
        
        if wire_dir == 'L':
            ex, ey = wx - wire_len, wy
            rot = 180
        elif wire_dir == 'R':
            ex, ey = wx + wire_len, wy
            rot = 0
        elif wire_dir == 'U':
            ex, ey = wx, wy - wire_len
            rot = 90
        elif wire_dir == 'D':
            ex, ey = wx, wy + wire_len
            rot = 270
        else:
            raise ValueError(f"Unknown wire_dir {wire_dir}")
        
        ex, ey = round(ex, 4), round(ey, 4)
        self.wires.append({"x1": wx, "y1": wy, "x2": ex, "y2": ey, "uuid": new_uuid()})
        self.labels.append({"name": net_name, "x": ex, "y": ey, "rot": 0, "uuid": new_uuid()})
        return ex, ey

    def connect_pin_nc(self, ref, pin_num):
        wx, wy = self.get_pin_pos(ref, pin_num)
        self.no_connects.append({"x": wx, "y": wy, "uuid": new_uuid()})

    def connect_pin_to_power(self, ref, pin_num, pwr_net, wire_dir=None, wire_len=2.54):
        wx, wy = self.get_pin_pos(ref, pin_num)
        if wire_dir is None or wire_len == 0:
            ex, ey = wx, wy
        else:
            if wire_dir == 'D':
                ex, ey = wx, wy + wire_len
            elif wire_dir == 'U':
                ex, ey = wx, wy - wire_len
            elif wire_dir == 'L':
                ex, ey = wx - wire_len, wy
            elif wire_dir == 'R':
                ex, ey = wx + wire_len, wy
            else:
                raise ValueError(f"Unknown wire_dir {wire_dir}")
            ex, ey = round(ex, 4), round(ey, 4)
            self.wires.append({"x1": wx, "y1": wy, "x2": ex, "y2": ey, "uuid": new_uuid()})
        
        self.pwr_sym_count += 1
        pwr_ref = f"#PWR{self.pwr_sym_count:04d}"
        pwr_lib_id = f"power:{pwr_net}"
        
        # Power symbols: GND is oriented downwards, +3V3/+1V2 upwards
        self.power_symbols.append({
            "lib_id": pwr_lib_id,
            "value": pwr_net,
            "ref": pwr_ref,
            "x": ex,
            "y": ey,
            "rot": 0,
            "uuid": new_uuid(),
            "pin_uuid": new_uuid()
        })
        return ex, ey

    def add_pwr_flag(self, pwr_net, x, y):
        self.pwr_flag_count += 1
        flg_ref = f"#FLG{self.pwr_flag_count:04d}"
        flg_uuid = new_uuid()
        x, y = round(x, 4), round(y, 4)
        
        # Place PWR_FLAG at (x, y)
        self.instances.append({
            "ref": flg_ref,
            "lib_id": "power:PWR_FLAG",
            "value": "PWR_FLAG",
            "x": x,
            "y": y,
            "rot": 0,
            "footprint": "",
            "desc": f"{pwr_net} Power Supply Flag",
            "uuid": flg_uuid,
            "pin_uuids": {"1": new_uuid()}
        })
        
        # If standard global power symbol (+3V3, +1V2, GND), use power symbol to avoid same_local_global_label warning
        if pwr_net in ["+3V3", "+1V2", "GND"]:
            self.pwr_sym_count += 1
            pwr_ref = f"#PWR{self.pwr_sym_count:04d}"
            pwr_lib_id = f"power:{pwr_net}"
            self.power_symbols.append({
                "lib_id": pwr_lib_id,
                "value": pwr_net,
                "ref": pwr_ref,
                "x": x,
                "y": y,
                "rot": 0,
                "uuid": new_uuid(),
                "pin_uuid": new_uuid()
            })
        else:
            # Local power net (e.g. VDD_3V3_SOC): connect with local net label
            self.labels.append({
                "name": pwr_net,
                "x": x,
                "y": y,
                "rot": 0,
                "uuid": new_uuid()
            })

    def generate_schematic(self, output_path):
        lines = []
        lines.append('(kicad_sch')
        lines.append('\t(version 20250114)')
        lines.append('\t(generator "eeschema")')
        lines.append('\t(generator_version "10.0")')
        lines.append(f'\t(uuid "{self.sch_uuid}")')
        lines.append('\t(paper "A3")')
        lines.append('\t(title_block')
        lines.append(f'\t\t(title "{self.title}")')
        lines.append('\t\t(date "2026-11-19")')
        lines.append('\t\t(rev "v1.0.0")')
        lines.append('\t\t(company "AIRMODA / CDTA")')
        lines.append('\t\t(comment 1 "Mixed-Signal Test & Characterization PCB")')
        lines.append('\t\t(comment 2 "Target IC: SoC8767 (IHP SG13G2 130nm BiCMOS, QFN-24)")')
        lines.append('\t\t(comment 3 "Zero 3.3V Direct Exposure, Full Block-by-Block Isolation")')
        lines.append('\t)')
        
        # Library symbols
        lines.append('\t(lib_symbols')
        for s_def in self.lib_symbols.values():
            lines.append(s_def)
        lines.append('\t)')
        
        # Instances
        for inst in self.instances:
            ref = inst["ref"]
            lib_id = inst["lib_id"]
            val = inst["value"]
            x, y = inst["x"], inst["y"]
            rot = inst["rot"]
            fp = inst["footprint"]
            desc = inst["desc"]
            uid = inst["uuid"]
            
            lines.append(f'\t(symbol (lib_id "{lib_id}") (at {x:.4f} {y:.4f} {rot}) (unit 1)')
            lines.append('\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)')
            lines.append(f'\t\t(uuid "{uid}")')
            lines.append(f'\t\t(property "Reference" "{ref}" (at {x:.4f} {y-2.54:.4f} 0) (effects (font (size 1.27 1.27))))')
            lines.append(f'\t\t(property "Value" "{val}" (at {x:.4f} {y+2.54:.4f} 0) (effects (font (size 1.27 1.27))))')
            lines.append(f'\t\t(property "Footprint" "{fp}" (at {x:.4f} {y:.4f} 0) (effects (font (size 1.27 1.27)) (hide yes)))')
            lines.append(f'\t\t(property "Datasheet" "~" (at {x:.4f} {y:.4f} 0) (effects (font (size 1.27 1.27)) (hide yes)))')
            if desc:
                lines.append(f'\t\t(property "Description" "{desc}" (at {x:.4f} {y:.4f} 0) (effects (font (size 1.27 1.27)) (hide yes)))')
            for pnum, puid in inst["pin_uuids"].items():
                lines.append(f'\t\t(pin "{pnum}" (uuid "{puid}"))')
            lines.append('\t)')
        
        # Power symbols
        for pwr in self.power_symbols:
            lib_id = pwr["lib_id"]
            val = pwr["value"]
            ref = pwr["ref"]
            x, y = pwr["x"], pwr["y"]
            rot = pwr["rot"]
            uid = pwr["uuid"]
            puid = pwr["pin_uuid"]
            lines.append(f'\t(symbol (lib_id "{lib_id}") (at {x:.4f} {y:.4f} {rot}) (unit 1)')
            lines.append('\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)')
            lines.append(f'\t\t(uuid "{uid}")')
            lines.append(f'\t\t(property "Reference" "{ref}" (at {x:.4f} {y:.4f} 0) (effects (font (size 1.27 1.27)) (hide yes)))')
            lines.append(f'\t\t(property "Value" "{val}" (at {x:.4f} {y-2.54:.4f} 0) (effects (font (size 1.27 1.27))))')
            lines.append(f'\t\t(property "Footprint" "" (at {x:.4f} {y:.4f} 0) (effects (font (size 1.27 1.27)) (hide yes)))')
            lines.append(f'\t\t(property "Datasheet" "" (at {x:.4f} {y:.4f} 0) (effects (font (size 1.27 1.27)) (hide yes)))')
            lines.append(f'\t\t(pin "1" (uuid "{puid}"))')
            lines.append('\t)')
            
        # Wires
        for w in self.wires:
            lines.append(f'\t(wire (pts (xy {w["x1"]:.4f} {w["y1"]:.4f}) (xy {w["x2"]:.4f} {w["y2"]:.4f}))')
            lines.append('\t\t(stroke (width 0) (type default))')
            lines.append(f'\t\t(uuid "{w["uuid"]}")')
            lines.append('\t)')
            
        # Labels
        for lbl in self.labels:
            lines.append(f'\t(label "{lbl["name"]}" (at {lbl["x"]:.4f} {lbl["y"]:.4f} {lbl["rot"]}) (fields_autoplaced yes)')
            lines.append('\t\t(effects (font (size 1.27 1.27)) (justify left bottom))')
            lines.append(f'\t\t(uuid "{lbl["uuid"]}")')
            lines.append('\t)')
            
        # No connects
        for nc in self.no_connects:
            lines.append(f'\t(no_connect (at {nc["x"]:.4f} {nc["y"]:.4f}) (uuid "{nc["uuid"]}"))')
            
        # Junctions
        for j in self.junctions:
            lines.append(f'\t(junction (at {j["x"]:.4f} {j["y"]:.4f}) (diameter 0) (color 0 0 0 0) (uuid "{j["uuid"]}"))')
            
        lines.append(')')
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"Schematic saved successfully to {output_path}")

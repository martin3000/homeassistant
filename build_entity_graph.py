"""
Liest HA-YAML-Dateien und erzeugt entities_graph.graphml + entities_graph_yed.graphml.
"""

import re
import yaml
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = Path(__file__).parent

# ---------------------------------------------------------------------------
# Farben
# ---------------------------------------------------------------------------
COLORS = {
    "integration":   "#2ECC71",
    "filter":        "#9B59B6",
    "utility_meter": "#E67E22",
    "template":      "#E74C3C",
    "statistics":    "#1ABC9C",
    "history_stats": "#F39C12",
    "rest":          "#3498DB",
    "mqtt":          "#4A90D9",
    "sensor":        "#4A90D9",
    "binary_sensor": "#5DADE2",
    "light":         "#F1C40F",
    "switch":        "#95A5A6",
    "climate":       "#C0392B",
    "input_number":  "#A6ACAF",
    "input_boolean": "#BDC3C7",
    "input_select":  "#D5D8DC",
    "external":      "#7F8C8D",
}

def color(platform, domain="sensor"):
    return COLORS.get(platform) or COLORS.get(domain) or "#7F8C8D"

def slugify(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")

class _IgnoreUnknownTags(yaml.SafeLoader):
    pass

def _ignore_tag(loader, tag_suffix, node):
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    return loader.construct_mapping(node)

_IgnoreUnknownTags.add_multi_constructor("", _ignore_tag)

def load(fname):
    p = BASE / fname
    if not p.exists():
        return None
    with open(p, encoding="utf-8") as f:
        return yaml.load(f, Loader=_IgnoreUnknownTags)

# ---------------------------------------------------------------------------
# Entitäten und Kanten sammeln
# ---------------------------------------------------------------------------
nodes = {}   # entity_id -> {"label", "color", "type", "description", "source_file"}
edges = []   # (source, target, label)

def add_node(eid, platform, domain="sensor", description="", source_file=""):
    if eid not in nodes:
        nodes[eid] = {
            "label":       eid,
            "color":       color(platform, domain),
            "type":        platform,
            "description": description,
            "source_file": source_file,
        }

def add_external(eid):
    if eid and eid not in nodes:
        nodes[eid] = {
            "label":       eid,
            "color":       COLORS["external"],
            "type":        "external",
            "description": "Externe Entität (ZHA/Shelly/ESPHome/MQTT-Integration)",
            "source_file": "",
        }

def add_edge(src, tgt, label):
    add_external(src)
    if (src, tgt, label) not in edges:
        edges.append((src, tgt, label))

# ---------------------------------------------------------------------------
# Template-Referenzen extrahieren
# ---------------------------------------------------------------------------
ENTITY_RE = re.compile(
    r"states\(['\"]([a-z_]+\.[a-z0-9_]+)['\"]"
    r"|states\.([a-z_]+\.[a-z0-9_]+)\."
    r"|state_attr\(['\"]([a-z_]+\.[a-z0-9_]+)['\"]"
    r"|is_state\(['\"]([a-z_]+\.[a-z0-9_]+)['\"]"
    r"|entity_id['\"]?\s*[:=]\s*['\"]([a-z_]+\.[a-z0-9_]+)['\"]"
)

def refs_from_template(text):
    if not text:
        return []
    return [next(g for g in m.groups() if g) for m in ENTITY_RE.finditer(str(text))]

def refs_from_block(block):
    """Sammelt entity-Referenzen aus einem Template-Block (dict oder str)."""
    found = []
    if isinstance(block, str):
        found += refs_from_template(block)
    elif isinstance(block, dict):
        for v in block.values():
            found += refs_from_block(v)
    elif isinstance(block, list):
        for item in block:
            found += refs_from_block(item)
    return found

# ---------------------------------------------------------------------------
# sensors.yaml
# ---------------------------------------------------------------------------
sensors_data = load("sensors.yaml")
if sensors_data:
    entries = sensors_data if isinstance(sensors_data, list) else [sensors_data]
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        platform = entry.get("platform", "sensor")
        name = entry.get("name") or ""
        eid = f"sensor.{slugify(name)}" if name else None

        unit = entry.get("unit_of_measurement", "")
        dclass = entry.get("device_class", "")
        unit_str = f" [{unit}]" if unit else ""

        if platform == "integration":
            source = entry.get("source")
            if eid and source:
                desc = f"Integriert {source} über die Zeit → Energie{unit_str}"
                add_node(eid, "integration", description=desc, source_file="sensors.yaml")
                add_external(source)
                add_edge(source, eid, "integration")

        elif platform == "filter":
            source = entry.get("entity_id")
            filters = entry.get("filters", [])
            filter_names = ", ".join(f.get("filter", "") for f in filters if isinstance(f, dict)) if filters else ""
            if eid and source:
                desc = f"Gefilterter Wert von {source}" + (f" (Filter: {filter_names})" if filter_names else "")
                add_node(eid, "filter", description=desc, source_file="sensors.yaml")
                add_external(source)
                add_edge(source, eid, "filter")

        elif platform == "statistics":
            source = entry.get("entity_id")
            stype = entry.get("state_characteristic", "")
            if eid and source:
                desc = f"Statistik von {source}" + (f" ({stype})" if stype else "")
                add_node(eid, "statistics", description=desc, source_file="sensors.yaml")
                add_external(source)
                add_edge(source, eid, "statistics")

        elif platform == "history_stats":
            source = entry.get("entity_id")
            stype = entry.get("type", "")
            if eid and source:
                desc = f"Verlaufsstatistik von {source}" + (f" ({stype})" if stype else "")
                add_node(eid, "history_stats", description=desc, source_file="sensors.yaml")
                add_external(source)
                add_edge(source, eid, "history_stats")

        elif platform == "template":
            vt = entry.get("value_template") or entry.get("state") or ""
            vt_short = str(vt)[:120].replace("\n", " ") if vt else ""
            if eid:
                desc = f"Template-Sensor{unit_str}" + (f": {vt_short}" if vt_short else "")
                add_node(eid, "template", description=desc, source_file="sensors.yaml")
                for ref in refs_from_template(str(vt)):
                    add_external(ref)
                    add_edge(ref, eid, "template")

        elif platform == "rest":
            if eid:
                desc = f"REST-Sensor{unit_str}" + (f" [{dclass}]" if dclass else "")
                add_node(eid, "rest", description=desc, source_file="sensors.yaml")

        elif platform == "mqtt":
            topic = entry.get("state_topic", "")
            if eid:
                desc = f"MQTT-Sensor" + (f" (Topic: {topic})" if topic else "") + unit_str
                add_node(eid, "mqtt", description=desc, source_file="sensors.yaml")

        else:
            if eid:
                add_node(eid, platform, description=f"Sensor ({platform}){unit_str}", source_file="sensors.yaml")

# ---------------------------------------------------------------------------
# configuration.yaml  →  utility_meter
# ---------------------------------------------------------------------------
config_data = load("configuration.yaml")
if config_data and isinstance(config_data, dict):
    um = config_data.get("utility_meter", {}) or {}
    for key, cfg in um.items():
        if not isinstance(cfg, dict):
            continue
        source = cfg.get("source")
        cycle  = cfg.get("cycle") if isinstance(cfg.get("cycle"), str) else ""
        cycle_label = {"daily": "Tages", "monthly": "Monats", "yearly": "Jahres",
                      "hourly": "Stunden"}.get(cycle, cycle)
        eid  = f"sensor.{slugify(key)}"
        desc = f"{cycle_label}verbrauch von {source or key}" if cycle_label else f"Verbrauchszähler von {source or key}"
        add_node(eid, "utility_meter", description=desc, source_file="configuration.yaml")
        if source:
           add_external(source)
           add_edge(source, eid, "utility_meter")

    for domain in ("input_number", "input_boolean", "input_select"):
        domain_labels = {"input_number": "Zahleneingabe", "input_boolean": "Schalter (Eingabe)", "input_select": "Auswahlliste"}
        for key in (config_data.get(domain) or {}).keys():
            eid = f"{domain}.{slugify(key)}"
            add_node(eid, domain, domain,
                     description=f"{domain_labels.get(domain, domain)}: {key}",
                     source_file="configuration.yaml")

# ---------------------------------------------------------------------------
# templates.yaml
# ---------------------------------------------------------------------------
tmpl_data = load("templates.yaml")
if tmpl_data:
    entries = tmpl_data if isinstance(tmpl_data, list) else [tmpl_data]
    for block in entries:
        if not isinstance(block, dict):
            continue
        for domain in ("sensor", "binary_sensor", "switch", "number", "select"):
            for tdef in (block.get(domain) or []):
                if not isinstance(tdef, dict):
                    continue
                name = tdef.get("name") or ""
                if not name:
                    continue
                eid = f"{domain}.{slugify(name)}"
                unit = tdef.get("unit_of_measurement", "")
                state_val = tdef.get("state") or tdef.get("value_template") or ""
                state_short = str(state_val)[:120].replace("\n", " ") if state_val else ""
                unit_str = f" [{unit}]" if unit else ""
                desc = f"Template-{domain}{unit_str}" + (f": {state_short}" if state_short else "")
                add_node(eid, "template", domain, description=desc, source_file="templates.yaml")
                for ref in refs_from_block(tdef):
                    if ref != eid:
                        add_external(ref)
                        add_edge(ref, eid, "template")

# ---------------------------------------------------------------------------
# light.yaml
# ---------------------------------------------------------------------------
light_data = load("light.yaml")
if light_data:
    entries = light_data if isinstance(light_data, list) else [light_data]
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name") or ""
        platform = entry.get("platform", "")
        if name:
            eid = f"light.{slugify(name)}"
            desc = f"Licht" + (f" ({platform})" if platform else "")
            add_node(eid, "light", "light", description=desc, source_file="light.yaml")

# ---------------------------------------------------------------------------
# mqtt.yaml
# ---------------------------------------------------------------------------
mqtt_data = load("mqtt.yaml")
if mqtt_data and isinstance(mqtt_data, dict):
    for domain, items in mqtt_data.items():
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get("name") or ""
            if name:
                eid = f"{domain}.{slugify(name)}"
                topic = item.get("state_topic") or item.get("command_topic") or ""
                unit = item.get("unit_of_measurement", "")
                unit_str = f" [{unit}]" if unit else ""
                desc = f"MQTT-{domain}{unit_str}" + (f" (Topic: {topic})" if topic else "")
                add_node(eid, "mqtt", domain, description=desc, source_file="mqtt.yaml")

# ---------------------------------------------------------------------------
# climate.yaml
# ---------------------------------------------------------------------------
climate_data = load("climate.yaml")
if climate_data:
    entries = climate_data if isinstance(climate_data, list) else [climate_data]
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name") or ""
        platform = entry.get("platform", "")
        if name:
            eid = f"climate.{slugify(name)}"
            desc = f"Klimagerät" + (f" ({platform})" if platform else "")
            add_node(eid, "climate", "climate", description=desc, source_file="climate.yaml")

# ---------------------------------------------------------------------------
# rest.yaml
# ---------------------------------------------------------------------------
rest_data = load("rest.yaml")
if rest_data:
    entries = rest_data if isinstance(rest_data, list) else [rest_data]
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        for sensor in (entry.get("sensor") or []):
            if not isinstance(sensor, dict):
                continue
            name = sensor.get("name") or ""
            if name:
                eid = f"sensor.{slugify(name)}"
                unit = sensor.get("unit_of_measurement", "")
                value_tmpl = sensor.get("value_template", "")
                unit_str = f" [{unit}]" if unit else ""
                desc = f"REST-Sensor{unit_str}" + (f": {str(value_tmpl)[:80]}" if value_tmpl else "")
                add_node(eid, "rest", description=desc, source_file="rest.yaml")

# ---------------------------------------------------------------------------
# JSON für Cytoscape.js (entity-graph.html) schreiben
# ---------------------------------------------------------------------------
import json

cy_nodes = [
    {"data": {
        "id":          nid,
        "label":       nd["label"],
        "type":        nd["type"],
        "description": nd.get("description", ""),
        "source":      nd.get("source_file", ""),
    }}
    for nid, nd in nodes.items()
]
cy_edges = [
    {"data": {"source": src, "target": tgt, "label": lbl}}
    for src, tgt, lbl in edges
]
(BASE / "www").mkdir(exist_ok=True)
with open(BASE / "www" / "entities_graph.json", "w", encoding="utf-8") as f:
    json.dump({"nodes": cy_nodes, "edges": cy_edges}, f, ensure_ascii=False, indent=2)
print(f"entities_graph.json:    {len(cy_nodes)} Knoten, {len(cy_edges)} Kanten")

# ---------------------------------------------------------------------------
# Namespace-Konstanten
# ---------------------------------------------------------------------------
NS_GML = "http://graphml.graphdrawing.org/graphml"
NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
NS_Y   = "http://www.yworks.com/xml/graphml"
NS_YED = "http://www.yworks.com/xml/yed/3"

# Namespace-Präfixe registrieren – ET ergänzt dann xmlns:* automatisch,
# ohne Duplikate, wenn man Elemente mit {ns}tag-Syntax erzeugt.
ET.register_namespace("",    NS_GML)
ET.register_namespace("xsi", NS_XSI)
ET.register_namespace("y",   NS_Y)
ET.register_namespace("yed", NS_YED)

# ---------------------------------------------------------------------------
# Standard-GraphML schreiben
# ---------------------------------------------------------------------------
root = ET.Element(f"{{{NS_GML}}}graphml")
root.set(f"{{{NS_XSI}}}schemaLocation",
         f"{NS_GML} http://graphml.graphdrawing.org/graphml/1.0/graphml.xsd")

ET.SubElement(root, f"{{{NS_GML}}}key", {"id": "d_label",  "for": "node", "attr.name": "label",       "attr.type": "string"})
ET.SubElement(root, f"{{{NS_GML}}}key", {"id": "d_color",  "for": "node", "attr.name": "color",       "attr.type": "string"})
ET.SubElement(root, f"{{{NS_GML}}}key", {"id": "d_type",   "for": "node", "attr.name": "type",        "attr.type": "string"})
ET.SubElement(root, f"{{{NS_GML}}}key", {"id": "d_desc",   "for": "node", "attr.name": "Description", "attr.type": "string"})
ET.SubElement(root, f"{{{NS_GML}}}key", {"id": "d_src",    "for": "node", "attr.name": "Source",      "attr.type": "string"})
ET.SubElement(root, f"{{{NS_GML}}}key", {"id": "d_elabel", "for": "edge", "attr.name": "label",       "attr.type": "string"})

graph_el = ET.SubElement(root, f"{{{NS_GML}}}graph", {"id": "G", "edgedefault": "directed"})

for nid, nd in nodes.items():
    n = ET.SubElement(graph_el, f"{{{NS_GML}}}node", {"id": nid})
    ET.SubElement(n, f"{{{NS_GML}}}data", {"key": "d_label"}).text = nd["label"]
    ET.SubElement(n, f"{{{NS_GML}}}data", {"key": "d_color"}).text = nd["color"]
    ET.SubElement(n, f"{{{NS_GML}}}data", {"key": "d_type"}).text  = nd["type"]
    ET.SubElement(n, f"{{{NS_GML}}}data", {"key": "d_desc"}).text  = nd.get("description", "")
    ET.SubElement(n, f"{{{NS_GML}}}data", {"key": "d_src"}).text   = nd.get("source_file", "")

for i, (src, tgt, lbl) in enumerate(edges):
    e = ET.SubElement(graph_el, f"{{{NS_GML}}}edge", {"id": f"e{i}", "source": src, "target": tgt})
    ET.SubElement(e, f"{{{NS_GML}}}data", {"key": "d_elabel"}).text = lbl

ET.indent(root, space="  ")
ET.ElementTree(root).write(BASE / "entities_graph.graphml",
                           xml_declaration=True, encoding="UTF-8")
print(f"entities_graph.graphml: {len(nodes)} Knoten, {len(edges)} Kanten")

# ---------------------------------------------------------------------------
# yEd-Format erzeugen
# ---------------------------------------------------------------------------
yed_root = ET.Element(f"{{{NS_GML}}}graphml")
yed_root.set(f"{{{NS_XSI}}}schemaLocation",
             f"{NS_GML} http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd")

ET.SubElement(yed_root, f"{{{NS_GML}}}key", {"for": "node", "id": "d_node", "yfiles.type": "nodegraphics"})
ET.SubElement(yed_root, f"{{{NS_GML}}}key", {"for": "edge", "id": "d_edge", "yfiles.type": "edgegraphics"})
ET.SubElement(yed_root, f"{{{NS_GML}}}key", {"for": "node", "id": "d_type", "attr.name": "type",        "attr.type": "string"})
ET.SubElement(yed_root, f"{{{NS_GML}}}key", {"for": "node", "id": "d_desc", "attr.name": "Description", "attr.type": "string"})
ET.SubElement(yed_root, f"{{{NS_GML}}}key", {"for": "node", "id": "d_src",  "attr.name": "Source",      "attr.type": "string"})

yed_graph = ET.SubElement(yed_root, f"{{{NS_GML}}}graph", {"id": "G", "edgedefault": "directed"})

for nid, nd in nodes.items():
    new_node = ET.SubElement(yed_graph, f"{{{NS_GML}}}node", {"id": nid})
    ET.SubElement(new_node, f"{{{NS_GML}}}data", {"key": "d_type"}).text = nd["type"]
    ET.SubElement(new_node, f"{{{NS_GML}}}data", {"key": "d_desc"}).text = nd.get("description", "")
    ET.SubElement(new_node, f"{{{NS_GML}}}data", {"key": "d_src"}).text  = nd.get("source_file", "")
    data_el = ET.SubElement(new_node, f"{{{NS_GML}}}data", {"key": "d_node"})
    shape   = ET.SubElement(data_el, f"{{{NS_Y}}}ShapeNode")
    ET.SubElement(shape, f"{{{NS_Y}}}Geometry", {"height": "30.0", "width": "220.0"})
    ET.SubElement(shape, f"{{{NS_Y}}}Fill", {"color": nd["color"], "transparent": "false"})
    ET.SubElement(shape, f"{{{NS_Y}}}BorderStyle", {"color": "#888888", "type": "line", "width": "1.0"})
    nl = ET.SubElement(shape, f"{{{NS_Y}}}NodeLabel", {
        "alignment": "center", "fontFamily": "Dialog",
        "fontSize": "11", "fontStyle": "plain", "textColor": "#000000",
    })
    nl.text = nd["label"]
    ET.SubElement(shape, f"{{{NS_Y}}}Shape", {"type": "roundrectangle"})

for i, (src, tgt, lbl) in enumerate(edges):
    new_edge = ET.SubElement(yed_graph, f"{{{NS_GML}}}edge", {"id": f"e{i}", "source": src, "target": tgt})
    data_el  = ET.SubElement(new_edge, f"{{{NS_GML}}}data", {"key": "d_edge"})
    ple      = ET.SubElement(data_el, f"{{{NS_Y}}}PolyLineEdge")
    ET.SubElement(ple, f"{{{NS_Y}}}Arrows", {"source": "none", "target": "standard"})
    ET.SubElement(ple, f"{{{NS_Y}}}LineStyle", {"color": "#888888", "type": "line", "width": "1.5"})
    if lbl:
        el = ET.SubElement(ple, f"{{{NS_Y}}}EdgeLabel", {
            "alignment": "center", "fontFamily": "Dialog",
            "fontSize": "10", "textColor": "#333333",
        })
        el.text = lbl

ET.indent(yed_root, space="  ")
ET.ElementTree(yed_root).write(BASE / "entities_graph_yed.graphml",
                               xml_declaration=True, encoding="UTF-8")
print(f"entities_graph_yed.graphml: {len(nodes)} Knoten, {len(edges)} Kanten")

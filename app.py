import streamlit as st
import streamlit.components.v1 as components
import random
import json

st.set_page_config(
    page_title="KDP Warehouse Re-Slotting Map",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
  #MainMenu, footer, header { visibility: hidden; }
  .stApp { background: #111111; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  div[data-testid="stVerticalBlock"] { gap: 0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:#7B3F00;border-left:5px solid #FF9800;padding:10px 20px;
            font-family:Arial;font-size:13px;color:#FFE0B2;letter-spacing:0.03em;">
  <b>DEMO VERSION — REPRESENTATIVE DATA ONLY</b> &nbsp;|&nbsp;
  All bin locations, SKU names, outbound values, and classifications shown here are
  randomly generated and have no correlation to real KDP warehouse data or operations.
  This dashboard is a portfolio demonstration of the analytical framework built for
  Keurig Dr Pepper Sumner DC by MSBA Team 3, University of Washington Tacoma.
</div>
""", unsafe_allow_html=True)

@st.cache_data
def fetch_bins(username=None, password=None):
    """Representative demo data for the Sumner DC warehouse map."""
    return generate_demo_bins()

def generate_demo_bins():
    """Fallback demo data if Azure connection fails."""
    random.seed(42)
    PRODUCTS = [
        "KIRK KCUP FTO BOLD 120CT","KIRK KCUP FTO SUMMIT RST 120CT",
        "PEET KCUP HOUSE BL 22CT","GREEN MTN BRKFST BL 24CT",
        "DONUT SHOP REG 24CT","FOLGERS CLASSIC RST 24CT",
        "STARBUCKS PIKE PL 24CT","CARIBOU CABIN BL 24CT",
        "DUNKIN ORIG BL 22CT","KIRK COLOMBIAN 100CT",
    ]
    config = (
        [("HA","Zone 1 Prime"),("HB","Zone 1 Prime"),("HC","Zone 1 Prime"),
         ("HD","Zone 1 Prime"),("HE","Zone 1 Prime"),("HF","Zone 1 Prime"),
         ("HG","Zone 1 Prime"),("HH","Zone 1 Prime"),("HI","Zone 1 Prime"),
         ("HJ","Zone 1 Prime"),("HK","Zone 1 Prime"),("HL","Zone 1 Prime"),
         ("HM","Zone 1 Prime")] +
        [("WI","Zone 3 Cold")] +
        [("RG","Zone 2 Secondary"),("RF","Zone 2 Secondary"),("RE","Zone 2 Secondary"),
         ("RD","Zone 2 Secondary"),("RC","Zone 2 Secondary"),("RB","Zone 2 Secondary"),
         ("RA","Zone 2 Secondary")]
    )
    bins = []
    for lane, zone in config:
        for r in range(8):
            for c in range(6):
                rnd = random.random()
                if rnd < 0.48:   status = "Empty"
                elif rnd < 0.55: status = "Blocked"
                elif rnd < 0.70: status = "A"
                elif rnd < 0.85: status = "B"
                else:            status = "C"
                bins.append({
                    "id": f"{lane}{r*6+c:03d}",
                    "sku": f"5000{random.randint(100000,999999)}" if status not in ("Empty","Blocked") else "",
                    "name": random.choice(PRODUCTS) if status not in ("Empty","Blocked") else status,
                    "status": status, "lane": lane, "zone": zone,
                    "outboundValue": round(random.uniform(50000,36000000)) if status not in ("Empty","Blocked") else 0,
                    "placement": "", "row": r, "col": c
                })
    return bins

# ── Load data ─────────────────────────────────────────────────────────────────
bins = fetch_bins()
total   = len(bins)
occ     = sum(1 for b in bins if b["status"] in ("A","B","C"))
avail   = sum(1 for b in bins if b["status"] == "Empty")
blocked = sum(1 for b in bins if b["status"] == "Blocked")
cls_a   = sum(1 for b in bins if b["status"] == "A")
cls_b   = sum(1 for b in bins if b["status"] == "B")
cls_c   = sum(1 for b in bins if b["status"] == "C")
max_abc = max(cls_a, cls_b, cls_c) if max(cls_a, cls_b, cls_c) > 0 else 1

# Real KPI values from data
total_skus_assigned = sum(1 for b in bins if b["status"] in ("A","B","C") and b["sku"])
zone1_bins  = sum(1 for b in bins if b["zone"] == "Zone 1 Prime")
zone2_bins  = sum(1 for b in bins if b["zone"] == "Zone 2 Secondary")
cold_bins   = sum(1 for b in bins if b["zone"] == "Zone 3 Cold")
# Avg outbound value for Class A SKUs
class_a_vals = [b["outboundValue"] for b in bins if b["status"] == "A" and b["outboundValue"] > 0]
avg_outbound_a = sum(class_a_vals) / len(class_a_vals) if class_a_vals else 0
# Format avg outbound
if avg_outbound_a >= 1_000_000:
    avg_outbound_str = f"${avg_outbound_a/1_000_000:.1f}M"
elif avg_outbound_a >= 1_000:
    avg_outbound_str = f"${avg_outbound_a/1_000:.0f}K"
else:
    avg_outbound_str = f"${avg_outbound_a:.0f}"

bins_json = json.dumps(bins)

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; font-family:Arial,sans-serif; }}
body {{ background:#111111; color:white; height:820px; overflow:hidden; display:flex; flex-direction:column; }}
.header {{ background:#443738; padding:7px 18px; display:flex; align-items:center; justify-content:space-between; flex-shrink:0; }}
.header-title {{ font-size:13px; font-weight:600; letter-spacing:0.04em; }}
.filter-select {{ background:#2A2A2A; border:1px solid #444; color:white; padding:4px 8px; border-radius:4px; font-size:11px; }}
.kpi-row {{ display:flex; gap:10px; padding:8px 16px; justify-content:center; background:#111; flex-shrink:0; }}
.kpi-card {{ background:#1E1E1E; border:1px solid #333; border-radius:8px; padding:10px 22px; text-align:center; }}
.kpi-value {{ font-size:26px; font-weight:700; }}
.kpi-label {{ font-size:10px; color:rgba(255,255,255,0.45); text-transform:uppercase; letter-spacing:0.08em; margin-top:3px; }}
.search-row {{ display:flex; gap:10px; padding:4px 14px; flex-shrink:0; }}
.search-box {{ display:flex; align-items:center; gap:6px; background:#1E1E1E; border:1px solid #333; border-radius:6px; padding:5px 10px; width:240px; }}
.search-box input {{ background:transparent; border:none; outline:none; color:white; font-size:11px; width:100%; }}
.search-box input::placeholder {{ color:rgba(255,255,255,0.3); }}
.main {{ display:flex; flex:1; min-height:0; }}
.left-panel {{ flex:1; display:flex; flex-direction:column; padding:4px 8px; min-width:0; overflow:hidden; }}
.right-panel {{ width:285px; flex-shrink:0; background:#1A1A1A; display:flex; flex-direction:column; gap:8px; padding:4px 10px 10px 10px; overflow-y:auto; }}
.bin-grid-area {{ flex:1; overflow-y:auto; overflow-x:hidden; }}
.lanes-container {{ display:flex; flex-direction:column; gap:4px; padding:2px; }}
.zone-row-block {{ display:flex; flex-direction:column; gap:2px; }}
.zone-row-label {{ font-size:8px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; padding:1px 4px; }}
.zone-lanes {{ display:flex; gap:3px; flex-wrap:nowrap; align-items:flex-start; overflow-x:auto; padding-bottom:3px; }}
.zone-lanes::-webkit-scrollbar {{ height:4px; }}
.zone-lanes::-webkit-scrollbar-track {{ background:#1A1A1A; }}
.zone-lanes::-webkit-scrollbar-thumb {{ background:#333; border-radius:2px; }}
.zone-group {{ display:flex; gap:3px; }}
.wi-cold-label {{ font-size:9px; color:#3FC7F2; font-weight:600; text-align:center; margin-bottom:2px; }}
.lane-cluster {{ display:flex; flex-direction:column; align-items:center; }}
.lane-name {{ font-size:7px; color:rgba(255,255,255,0.55); margin-bottom:1px; font-weight:600; }}
.lane-grid {{ padding:3px; border-radius:3px; display:grid; gap:2px; }}
.bin {{ width:10px; height:10px; border-radius:1px; cursor:pointer; transition:transform 0.1s; }}
.bin:hover {{ transform:scale(1.7); z-index:999; }}
.floor-plan {{ background:#151515; border:1px solid #2A2A2A; border-radius:6px; overflow:hidden; margin-top:4px; flex-shrink:0; }}
.fp-header {{ padding:3px 12px; border-bottom:1px solid #2A2A2A; font-size:9px; color:rgba(255,255,255,0.35); letter-spacing:0.1em; }}
.sidebar-card {{ background:#1E1E1E; border:1px solid #2A2A2A; border-radius:8px; padding:12px; flex-shrink:0; }}
.sidebar-title {{ font-size:11px; font-weight:600; color:rgba(255,255,255,0.45); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:10px; }}
.metrics-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
.metric-value {{ font-size:22px; font-weight:700; }}
.metric-label {{ font-size:9px; color:rgba(255,255,255,0.35); text-transform:uppercase; letter-spacing:0.06em; margin-top:2px; }}
.zone-hdr {{ display:grid; grid-template-columns:1.8fr 1fr 1fr 1fr 1fr; font-size:8px; color:rgba(255,255,255,0.3); text-transform:uppercase; padding:2px 3px; margin-bottom:3px; }}
.zone-row {{ display:grid; grid-template-columns:1.8fr 1fr 1fr 1fr 1fr; font-size:11px; padding:5px 4px; border-radius:3px; }}
.zone-row:hover {{ background:#2A2A2A; }}
.donut-wrap {{ position:relative; height:160px; display:flex; align-items:center; justify-content:center; }}
.donut-center {{ position:absolute; text-align:center; pointer-events:none; }}
.donut-legend {{ display:flex; justify-content:center; gap:12px; margin-top:8px; }}
.dl-item {{ display:flex; align-items:center; gap:5px; font-size:11px; color:rgba(255,255,255,0.55); }}
.dl-dot {{ width:7px; height:7px; border-radius:50%; }}
.abc-row {{ display:flex; align-items:center; gap:6px; margin-bottom:6px; }}
.abc-lbl {{ font-size:11px; width:12px; font-weight:600; }}
.abc-track {{ flex:1; background:#2A2A2A; border-radius:3px; height:14px; overflow:hidden; }}
.abc-fill {{ height:100%; border-radius:3px; }}
.abc-cnt {{ font-size:9px; color:rgba(255,255,255,0.45); width:24px; text-align:right; }}
.legend-row {{ display:flex; flex-wrap:wrap; gap:4px; }}
.legend-item {{ display:flex; align-items:center; gap:4px; font-size:10px; color:rgba(255,255,255,0.65); }}
.legend-sq {{ width:10px; height:10px; border-radius:2px; }}
.footer {{ background:#443738; padding:3px 18px; text-align:center; font-size:9px; color:rgba(255,255,255,0.55); letter-spacing:0.04em; flex-shrink:0; }}
.tooltip {{ display:none; position:fixed; z-index:9999; background:#1E1E1E; border:1px solid #555; border-radius:8px; padding:10px 13px; font-size:11px; pointer-events:none; min-width:195px; box-shadow:0 4px 20px rgba(0,0,0,0.6); }}
.tt-name {{ font-weight:700; font-size:12px; margin-bottom:6px; }}
.tt-row {{ display:flex; justify-content:space-between; gap:14px; color:rgba(255,255,255,0.55); margin:2px 0; }}
.tt-val {{ color:white; }}
</style>
</head>
<body>

<div class="header">
  <span class="header-title">KEURIG DR PEPPER | SUMNER DC — WAREHOUSE RE-SLOTTING MAP | MSBA TEAM 3</span>
  <div style="display:flex;align-items:center;gap:12px;">
    <span style="font-size:10px;color:rgba(255,255,255,0.4);">Last Refresh: Q1 2026 &nbsp;|&nbsp; 2658 Bins</span>
    <select class="filter-select" onchange="filterBins()"><option>ABC: All</option><option>A</option><option>B</option><option>C</option></select>
    <select class="filter-select" onchange="filterBins()"><option>Zone: All</option><option>Zone 1 Prime</option><option>Zone 2 Secondary</option><option>Zone 3 Cold</option></select>
    <select class="filter-select" onchange="filterBins()"><option>Status: All</option><option>Assigned</option><option>Available</option><option>Blocked</option></select>
  </div>
</div>

<div class="kpi-row">
  <div class="kpi-card"><div class="kpi-value" style="color:white">{total_skus_assigned}</div><div class="kpi-label">Total SKUs Assigned</div></div>
  <div class="kpi-card"><div class="kpi-value" style="color:#7AC143">{zone1_bins}</div><div class="kpi-label">Zone 1 Prime Bins</div></div>
  <div class="kpi-card"><div class="kpi-value" style="color:#925041">{zone2_bins}</div><div class="kpi-label">Zone 2 Secondary Bins</div></div>
  <div class="kpi-card"><div class="kpi-value" style="color:#3FC7F2">{cold_bins}</div><div class="kpi-label">Cold Zone Bins</div></div>
  <div class="kpi-card"><div class="kpi-value" style="color:#CE0954">{avg_outbound_str}</div><div class="kpi-label">Avg Outbound (Class A)</div></div>
</div>

<div class="search-row">
  <div class="search-box"><span style="color:rgba(255,255,255,0.35);font-size:13px">&#128269;</span><input type="text" id="searchSku" placeholder="Search by SKU ID..." oninput="filterBins()"/></div>
  <div class="search-box"><span style="color:rgba(255,255,255,0.35);font-size:13px">&#128269;</span><input type="text" id="searchName" placeholder="Search by Name..." oninput="filterBins()"/></div>
</div>

<div class="main">
  <div class="left-panel">
    <div class="bin-grid-area">
      <div class="lanes-container" id="lanesContainer"></div>
    </div>
    <div class="floor-plan">
      <div class="fp-header">SUMNER DC — WAREHOUSE FLOOR PLAN</div>
      <svg viewBox="0 0 980 168" style="width:100%;height:280px;display:block;">
        <rect width="980" height="168" fill="#111111"/>
        <rect x="30"  y="4" width="55"  height="13" fill="#CE0954" rx="2"/>
        <text x="57"  y="13" fill="white" font-size="7" text-anchor="middle" font-weight="bold">Hot 23-26</text>
        <rect x="92"  y="4" width="148" height="13" fill="#7AC143" rx="2"/>
        <text x="166" y="13" fill="#111" font-size="7" text-anchor="middle" font-weight="bold">FG Inbound  Doors 14-22</text>
        <rect x="500" y="4" width="55"  height="13" fill="#3FC7F2" rx="2"/>
        <text x="527" y="13" fill="#111" font-size="7" text-anchor="middle" font-weight="bold">Cold 5-6</text>
        <rect x="15"  y="23" width="300" height="120" fill="#0D2B0D" stroke="#7AC143" stroke-width="2" rx="5"/>
        <text x="165" y="46" fill="#7AC143" font-size="13" text-anchor="middle" font-weight="bold">ZONE 1 PRIME</text>
        <text x="165" y="60" fill="#7AC143" font-size="9"  text-anchor="middle">Lanes HA-HM, WE, WG</text>
        <text x="28"  y="84" fill="#7AC143" font-size="8">HA  HB  HC  HD  HE  HF  HG</text>
        <text x="28"  y="99" fill="#7AC143" font-size="8">HH  HI  HJ  HK  HL  HM  WE  WG</text>
        <rect x="323" y="23" width="85"  height="65"  fill="#2B1A08" stroke="#CE0954" stroke-width="2" rx="5"/>
        <text x="365" y="50" fill="#CE0954" font-size="10" text-anchor="middle" font-weight="bold">DR FLEX</text>
        <text x="365" y="64" fill="#CE0954" font-size="8"  text-anchor="middle">Shipping</text>
        <rect x="416" y="23" width="140" height="75"  fill="#082228" stroke="#3FC7F2" stroke-width="2" rx="5"/>
        <text x="486" y="56" fill="#3FC7F2" font-size="13" text-anchor="middle" font-weight="bold">ZONE 3 COLD</text>
        <text x="486" y="71" fill="#3FC7F2" font-size="9"  text-anchor="middle">WI</text>
        <rect x="564" y="23" width="240" height="120" fill="#2B1208" stroke="#925041" stroke-width="2" rx="5"/>
        <text x="684" y="46" fill="#925041" font-size="13" text-anchor="middle" font-weight="bold">ZONE 2 SECONDARY</text>
        <text x="684" y="60" fill="#925041" font-size="9"  text-anchor="middle">Lanes RG-RA, RH, V</text>
        <text x="578" y="84" fill="#925041" font-size="8">RG  RF  RE  RD  RC  RB  RA  RH  V</text>
        <rect x="812" y="23" width="152" height="120" fill="#151515" stroke="#2A2A2A" stroke-width="2" rx="5"/>
        <text x="888" y="78"  fill="#444" font-size="12" text-anchor="middle" font-weight="bold">ZONE 4</text>
        <text x="888" y="93"  fill="#444" font-size="10" text-anchor="middle">MFG</text>
        <text x="888" y="107" fill="#333" font-size="8"  text-anchor="middle">(Excluded)</text>
        <rect x="15"  y="149" width="210" height="13" fill="#7AC143" rx="2"/>
        <text x="120" y="158" fill="#111" font-size="7" text-anchor="middle" font-weight="bold">FG Outbound  Doors 29-44</text>
        <rect x="580" y="152" width="9" height="9" fill="#7AC143" rx="1"/>
        <text x="593" y="159" fill="#555" font-size="8">FG Inbound</text>
        <rect x="658" y="152" width="9" height="9" fill="#CE0954" rx="1"/>
        <text x="671" y="159" fill="#555" font-size="8">Hot Shipping</text>
        <rect x="745" y="152" width="9" height="9" fill="#3FC7F2" rx="1"/>
        <text x="758" y="159" fill="#555" font-size="8">Cold IB/OB</text>
      </svg>
    </div>
  </div>

  <div class="right-panel">
    <div class="sidebar-card">
      <div class="sidebar-title">Key Metrics</div>
      <div class="metrics-grid">
        <div><div class="metric-value" style="color:white">{total:,}</div><div class="metric-label">Total Bins</div></div>
        <div><div class="metric-value" style="color:#925041">{occ/total*100:.1f}%</div><div class="metric-label">Occupied</div></div>
        <div><div class="metric-value" style="color:#7AC143">{avail/total*100:.1f}%</div><div class="metric-label">Available</div></div>
        <div><div class="metric-value" style="color:#CE0954">{blocked/total*100:.1f}%</div><div class="metric-label">Blocked</div></div>
      </div>
    </div>

    <div class="sidebar-card">
      <div class="sidebar-title">Zone Breakdown</div>
      <div class="zone-hdr"><span>Location</span><span>Free</span><span>Occ</span><span>Blk</span><span>Tot</span></div>
      <div id="zoneTable"></div>
    </div>

    <div class="sidebar-card">
      <div class="sidebar-title">Bin Status Distribution</div>
      <div class="donut-wrap">
        <canvas id="donutChart" width="140" height="140"></canvas>
        <div class="donut-center">
          <div style="font-size:22px;font-weight:700">{total:,}</div>
          <div style="font-size:9px;color:rgba(255,255,255,0.4)">Total</div>
        </div>
      </div>
      <div class="donut-legend">
        <div class="dl-item"><div class="dl-dot" style="background:#925041"></div>Occupied</div>
        <div class="dl-item"><div class="dl-dot" style="background:#7AC143"></div>Available</div>
        <div class="dl-item"><div class="dl-dot" style="background:#CE0954"></div>Blocked</div>
      </div>
    </div>

    <div class="sidebar-card">
      <div class="sidebar-title">ABC Class Breakdown</div>
      <div class="abc-row">
        <span class="abc-lbl" style="color:#FF3333">A</span>
        <div class="abc-track"><div class="abc-fill" style="background:#FF3333;width:{cls_a/max_abc*100:.0f}%"></div></div>
        <span class="abc-cnt">{cls_a}</span>
      </div>
      <div class="abc-row">
        <span class="abc-lbl" style="color:#33CC33">B</span>
        <div class="abc-track"><div class="abc-fill" style="background:#33CC33;width:{cls_b/max_abc*100:.0f}%"></div></div>
        <span class="abc-cnt">{cls_b}</span>
      </div>
      <div class="abc-row">
        <span class="abc-lbl" style="color:#00BBFF">C</span>
        <div class="abc-track"><div class="abc-fill" style="background:#00BBFF;width:{cls_c/max_abc*100:.0f}%"></div></div>
        <span class="abc-cnt">{cls_c}</span>
      </div>
    </div>

    <div class="sidebar-card">
      <div class="sidebar-title">Location Status</div>
      <div class="legend-row">
        <div class="legend-item"><div class="legend-sq" style="background:#FF3333"></div>Class A</div>
        <div class="legend-item"><div class="legend-sq" style="background:#33CC33"></div>Class B</div>
        <div class="legend-item"><div class="legend-sq" style="background:#00BBFF"></div>Class C</div>
        <div class="legend-item"><div class="legend-sq" style="background:#2A2A2A;border:1px solid #555"></div>Empty</div>
        <div class="legend-item"><div class="legend-sq" style="background:#886600"></div>Blocked</div>
      </div>
    </div>
  </div>
</div>

<div class="footer">KEURIG DR PEPPER | SUMNER DC — 224,000 SQ FT | MSBA TEAM 3 — UW TACOMA | REPRESENTATIVE LAYOUT — COORDINATES APPROXIMATED</div>

<div class="tooltip" id="tooltip">
  <div class="tt-name" id="tt-name"></div>
  <div class="tt-row"><span>SKU:</span><span class="tt-val" id="tt-sku"></span></div>
  <div class="tt-row"><span>ABC:</span><span class="tt-val" id="tt-abc"></span></div>
  <div class="tt-row"><span>Lane:</span><span class="tt-val" id="tt-lane"></span></div>
  <div class="tt-row"><span>Zone:</span><span class="tt-val" id="tt-zone"></span></div>
  <div class="tt-row"><span>Outbound:</span><span class="tt-val" id="tt-val"></span></div>
</div>

<script>
const BINS = {bins_json};
const COLORS = {{A:"#FF3333",B:"#33CC33",C:"#00BBFF",Empty:"#2A2A2A",Blocked:"#886600"}};
const ZONES  = {{
  "Zone 1 Prime":    {{bg:"#2B1208",border:"#925041"}},
  "Zone 2 Secondary":{{bg:"#0D2B0D",border:"#7AC143"}},
  "Zone 3 Cold":     {{bg:"#082228",border:"#3FC7F2"}},
}};
const LEFT  = ["HA","HB","HC","HD","HE","HF","HG","HH","HI","HJ","HK","HL","HM"];
const COLD  = ["WI"];
const RIGHT = ["RG","RF","RE","RD","RC","RB","RA"];

let currentBins = BINS;

function makeLane(lane, zone) {{
  const bins = currentBins.filter(b => b.lane === lane);
  const z = ZONES[zone] || {{bg:"#1A1A1A",border:"#333"}};
  const cols = 6;
  const wrap = document.createElement("div"); wrap.className = "lane-cluster";
  const nm = document.createElement("div"); nm.className = "lane-name"; nm.textContent = lane;
  wrap.appendChild(nm);
  const grid = document.createElement("div"); grid.className = "lane-grid";
  grid.style.cssText = `background:${{z.bg}};border:1px solid ${{z.border}};grid-template-columns:repeat(${{cols}},10px);gap:2px;padding:4px;`;
  bins.forEach(bin => {{
    const sq = document.createElement("div"); sq.className = "bin";
    sq.style.background = COLORS[bin.status] || "#2A2A2A";
    sq.addEventListener("mouseenter", e => showTT(bin, e));
    sq.addEventListener("mouseleave", hideTT);
    grid.appendChild(sq);
  }});
  wrap.appendChild(grid);
  return wrap;
}}

function makeZoneRow(title, color, lanes, zone) {{
  const block = document.createElement("div"); block.className = "zone-row-block";
  const lbl = document.createElement("div"); lbl.className = "zone-row-label";
  lbl.style.color = color; lbl.textContent = title; block.appendChild(lbl);
  const row = document.createElement("div"); row.className = "zone-lanes";
  lanes.forEach(l => row.appendChild(makeLane(l, zone))); block.appendChild(row);
  return block;
}}

function buildGrid() {{
  const c = document.getElementById("lanesContainer"); c.innerHTML = "";
  c.appendChild(makeZoneRow("Zone 1 — Prime  |  HA–HM, WE, WG", "#925041", LEFT, "Zone 1 Prime"));
  c.appendChild(makeZoneRow("Zone 2 — Secondary  |  RG–RA, RH, V", "#7AC143", RIGHT, "Zone 2 Secondary"));
  c.appendChild(makeZoneRow("Zone 3 — Cold  |  WI", "#3FC7F2", COLD, "Zone 3 Cold"));
}}

function buildZoneTable() {{
  const tbl = document.getElementById("zoneTable"); tbl.innerHTML = "";
  [["Zone 1 Prime","Z1 Prime"],["Zone 2 Secondary","Z2 Secondary"],["Zone 3 Cold","Z3 Cold"],["DR Flex","DR Flex"]].forEach(([zone,label]) => {{
    const zb = BINS.filter(b => b.zone === zone);
    const free = zb.filter(b => b.status === "Empty").length;
    const occ  = zb.filter(b => ["A","B","C"].includes(b.status)).length;
    const blk  = zb.filter(b => b.status === "Blocked").length;
    const tot  = zb.length || 100;
    const row = document.createElement("div"); row.className = "zone-row";
    row.innerHTML = `<span style="color:rgba(255,255,255,0.8)">${{label}}</span><span style="color:#7AC143;text-align:center">${{free}}</span><span style="color:#925041;text-align:center">${{occ}}</span><span style="color:#CE0954;text-align:center">${{blk}}</span><span style="color:rgba(255,255,255,0.4);text-align:center">${{tot}}</span>`;
    tbl.appendChild(row);
  }});
}}

function drawDonut() {{
  const canvas = document.getElementById("donutChart");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const data = [{occ},{avail},{blocked}];
  const colors = ["#925041","#7AC143","#CE0954"];
  const total = data.reduce((a,b)=>a+b,0);
  let angle = -Math.PI/2;
  data.forEach((val, i) => {{
    const slice = (val/total)*2*Math.PI;
    ctx.beginPath(); ctx.moveTo(70,70);
    ctx.arc(70,70,65,angle,angle+slice); ctx.closePath();
    ctx.fillStyle = colors[i]; ctx.fill();
    angle += slice;
  }});
  ctx.beginPath(); ctx.arc(70,70,45,0,2*Math.PI);
  ctx.fillStyle = "#1E1E1E"; ctx.fill();
}}

function showTT(bin, e) {{
  const tt = document.getElementById("tooltip");
  document.getElementById("tt-name").textContent = bin.name;
  document.getElementById("tt-sku").textContent  = bin.sku || "-";
  document.getElementById("tt-abc").textContent  = bin.status;
  document.getElementById("tt-abc").style.color  = COLORS[bin.status];
  document.getElementById("tt-lane").textContent = bin.lane;
  document.getElementById("tt-zone").textContent = bin.zone;
  document.getElementById("tt-val").textContent  = bin.outboundValue ? "$" + bin.outboundValue.toLocaleString() : "-";
  tt.style.display = "block";
  tt.style.left = (e.clientX + 14) + "px";
  tt.style.top  = (e.clientY - 10) + "px";
}}

function hideTT() {{ document.getElementById("tooltip").style.display = "none"; }}

function filterBins() {{
  const skuQ  = document.getElementById("searchSku").value.toLowerCase();
  const nameQ = document.getElementById("searchName").value.toLowerCase();
  currentBins = BINS.filter(b => {{
    if (skuQ  && !b.sku.toLowerCase().includes(skuQ))   return false;
    if (nameQ && !b.name.toLowerCase().includes(nameQ)) return false;
    return true;
  }});
  buildGrid();
}}

buildGrid();
buildZoneTable();
window.addEventListener("load", drawDonut);
</script>
</body>
</html>"""

components.html(html, height=820, scrolling=False)

from sheets import *

fig, frame = new_sheet("L-401", "Planting plan", "Graphic only — see plant schedule",
    notes=("1. Deer-resistant palette; adjust to\n   your USDA hardiness zone.\n"
           "2. Beds: 3\" shredded hardwood mulch\n   over amended topsoil, 12\" deep.\n"
           "3. Protect the swing tree: fence at the\n   drip line before digging; arborist to\n   review cuts near its roots.\n"
           "4. Drip irrigation zone for all new\n   beds (optional, price as alternate).\n"
           "5. Lawn: restore all disturbed lawn\n   with sod to match existing.\n"
           "6. Quantities approximate; designer to\n   finalize after layout is staked."))
ax = plan_axes(fig, (-66, 66), (-82, 34))
base_context(ax)
site_steps(ax); site_walls(ax); pavilion_outline(ax, roof=False)
SPECIES = {"PV": ("#7A8F3E", 1.5), "SY": ("#8E87B8", 1.3), "NW": ("#9A8FC9", 0.9), "IG": ("#2F5E3A", 1.5),
           "BX": ("#3F7A47", 1.2), "HP": ("#D9D2A6", 1.8), "CK": ("#B8A46A", 1.0), "LV": ("#A796D6", 0.8)}
counts = {k: 0 for k in SPECIES}
def plant(x, y, k):
    c, r = SPECIES[k]
    ax.add_patch(Circle((x, y), r, fc=c, ec=INK, lw=0.5, alpha=0.9, zorder=15)); counts[k] += 1
def along(pts, k, spacing, off=0.0, side="left"):
    ln = LineString(pts)
    if off: ln = ln.parallel_offset(off, side)
    n = max(1, int(ln.length // spacing))
    for i in range(n):
        p = ln.interpolate((i + 0.5) * ln.length / n); plant(p.x, p.y, k)
def bed(poly_pts, label):
    P(ax, poly_pts, fc="#E6DCC6", ec=PLANT, lw=0.8, z=3)
    c = np.mean(poly_pts, axis=0); T(ax, c[0], c[1], label, size=5.8, color=PLANT, weight="bold", z=16)

# B1: behind pavilion back wall (lawn side)
b1 = LineString([W(-37.5, 2.0), W(-2.5, 2.0)]).buffer(2.6, cap_style=2)
G(ax, b1, fc="#E6DCC6", ec=PLANT, lw=0.8, z=3)
along([W(-36, 2.6), W(-4, 2.6)], "PV", 3.2); along([W(-35, 4.4), W(-5, 4.4)], "SY", 4.0)
# B2: along curved wall top (outside)
b2 = LineString(NEW_CURVE_A).buffer(2.2, cap_style=2).difference(PAVE)
G(ax, b2, fc="#E6DCC6", ec=PLANT, lw=0.8, z=3)
along(NEW_CURVE_A, "PV", 3.4, off=1.8, side="right"); along(NEW_CURVE_A, "NW", 2.4, off=3.3, side="right")
# B3 foundation beds
for x0, x1 in ((0.5, 6), (13.5, 26)):
    P(ax, [(x0, -3), (x1, -3), (x1, -0.2), (x0, -0.2)], fc="#E6DCC6", ec=PLANT, lw=0.8, z=3)
for x in (2.0, 4.5): plant(x, -1.6, "IG")
for x in np.arange(15, 25.5, 2.6): plant(x, -1.6, "IG")
for x in np.arange(14.5, 25.5, 2.0): plant(x, -2.6, "NW") if False else None
# B4 raised bed at walk
P(ax, [(26.8, -12), (35.5, -12), (35.5, -6), (34, -6), (34, 0), (26.8, 0)], fc="#E6DCC6", ec=PLANT, lw=0.8, z=3)
for (x, y) in [(29, -2), (31.5, -2), (29, -5), (31.5, -5), (29, -8), (31.5, -8), (33.5, -9.5)]: plant(x, y, "CK")
for (x, y) in [(28, -10.6), (30, -10.6), (32, -10.6), (34, -10.6), (28, -0.9)]: plant(x, y, "LV")
# B5 AC screen
P(ax, [(-12.8, 2.4), (-10, 2.4), (-10, 13), (-12.8, 13)], fc="#E6DCC6", ec=PLANT, lw=0.8, z=3)
for y in (3.8, 6.6, 9.4, 12.0): plant(-11.4, y, "IG")
# boxwood at stair cheeks + hydrangea at pavilion outer corners
for (x, y) in [(5.0, 1.2), (14.5, 1.2), (24.6, -11.0), (24.6, -22.0), (-10.8, 0.4), (-3.3, 0.4)]: plant(x, y, "BX")
for p in (W(-39.5, 3.5), W(-39.5, -24.5)): plant(p[0], p[1], "HP")
# swing tree protection
ax.add_patch(Circle((-37, 16), 13, fc="none", ec=PLANT, lw=1.0, ls=(0, (5, 3)), zorder=4))
ax.add_patch(Circle((-37, 16), 0.9, fc="#6F5B45", ec="none", zorder=4))
T(ax, -37, 30.5, "existing swing tree to remain\ntree protection fence at drip line", size=5.8, color=PLANT)
for lbl, (x, y) in {"B1": W(-20, 6.8), "B2": (-40, -36), "B3": (19, -4.4), "B4": (31, -6.5), "B5": (-14.8, 8)}.items():
    T(ax, x, y, lbl, size=6.2, weight="bold", color=PLANT)
north_arrow_local(ax, 58, 22)
names = {"PV": "Panicum virgatum 'Northwind'", "SY": "Salvia yangii 'Denim 'n Lace'", "NW": "Nepeta 'Walker's Low'",
         "IG": "Ilex glabra 'Shamrock'", "BX": "Buxus 'Green Velvet'", "HP": "Hydrangea pan. 'Little Lime'",
         "CK": "Calamagrostis 'Karl Foerster'", "LV": "Lavandula 'Phenomenal'"}
txt = "PLANT KEY            qty\n" + "\n".join(f"{k}  {names[k]:<30}{counts[k]:>3}" for k in SPECIES)
frame.text(0.6, 2.45, txt, fontsize=6.3, family="DejaVu Sans Mono", color=INK, va="top", bbox=dict(fc="white", ec=INK, lw=0.6, pad=5))
for i, k in enumerate(SPECIES):
    pass
print(counts)
fig.savefig("L-401.png", facecolor=PAPER); print("ok")

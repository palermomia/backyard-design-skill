from sheets import *
fig, frame = new_sheet("L-601", "Construction details\n(typical, for bidding)", "Details not to scale",
    notes=("1. Typical sections for pricing only.\n   Engineer to size footings, rebar,\n   wall reinforcement and drainage.\n"
           "2. Frost depth: footings bear at least\n   local frost depth (often 36\"\n   in the northeast US).\n"
           "3. Bluestone: 1-1/2\" thermal or natural\n   cleft, mortar-set on 4\" reinforced\n   slab over 4\"–6\" compacted gravel.\n"
           "4. Risers 6\"–7\", treads 12\"–14\";\n   keep all risers in a flight equal.\n"
           "5. Walls over 4 ft exposed height\n   require engineered design and permit."))
def box_(ax, x0, y0, x1, y1, fc, hatch=None, z=2, ec=INK):
    P(ax, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fc=fc, ec=ec, lw=0.8, z=z, hatch=hatch)
def lead(ax, xy, txy, s):
    ax.annotate(s, xy=xy, xytext=txy, fontsize=5.8, color=INK, va="center", bbox=dict(fc="white", ec="none", pad=1.2),
                arrowprops=dict(arrowstyle="-", color=MID, lw=0.5), zorder=30)
def panel(rect, title, xl, yl):
    a = fig.add_axes(rect); a.set_axis_off(); a.set_aspect("equal"); a.set_xlim(*xl); a.set_ylim(*yl)
    a.text(xl[0], yl[1] - 0.5, title, fontsize=7.5, weight="bold", color=INK, va="top")
    return a
SOIL, GRAV, CONC, BS = "#E8DFCC", "#D9D6CF", "#D3D1CC", "#9FB0BC"
# 1 patio section
a = panel([0.03, 0.55, 0.36, 0.40], "1  BLUESTONE PATIO ON SLAB", (0, 40), (0, 24))
box_(a, 2, 2, 38, 8, SOIL, "..."); box_(a, 2, 8, 38, 13, GRAV, "oo"); box_(a, 2, 13, 38, 17, CONC, "//")
box_(a, 2, 17, 38, 17.6, "#BDB7AC"); box_(a, 2, 17.6, 38, 19.1, BS)
for x in range(6, 38, 7): L(a, [(x, 17.6), (x, 19.1)], lw=0.6)
lead(a, (30, 18.4), (30, 22), "1-1/2\" bluestone, 3/8\" mortar joints")
lead(a, (24, 17.3), (24, 21), "1\" mortar setting bed")
lead(a, (18, 15), (12, 21), "4\" concrete slab, wire mesh")
lead(a, (10, 10.5), (3, 21), "4\"-6\" compacted 3/4\" gravel")
a.text(20, 4, "compacted subgrade", fontsize=5.8, ha="center", bbox=dict(fc="white", ec="none", pad=1))
a.text(20, 0.5, "pitch 1/8\"–1/4\" per ft away from house", fontsize=5.8, ha="center", color=MID)
# 2 retaining wall
a = panel([0.40, 0.48, 0.36, 0.47], "2  FIELDSTONE RETAINING WALL (W1–W4)", (0, 40), (0, 34))
box_(a, 6, 2, 22, 6, CONC, "//")
box_(a, 9, 6, 17, 22, "#A39C90", "xx")
box_(a, 8.3, 22, 18, 23.4, BS)
P(a, [(17, 6), (17, 26), (38, 26), (38, 6)], fc=SOIL, ec="none", z=1, hatch="...")
box_(a, 17, 6, 22, 21, GRAV, "oo", z=2)
a.add_patch(Circle((20, 7.5), 1.0, fc="white", ec=BLUE, lw=1.2, zorder=4))
box_(a, 0, 8, 9, 9, BS); box_(a, 0, 6, 9, 8, CONC, "//")
L(a, [(17, 23.4), (38, 26)], lw=0.8)
lead(a, (13, 22.7), (24, 31), "2\" bluestone cap, 2\" overhang")
lead(a, (12, 14), (24, 29), "fieldstone veneer on CMU core\n(or dry-laid boulder, engineer)")
lead(a, (19.5, 15), (26, 17), "12\" clean stone drainage zone\n+ filter fabric")
lead(a, (20, 7.5), (26, 9.5), "4\" perforated pipe to outlet")
lead(a, (14, 4), (24, 2), "footing 36\" min. below grade")
a.text(2, 11, "patio side", fontsize=5.8, color=MID); a.text(30, 23, "lawn side", fontsize=5.8, color=MID, bbox=dict(fc="white", ec="none", pad=1))
dimline(a, (5.5, 9), (5.5, 23.4), "max 4'-0\" exposed\n(taller = engineered)", off=1.0, size=5.4)
# 3 steps with side wall
a = panel([0.03, 0.06, 0.36, 0.46], "3  BLUESTONE STEPS WITH CAPPED SIDE WALL", (0, 40), (0, 30))
P(a, [(4, 4), (30, 4), (30, 6.2)], fc="none", ec="none")
pts = [(4, 4)]
for i in range(4):
    x = 6 + i * 6; y = 4 + i * 2.2
    box_(a, x, 2, x + 6.6, y + 2.2, CONC, "//", z=2)
    box_(a, x - 0.3, y + 2.2, x + 6.6, y + 2.8, BS, z=3)
box_(a, 30, 2, 38, 13.6, CONC, "//"); box_(a, 30, 13.6, 38, 14.2, BS, z=3)
box_(a, 2, 4.0, 6, 4.6, BS, z=3)
P(a, [(4, 7), (31, 17), (31, 19), (4, 9)], fc="none", ec=RED, lw=1.0, z=5, hatch=None)
lead(a, (17, 13), (8, 24), "capped fieldstone side wall each\nside of flight, about 30\" above nosing")
lead(a, (13, 9.5), (17, 26), "2\" bluestone tread, 1\" overhang")
lead(a, (9, 6), (28, 24), "riser 6\"-7\" (equal), tread 12\"-14\"")
a.text(4, 1, "lower patio", fontsize=5.8, color=MID); a.text(31, 15.2, "walkway (+2'-6\")", fontsize=5.8, color=MID)
# 4 column base
a = panel([0.40, 0.06, 0.36, 0.40], "4  PAVILION COLUMN BASE", (0, 40), (0, 30))
box_(a, 12, 1, 28, 4, CONC, "//"); box_(a, 15, 4, 25, 6, CONC, "//")
box_(a, 14.5, 6, 25.5, 16, "#A39C90", "xx"); box_(a, 14, 16, 26, 17, BS)
box_(a, 18, 17, 22, 28, "white")
L(a, [(20, 2), (20, 26)], color=MID, lw=0.6, ls=(0, (4, 2)))
lead(a, (20, 22), (28, 25), "10\" sq. PVC-wrapped post\nover 6x6 PT or steel");
lead(a, (25, 16.5), (29, 19), "thermal bluestone cap")
lead(a, (25, 11), (29, 12), "24\" fieldstone base, 36\" high")
lead(a, (21, 5), (29, 6), "post base on concrete pier")
lead(a, (26, 2.5), (29, 2.5), "spread footing below frost\n(size by engineer)")
fig.savefig("L-601.png", facecolor=PAPER); print("ok")

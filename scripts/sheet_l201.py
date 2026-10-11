from sheets import *

fig, frame = new_sheet("L-201", "Grading and\ndrainage plan", "Graphic only — elevations in feet",
    notes=("1. Datum: existing pool patio = 100.00.\n   All elevations estimated; replace\n   with topographic survey values.\n"
           "2. Patio pitch 1/8\"–1/4\" per ft away\n   from the house; pavilion floor pitches\n   toward its open side.\n"
           "3. TD-2 replaces the existing channel\n   drain at the base of the wall being\n   removed; connect to its outlet.\n"
           "4. All roof leaders to 4\" solid PVC;\n   no splash blocks onto paving.\n"
           "5. Gravel + 4\" perforated drain behind\n   every retaining wall (L-601).\n"
           "6. Stairwell drain TD-1 needs a gravity\n   outlet below 98.0 or a sump pump.\n"
           "7. Outlet / dry well location by\n   engineer; keep 25' from septic field.\n"
           "8. Keep machines off the septic field\n   and the tank access."))
ax = plan_axes(fig, (-66, 66), (-82, 34))
base_context(ax)
site_steps(ax); site_walls(ax); pavilion_outline(ax)

def spot(x, y, val, kind="FG", color=INK):
    ax.plot([x], [y], marker="+", ms=7, mew=1.0, color=color, zorder=40)
    T(ax, x + 0.8, y + 0.9, f"{kind} {val:.2f}", size=5.9, color=color, ha="left", z=41)

# finished grades
for (x, y, v) in [(2, -1.5, 100.25), (22, -1.5, 100.25), (2, -20.5, 100.00), (22, -20.5, 100.00), (12, -28, 100.00),
                  (-12, -30, 100.00)]:
    spot(x, y, v)
for lp, v in [((-33, -2.5), 100.30), ((-8, -2.5), 100.30), ((-33, -20.5), 100.05), ((-8, -20.5), 100.05)]:
    p = W(*lp); spot(p[0], p[1], v)
spot(9.75, -2.0, 98.75, "LANDING", BLUE)
spot(33, -19.5, 102.50, "TOP WALK")
spot(-7, 4, 103.10, "TOP STEPS")
for lp, tw in [((-20, 2.6), 104.00), ((-38.5, -16), 102.50)]:
    p = W(*lp); spot(p[0], p[1], tw, "TW", RED)
spot(-44, -30, 101.50, "TW", RED)
for (x, y, v) in [(-30, 12, 104.0), (-50, 0, 104.5), (-52, -20, 102.5), (-14, 18, 103.5)]:
    spot(x, y, v, "EG", MID)
spot(10, -10, 102.50, "EG (remove)", MID)

# slope arrows
for (x, y) in [(5, -8), (17, -8)]:
    ax.annotate("", xy=(x, y - 8), xytext=(x, y), arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9, mutation_scale=9), zorder=30)
    T(ax, x + 1.2, y - 4, "1%", size=6, ha="left")
p0, p1 = np.array(W(-20, -4)), np.array(W(-20, -16))
ax.annotate("", xy=tuple(p1), xytext=tuple(p0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9, mutation_scale=9), zorder=30)
T(ax, *(p0 + p1) / 2 + np.array([1.5, 0]), "1%", size=6, ha="left")

# drainage
L(ax, [(-10, WALL_Y + 0.6), (26, WALL_Y + 0.6)], color=BLUE, lw=3.2, z=12)
T(ax, 8, WALL_Y - 1.6, "TD-2  trench drain (replaces existing channel drain)", size=6, color=BLUE, weight="bold")
x0, y0, x1, y1 = STAIRWELL
L(ax, [(x0 + 0.3, -3.6), (x1 - 0.3, -3.6)], color=BLUE, lw=3.2, z=12)
T(ax, x1 + 1.5, -3.2, "TD-1", size=6, color=BLUE, weight="bold", ha="left")
# wall drains behind W1-W4
for name, (pts, h) in WALLS.items():
    if name.startswith(("W1", "W2", "W3", "W4")):
        g = LineString(pts).parallel_offset(1.6, "left" if not name.startswith("W4") else "right")
        if g.geom_type == "LineString":
            L(ax, list(g.coords), color=BLUE, lw=1.0, ls=(0, (2, 1.5)), z=12)
# swale above pavilion
sw = [W(-42, 6), W(-20, 7), W(2, 6), (-12, 10)]
L(ax, sw, color="#5E8C3A", lw=1.4, ls=(0, (6, 3)), z=12)
T(ax, *W(-26, 9.2), "grass swale diverts lawn runoff around pavilion", size=5.8, color="#4E6B3E")
# downspouts and collector
ds = [(0.5, 0.5), (33.5, 0.5), W(-37.5, 1.5), W(-2.5, 1.5), W(-37.5, -23.5), W(-2.5, -23.5)]
for i, p in enumerate(ds, 1):
    ax.add_patch(Circle(p, 0.9, fc="white", ec=BLUE, lw=1.2, zorder=35)); T(ax, p[0] + 1.3, p[1] - 1.3, f"DS-{i}", size=5.6, color=BLUE, ha="left")
col = [(33.5, 0.5), (33.5, -2.2), (0.5, -2.2), (0.5, 0.5)]
L(ax, [(33.5, -2.2), (-2, -2.2)], color=BLUE, lw=1.4, z=11)
L(ax, [W(-2.5, 1.5), W(-37.5, 1.5)], color=BLUE, lw=1.4, z=11)
L(ax, [W(-37.5, 1.5), W(-37.5, -23.5), (-44, -40), (-50, -48)], color=BLUE, lw=1.4, z=11)
L(ax, [(-10, WALL_Y + 0.6), (-16, -30), (-40, -38), (-50, -48)], color=BLUE, lw=1.4, z=11)
L(ax, [(-2, -2.2), (-12, -4), W(-2.5, -23.5)], color=BLUE, lw=1.4, z=11)
ax.add_patch(Circle((-52, -50), 2.6, fc="white", ec=BLUE, lw=1.4, zorder=12))
T(ax, -52, -50, "DW-1", size=6, color=BLUE, weight="bold")
T(ax, -52, -55.5, "dry well or daylight outlet\n(location by engineer)", size=5.8, color=BLUE)
T(ax, -36, -41, "6\" solid PVC collector", size=5.8, color=BLUE, rot=-20)

# legend
lg = ("LEGEND\n"
      "+ FG 100.25   finished grade\n+ EG 104.0    existing grade (est.)\n+ TW 104.0    top of wall\n"
      "──  solid drain pipe\n┄┄  perforated wall drain\n▬▬  trench drain (TD)\n"
      "○ DS  roof leader / downspout\n→ 1%  slope direction")
frame.text(0.6, 2.25, lg, fontsize=6.6, family="DejaVu Sans Mono", color=INK, va="top", bbox=dict(fc="white", ec=INK, lw=0.6, pad=5))
fig.savefig("L-201.png", facecolor=PAPER); print("ok")

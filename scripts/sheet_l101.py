from sheets import *
from plan_angled import dim_any

fig, frame = new_sheet("L-101", "Layout and\ndimension plan", "Graphic only — use written dimensions",
    notes=("1. Origin 0,0 = rear corner of house\n   at the AC units. X runs along the\n   rear wall toward the sunroom; Y runs\n"
           "   out from the house toward the pool.\n2. Stake pavilion column centers from\n   the coordinate table, then check the\n"
           "   two diagonals (both 38'-10\").\n3. Pavilion is turned 55° from the\n   house wall so its open side faces\n"
           "   the near corner of the pool.\n4. Wall tags W1–W5: see L-601 and\n   the wall schedule.\n"
           "5. Verify all dimensions in the field\n   before ordering stone."))
ax = plan_axes(fig, (-62, 66), (-80, 34))
base_context(ax)
site_steps(ax); site_walls(ax); pavilion_outline(ax)
kitchen_furniture(ax)
north_arrow_local(ax, 58, 22)

# wall tags
for name, (pts, h) in WALLS.items():
    tag = name.split()[0]
    m = np.array(pts[len(pts) // 2]) if len(pts) > 2 else (np.array(pts[0]) + np.array(pts[1])) / 2
    ax.add_patch(Rectangle((m[0] - 1.7, m[1] - 1.0), 3.4, 2.0, fc="white", ec=INK, lw=0.7, zorder=30))
    T(ax, m[0], m[1], tag, size=6.2, weight="bold", z=31, bg=False)

# dimensions
dimline(ax, (19, 0), (19, WALL_Y), "23'-6\" meas.", off=-2.5)
dimline(ax, (0, -18), (30, -18), "30'-0\" (measured)", off=1.2)
dimline(ax, (0, 2.5), (6.5, 2.5), "6'-6\"", off=1.0)
dimline(ax, (6.5, 2.5), (13, 2.5), "6'-6\" stairwell", off=1.0)
dimline(ax, (14.5, 0), (14.5, -6.9), "6'-11\"", off=-1.6)
dimline(ax, (26, -25.5), (30, -25.5), "4'-0\"", off=-1.2)
dimline(ax, (-9, 31), (-5, 31), "4'-0\" path", off=1.0)
dim_any(ax, W(-36, -22), W(-4, -22), "32'-0\" column centers (10' / 12' / 10')", off=-3.4)
dim_any(ax, W(-36, 0), W(-36, -22), "22'-0\" column centers", off=-3.4)
c = W(-20, -11)
T(ax, c[0] + 2, c[1] - 3, "PAVILION\nroof 35' x 25'\nfloor 35' x 23'-6\"", size=6.4, weight="semibold")
T(ax, 3, -14, "NEW PATIO\nirregular bluestone\nat pool-patio level", size=6.4, color=MID)
T(ax, 35.5, -16.6, "square bluestone\nwalk (existing)", size=6, color=MID)
T(ax, -7, 12, "side path\nfrom French\ndoors", size=5.8, color=MID, rot=90)
T(ax, 9.75, -8.6, "basement\nstairwell", size=5.8, color=MID)

# coordinate table (x along wall, y out from house)
pts = {"C1": (-36, -22), "C2": (-26, -22), "C3": (-14, -22), "C4": (-4, -22), "C5": (-4, 0), "C6": (-36, 0)}
for k, (x, y) in pts.items():
    p = W(x, y); T(ax, p[0] + 1.6, p[1] + 1.6, k, size=6, color=BLUE, weight="bold")
rows = "\n".join(f"{k}   {W(*v)[0]:6.1f}   {-W(*v)[1]:6.1f}" for k, v in pts.items())
d1 = np.linalg.norm(np.array(W(-36, -22)) - np.array(W(-4, 0)))
frame.text(10.75, 3.0, "STAKING POINTS (ft)\ncolumn centers\n      X        Y\n" + rows + f"\ndiagonals {d1:.1f}\n(-Y = beside the house,\n street side of rear wall)",
           fontsize=6.8, family="DejaVu Sans Mono", color=INK, va="top", bbox=dict(fc="white", ec=INK, lw=0.6, pad=5))
fig.savefig("L-101.png", facecolor=PAPER); print("ok", d1)

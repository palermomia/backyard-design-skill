from sheets import *

fig, frame = new_sheet("L-301", "Pavilion elevations\nand roof plan", "Graphic only — heights in feet above pavilion floor",
    notes=("1. Heights are design intent; framing,\n   footings and fireplace by licensed\n   engineer / architect.\n"
           "2. Roof: 8:12 gable, architectural\n   shingles to match the house.\n"
           "3. Columns: 10\" square white PVC-wrapped\n   posts on 24\" fieldstone bases, 3'-0\"\n   high, 2\" thermal bluestone caps.\n"
           "4. Ceiling: painted tongue-and-groove,\n   two fans, dimmable downlights.\n"
           "5. Chimney top at least 2 ft above any\n   roof within 10 ft (confirm with\n   fire subcode)."))
STONE_H = "xx"
def stone(ax, x0, y0, x1, y1, z=4):
    P(ax, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fc=STONE, ec=INK, lw=0.8, z=z, hatch=".." )
def white(ax, x0, y0, x1, y1, z=5):
    P(ax, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fc="white", ec=INK, lw=0.8, z=z)
def vdim(ax, x, y0, y1, text, off=1.2):
    dimline(ax, (x, y0), (x, y1), text, off=off, size=6.2)

EAVE, PLATE, RIDGE, CHIM = 10.0, 9.0, 18.33, 21.0
# ---------------- front elevation
ax = fig.add_axes([0.04, 0.50, 0.50, 0.45]); ax.set_axis_off(); ax.set_aspect("equal")
ax.set_xlim(-6, 40); ax.set_ylim(-3, 24)
L(ax, [(-5, 0), (39, 0)], lw=1.4)
L(ax, [(-5, 3.5), (-1.5, 3.5)], color=MID, ls=(0, (4, 2))); L(ax, [(33.5, 3.5), (39, 3.5)], color=MID, ls=(0, (4, 2)))
T(ax, 36, 4.3, "lawn beyond\n(est. +3.5')", size=5.8, color=MID)
# back wall + fireplace seen between columns
stone(ax, -1.0, 0, 33.0, 3.8, z=2)
stone(ax, 11.5, 0, 20.5, EAVE + 0.2, z=2.5)
P(ax, [(14, 1.4), (18, 1.4), (17.4, 4.6), (14.6, 4.6)], fc="#3B3530", ec=INK, lw=0.8, z=3)
white(ax, 13, 0.0, 19, 1.4, z=3)
T(ax, 16, 0.7, "raised hearth", size=5.4, color=MID, bg=False)
stone(ax, 14.2, RIDGE - 1, 17.8, CHIM, z=1)
P(ax, [(14.0, CHIM), (18.0, CHIM), (18.0, CHIM + 0.4), (14.0, CHIM + 0.4)], fc="#9AA7AF", ec=INK, lw=0.8, z=1)
# roof
P(ax, [(-1.5, EAVE), (33.5, EAVE), (33.5, RIDGE), (-1.5, RIDGE)], fc="#6D7177", ec=INK, lw=0.9, z=6)
for y in np.arange(EAVE + 0.6, RIDGE, 0.6):
    L(ax, [(-1.5, y), (33.5, y)], color="#8C9096", lw=0.4, z=6.1)
white(ax, -1.5, EAVE - 0.9, 33.5, EAVE, z=7)
white(ax, -1.2, PLATE - 0.25, 33.2, PLATE + 0.1, z=7)
for x in (0, 10, 22, 32):
    stone(ax, x - 1.0, 0, x + 1.0, 3.0, z=8)
    P(ax, [(x - 1.15, 3.0), (x + 1.15, 3.0), (x + 1.15, 3.2), (x - 1.15, 3.2)], fc="#9AA7AF", ec=INK, lw=0.7, z=8)
    white(ax, x - 0.42, 3.2, x + 0.42, PLATE - 0.25, z=8)
T(ax, 16, 22.8, "FRONT ELEVATION (open side, facing the pool)", size=8, weight="bold", bg=False)
dimline(ax, (0, -1.0), (10, -1.0), "10'-0\"", off=-0.6, size=6)
dimline(ax, (10, -1.0), (22, -1.0), "12'-0\"", off=-0.6, size=6)
dimline(ax, (22, -1.0), (32, -1.0), "10'-0\"", off=-0.6, size=6)
vdim(ax, 35.5, 0, 3.0, "3'-0\" base", off=-1.0)
vdim(ax, 37.5, 0, PLATE, "9'-0\" clear", off=-1.0)
vdim(ax, -3.5, 0, RIDGE, "18'-4\" ridge", off=1.0)
vdim(ax, 20.8, RIDGE, CHIM + 0.4, "chimney", off=-0.9)
T(ax, 26, 15.4, "architectural shingles\nto match house", size=6, color="white", bg=False)
T(ax, 6, 2.0, "fieldstone back wall", size=5.6, color=INK, bg=False)

# ---------------- side elevation
ax2 = fig.add_axes([0.04, 0.05, 0.36, 0.43]); ax2.set_axis_off(); ax2.set_aspect("equal")
ax2.set_xlim(-6, 32); ax2.set_ylim(-3, 24)
L(ax2, [(-5, 0), (31, 0)], lw=1.4)
P(ax2, [(22.6, 0), (31, 0), (31, 4.0), (22.6, 4.0)], fc=GREEN, ec="none", z=1)
L(ax2, [(22.6, 4.0), (31, 4.3)], color=MID, ls=(0, (4, 2)))
T(ax2, 28, 5.0, "lawn (est.)", size=5.8, color=MID)
stone(ax2, 22.0, 0, 23.4, 4.3, z=3)
stone(ax2, 22.6, 0, 25.6, EAVE + 0.5, z=2)
stone(ax2, 23.2, EAVE, 25.4, CHIM, z=1.5)
P(ax2, [(23.0, CHIM), (25.6, CHIM), (25.6, CHIM + 0.4), (23.0, CHIM + 0.4)], fc="#9AA7AF", ec=INK, lw=0.8, z=1.6)
P(ax2, [(-1.5, EAVE), (11, RIDGE), (23.5, EAVE)], fc="white", ec=INK, lw=0.9, z=6)
for x in np.arange(0.5, 23, 1.0):
    ytop = EAVE + (RIDGE - EAVE) * (1 - abs(x - 11) / 12.5)
    L(ax2, [(x, EAVE), (x, ytop)], color=LIGHT, lw=0.5, z=6.1)
P(ax2, [(-1.9, EAVE - 0.2), (11, RIDGE + 0.35), (23.9, EAVE - 0.2), (23.5, EAVE - 0.6), (11, RIDGE - 0.1), (-1.5, EAVE - 0.6)], fc="#6D7177", ec=INK, lw=0.8, z=7)
white(ax2, -1.2, PLATE - 0.25, 23.2, PLATE + 0.1, z=7)
for x in (0, 22):
    stone(ax2, x - 1.0, 0, x + 1.0, 3.0, z=8)
    P(ax2, [(x - 1.15, 3.0), (x + 1.15, 3.0), (x + 1.15, 3.2), (x - 1.15, 3.2)], fc="#9AA7AF", ec=INK, lw=0.7, z=8)
    white(ax2, x - 0.42, 3.2, x + 0.42, PLATE - 0.25, z=8)
T(ax2, 11, 22.8, "SIDE ELEVATION (kitchen end)", size=8, weight="bold", bg=False)
dimline(ax2, (0, -1.0), (22, -1.0), "22'-0\" column centers", off=-0.6, size=6)
T(ax2, 11, 13.0, "8:12 gable\nwhite board-and-\nbatten gable end", size=6, bg=False)
T(ax2, 27.5, 9.5, "fireplace mass +\nretaining back wall", size=5.8, color=INK)
ax2.annotate("", xy=(23.6, 3.0), xytext=(28, 2.2), arrowprops=dict(arrowstyle="-", color=MID, lw=0.6))

# ---------------- roof plan
ax3 = fig.add_axes([0.43, 0.06, 0.34, 0.40]); ax3.set_axis_off(); ax3.set_aspect("equal")
ax3.set_xlim(-4, 39); ax3.set_ylim(-6, 34)
P(ax3, [(-1.5, -1.5), (33.5, -1.5), (33.5, 23.5), (-1.5, 23.5)], fc="#DADCDF", ec=INK, lw=1.0, z=2)
L(ax3, [(-1.5, 11), (33.5, 11)], lw=1.2, z=3)
for y0, y1 in ((11, 23.5), (11, -1.5)):
    ax3.annotate("", xy=(6, y1 + (2 if y1 < y0 else -2)), xytext=(6, y0 + (-1 if y1 < y0 else 1)),
                 arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.8, mutation_scale=8), zorder=4)
P(ax3, [(14.2, 23.5), (17.8, 23.5), (17.8, 26.1), (14.2, 26.1)], fc=STONE, ec=INK, lw=0.9, z=5, hatch="..")
T(ax3, 16, 27.5, "chimney", size=6)
for (x, y) in [(-1.5, -1.5), (33.5, -1.5), (-1.5, 23.5), (33.5, 23.5)]:
    ax3.add_patch(Circle((x, y), 0.7, fc="white", ec=BLUE, lw=1.0, zorder=6))
T(ax3, 16, 12.3, "RIDGE", size=6, weight="bold")
T(ax3, 9, 5, "8:12", size=6); T(ax3, 9, 17, "8:12", size=6)
T(ax3, 16, -4.3, "open side → pool", size=6, color=MID)
dimline(ax3, (-1.5, 23.5), (33.5, 23.5), "35'-0\" roof", off=4.5, size=6)
dimline(ax3, (33.5, -1.5), (33.5, 23.5), "25'-0\"", off=-2.0, size=6)
T(ax3, 16, 32.8, "ROOF PLAN", size=8, weight="bold", bg=False)
T(ax3, 37.5, -3.0, "○ downspout\n  (see L-201)", size=5.6, color=BLUE, ha="right")
fig.savefig("L-301.png", facecolor=PAPER); print("ok")

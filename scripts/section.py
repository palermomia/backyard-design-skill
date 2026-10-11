"""Grade section, house to pool, through the gym window. Option A vs Option B."""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle, Circle, FancyBboxPatch
import matplotlib.patheffects as pe
from plan import (PAPER, INK, SOFT, STONE, STONE_E, HOUSE, HOUSE_E, FLAG, FLAG_J, POOL, POOL_E, MULCH,
                  REMOVED, ACCENT, COPING)

EARTH = "#D9CDB6"
EARTH_H = "#BFAF92"
CONC = "#CFCBC3"
X0, X1 = -11, 43
Y0, Y1 = -6.5, 11.5


def P(ax, pts, fc, ec="none", lw=0.9, z=2, hatch=None, ls="-", alpha=1):
    ax.add_patch(MPoly(pts, closed=True, fc=fc, ec=ec, lw=lw, zorder=z, hatch=hatch, ls=ls, alpha=alpha,
                       joinstyle="miter"))


def txt(ax, x, y, s, size=7.6, color=SOFT, ha="left", va="center", weight="regular", z=30, style="normal"):
    t = ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, weight=weight, zorder=z, style=style,
                linespacing=1.3)
    t.set_path_effects([pe.withStroke(linewidth=2.8, foreground=PAPER)])
    return t


def leader(ax, xy, xytext, s, ha="left", size=7.4):
    ax.annotate(s, xy=xy, xytext=xytext, fontsize=size, color=SOFT, ha=ha, va="center", zorder=31,
                arrowprops=dict(arrowstyle="-", color=SOFT, lw=0.6, shrinkA=2, shrinkB=1),
                path_effects=[pe.withStroke(linewidth=2.8, foreground=PAPER)], linespacing=1.3)


def elev(ax, x, y, s, side="right"):
    ax.plot([x], [y], marker="v", ms=6, mfc="white", mec=ACCENT, mew=1.0, zorder=32)
    ax.plot([x - 1.6, x + 1.6], [y, y], color=ACCENT, lw=0.8, zorder=31)
    txt(ax, x + (1.9 if side == "right" else -1.9), y + 0.55, s, size=7.2, color=ACCENT,
        ha="left" if side == "right" else "right", weight="semibold")


def person(ax, x, y, z=20):
    # simple 5'-9" figure
    ax.add_patch(Circle((x, y + 5.35), 0.42, fc="#7C8790", ec="none", zorder=z))
    ax.add_patch(FancyBboxPatch((x - 0.55, y + 2.6), 1.1, 2.2, boxstyle="round,pad=0,rounding_size=0.4",
                                fc="#7C8790", ec="none", zorder=z))
    ax.plot([x - 0.25, x - 0.3], [y + 2.8, y], color="#7C8790", lw=3.2, zorder=z, solid_capstyle="round")
    ax.plot([x + 0.25, x + 0.3], [y + 2.8, y], color="#7C8790", lw=3.2, zorder=z, solid_capstyle="round")


def house_and_pool(ax, door=False):
    # earth base
    P(ax, [(X0, Y0), (X1, Y0), (X1, -2.1), (X0, -2.1)], EARTH, z=0.5)
    # basement interior (cut) - floor slab, foundation wall, rim, framed wall above
    P(ax, [(X0, -1.25), (-1.0, -1.25), (-1.0, 7.4), (X0, 7.4)], "#F1EEE7", z=1)
    P(ax, [(X0, -1.65), (-1.0, -1.65), (-1.0, -1.25), (X0, -1.25)], CONC, ec=HOUSE_E, lw=0.8, z=2)
    P(ax, [(X0, -2.1), (X0, -1.65), (-1.0, -1.65), (-1.0, -2.1)], EARTH, z=1.5)
    # footing + foundation wall
    P(ax, [(-2.0, -3.1), (1.0, -3.1), (1.0, -2.1), (-2.0, -2.1)], CONC, ec=HOUSE_E, lw=0.8, z=3)
    if door:
        P(ax, [(-1.0, -2.1), (0, -2.1), (0, -1.25), (-1.0, -1.25)], CONC, ec=HOUSE_E, lw=0.8, z=3, hatch="....")
        P(ax, [(-1.0, 5.95), (0, 5.95), (0, 6.6), (-1.0, 6.6)], "#6F7378", ec=HOUSE_E, lw=0.8, z=3)  # header
        # glass door
        P(ax, [(-0.65, -1.25), (-0.35, -1.25), (-0.35, 5.95), (-0.65, 5.95)], "#BFDDE6", ec=HOUSE_E, lw=0.8, z=3)
    else:
        P(ax, [(-1.0, -2.1), (0, -2.1), (0, 2.5), (-1.0, 2.5)], CONC, ec=HOUSE_E, lw=0.8, z=3, hatch="....")
        P(ax, [(-1.0, 5.0), (0, 5.0), (0, 6.6), (-1.0, 6.6)], CONC, ec=HOUSE_E, lw=0.8, z=3, hatch="....")
        P(ax, [(-0.65, 2.5), (-0.35, 2.5), (-0.35, 5.0), (-0.65, 5.0)], "#BFDDE6", ec=HOUSE_E, lw=0.8, z=3)
    # rim + first floor framing
    P(ax, [(-1.0, 6.6), (0, 6.6), (0, 7.6), (X0, 7.6), (X0, 7.4), (-1.0, 7.4)], "#C9B391", ec=HOUSE_E, lw=0.8, z=3)
    P(ax, [(X0, 7.6), (-0.2, 7.6), (-0.2, 8.0), (X0, 8.0)], "#E2D6BE", ec=HOUSE_E, lw=0.6, z=3)
    # framed wall with siding
    P(ax, [(-0.6, 7.6), (0, 7.6), (0, Y1), (-0.6, Y1)], HOUSE, ec=HOUSE_E, lw=0.8, z=3)
    for y in np.arange(7.9, Y1, 0.55):
        ax.plot([0, 0.12], [y, y - 0.1], color=HOUSE_E, lw=0.5, zorder=3.1)
    # first-floor window
    P(ax, [(-0.45, 8.6), (-0.15, 8.6), (-0.15, 11.5), (-0.45, 11.5)], "#BFDDE6", ec=HOUSE_E, lw=0.7, z=3.2)
    txt(ax, -6, 2.6, "BASEMENT GYM", size=8.4, color=HOUSE_E, ha="center", weight="semibold")
    txt(ax, -6, 1.5, "full bath down the hall", size=7.0, color=HOUSE_E, ha="center")
    txt(ax, -6, 9.6, "MAIN LEVEL", size=7.6, color=HOUSE_E, ha="center", weight="semibold")
    elev(ax, -8.7, -1.25, "–1'-3\" gym floor (est.)", side="right")

    # pool: patio continues to coping, then pool shell + water
    P(ax, [(33.0, -0.45), (34.2, -0.45), (34.2, 0), (33.0, 0)], COPING, ec="#A9A396", lw=0.7, z=6)
    P(ax, [(34.2, -5.6), (X1, -5.6), (X1, -0.55), (34.2, -0.55)], POOL, ec="none", z=4)
    P(ax, [(33.4, -6.1), (34.2, -6.1), (34.2, -0.45), (33.4, -0.45)], CONC, ec=HOUSE_E, lw=0.7, z=5)
    P(ax, [(34.2, -6.1), (X1, -6.1), (X1, -5.6), (34.2, -5.6)], CONC, ec=HOUSE_E, lw=0.7, z=5)
    ax.plot([34.2, X1], [-0.55, -0.55], color=POOL_E, lw=1.0, zorder=5)
    txt(ax, 38.6, -3.2, "POOL", size=8.4, color=POOL_E, ha="center", weight="semibold")
    # pool patio slab (0'-0") from wall line to coping
    return


def patio(ax, x0, x1, y, z=6, thick=0.55):
    P(ax, [(x0, y - thick), (x1, y - thick), (x1, y), (x0, y)], "#8FA0AB", ec="#5E6D78", lw=0.7, z=z)
    P(ax, [(x0, y - thick - 0.5), (x1, y - thick - 0.5), (x1, y - thick), (x0, y - thick)], "#E3DDD0",
      ec="none", z=z - 0.1, hatch="....")


def earth_fill(ax, pts):
    P(ax, pts, EARTH, z=1)
    P(ax, pts, "none", ec=EARTH_H, lw=0, z=1.05, hatch="///")


def panel_a(ax):
    house_and_pool(ax, door=True)
    R = 1.25 / 3            # three ~5" risers from the gym-floor landing up to the patio
    T = 0.95                # ~11" treads
    L = 3.6                 # landing depth in front of the door
    xs = L + 3 * T
    # capped stone side wall of the stairwell, seen beyond the cut
    P(ax, [(0, -1.25), (xs + 0.4, -1.25), (xs + 0.4, 1.3), (0, 1.3)], "#A69E90", ec=STONE_E, lw=0.8, z=4.5)
    P(ax, [(0, -1.25), (xs + 0.4, -1.25), (xs + 0.4, 1.3), (0, 1.3)], "none", ec="#C4BCAE", lw=0, z=4.55, hatch="////")
    P(ax, [(-0.05, 1.3), (xs + 0.55, 1.3), (xs + 0.55, 1.55), (-0.05, 1.55)], "#9AA7AF", ec=STONE_E, lw=0.8, z=4.6)
    # earth under the patio and the stairwell
    earth_fill(ax, [(xs, -1.1), (33.4, -1.1), (33.4, Y0), (0, Y0), (0, -2.35), (xs, -2.35)])
    earth_fill(ax, [(-2.0, Y0), (0, Y0), (0, -3.1), (-2.0, -3.1)])
    # landing at gym-floor level, then three steps up to the patio
    patio(ax, 0, L, -1.25)
    for i in range(3):
        x0 = L + i * T
        top = -1.25 + (i + 1) * R
        P(ax, [(x0, -2.35), (x0 + T, -2.35), (x0 + T, top), (x0, top)], "#8FA0AB", ec="#5E6D78", lw=0.7, z=6.1)
    patio(ax, xs, 33.0, 0.0)
    P(ax, [(L - 1.0, -1.95), (L - 0.3, -1.95), (L - 0.3, -1.25), (L - 1.0, -1.25)], "#5E6268", ec=HOUSE_E, lw=0.6, z=7)
    # existing grade + wall (to be removed), dashed
    ax.plot([0.45, 23.5], [2.5, 2.6], color=REMOVED, lw=1.3, ls=(0, (5, 3)), zorder=12)
    P(ax, [(23.5, 0), (25.0, 0), (25.0, 2.75), (23.5, 2.75)], "none", ec=REMOVED, lw=1.2, ls=(0, (3, 2)), z=12)
    P(ax, [(xs + 0.6, 0.05), (23.5, 0.05), (23.5, 2.6), (xs + 0.6, 2.55)], REMOVED, z=11, alpha=0.08)
    txt(ax, 15.0, 1.3, "about 2'-6\" of soil removed here\nroughly 250 cu yd across the project (est.)",
        size=7.4, color=REMOVED, ha="center", weight="medium")
    person(ax, 21.5, 0.0)
    person(ax, 30.0, 0.0)
    elev(ax, 10.5, 0.0, "0'-0\" new patio = pool patio", side="right")
    leader(ax, (-0.5, 3.6), (2.0, 7.4), "New door to gym + bath where the window is\n(sill is at today's grade); header by engineer")
    leader(ax, (5.2, 1.4), (8.0, 4.6), "Capped fieldstone side walls, like the\nexisting steps down to the pool")
    leader(ax, (L - 0.65, -1.7), (7.2, -3.6), "3 steps down (~5\" each) to a landing at gym-floor\nlevel; trench drain at the landing")
    leader(ax, (24.5, 2.75), (25.6, 7.6), "Existing 27–33\" wall +\nplanting bed removed")
    leader(ax, (30.0, -0.3), (25.5, -3.6), "One level, pitched ⅛–¼\" per ft away from house")


def panel_b(ax):
    house_and_pool(ax, door=False)
    # earth: terrace level to the wall, pool level beyond
    earth_fill(ax, [(0, 1.9), (23.5, 1.9), (23.5, Y0), (0, Y0)])
    earth_fill(ax, [(25.0, -1.1), (33.4, -1.1), (33.4, Y0), (25.0, Y0)])
    earth_fill(ax, [(-2.0, Y0), (0, Y0), (0, -2.6), (-2.0, -2.6)])
    patio(ax, 0.1, 20.0, 2.5)
    # planting bed on top of wall
    P(ax, [(20.0, 1.9), (23.5, 1.9), (23.5, 2.6), (20.0, 2.6)], MULCH, ec="#B7A688", lw=0.7, z=6)
    for x in (20.8, 21.9, 22.9):
        for k in range(7):
            a = np.radians(60 + k * 10)
            ax.plot([x, x + 1.4 * np.cos(a)], [2.6, 2.6 + 1.4 * np.sin(a)], color="#A39C74", lw=0.7, zorder=6.2)
    # existing wall
    P(ax, [(23.5, -1.6), (25.0, -1.6), (25.0, 2.75), (23.5, 2.75)], STONE, ec=STONE_E, lw=0.9, z=7)
    P(ax, [(23.5, -1.6), (25.0, -1.6), (25.0, 2.75), (23.5, 2.75)], "none", ec="#B4AC9E", lw=0, z=7.1, hatch="////")
    P(ax, [(23.3, 2.75), (25.3, 2.75), (25.3, 3.05), (23.3, 3.05)], "#9AA7AF", ec=STONE_E, lw=0.8, z=7.2)
    patio(ax, 25.0, 33.0, 0.0)
    person(ax, 10.5, 2.5)
    person(ax, 30.0, 0.0)
    elev(ax, 3.5, 2.5, "+2'-6\" terrace (today's grade)", side="right")
    elev(ax, 26.5, 0.0, "0'-0\" pool patio", side="right")
    leader(ax, (-0.5, 3.6), (3.2, 6.6), "Window sill is at today's grade: terrace needs a\nwindow well and waterproofing here")
    leader(ax, (24.3, 3.0), (25.6, 7.6), "Existing wall + bed kept;\nbed is the buffer at the drop")
    leader(ax, (14.0, 2.2), (12.0, -2.8), "Terrace pitched away from house; drains through wall weeps")


def draw(out):
    fig = plt.figure(figsize=(15.5, 11.4), dpi=170)
    fig.patch.set_facecolor(PAPER)
    fig.text(0.03, 0.972, "Grade section — house to pool, cut through the gym window", fontsize=16,
             weight="bold", color=INK, va="top")
    fig.text(0.03, 0.937, "Same cut, both options. Elevations relative to the pool patio (0'-0\"). Basement floor "
             "level is set from your 45 in floor-to-sill (sill at today's grade) and 27–33 in wall; soil volume is an estimate.",
             fontsize=8.8, color=SOFT, va="top")
    for i, (title, fn) in enumerate([("Option A — Flat (recommended)", panel_a),
                                     ("Option B — Elevated terrace", panel_b)]):
        ax = fig.add_axes([0.03, 0.52 - i * 0.465, 0.94, 0.37])
        ax.set_xlim(X0, X1)
        ax.set_ylim(Y0, Y1)
        ax.set_aspect("equal")
        ax.set_axis_off()
        ax.add_patch(Rectangle((X0, Y0), X1 - X0, Y1 - Y0, fc="#FBFAF6", ec="none", zorder=0))
        fn(ax)
        ax.add_patch(Rectangle((X0, Y0), X1 - X0, Y1 - Y0, fc="none", ec=INK, lw=1.2, zorder=40))
        ax.text(X0, Y1 + 0.6, title, fontsize=12.5, weight="bold", color=INK, va="bottom")
        # distance ruler
        for d in range(0, 36, 5):
            ax.plot([d, d], [Y0, Y0 + 0.35], color=SOFT, lw=0.6, zorder=41)
            ax.text(d, Y0 - 0.35, f"{d}'", fontsize=6.8, color=SOFT, ha="center", va="top")
        ax.text(X1, Y0 - 0.35, "distance from house (ft)", fontsize=6.8, color=SOFT, ha="right", va="top")
        ax.annotate("", xy=(23.5, Y1 - 1.9), xytext=(0, Y1 - 1.9),
                    arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=0.8, mutation_scale=7), zorder=42)
        t = ax.text(11.75, Y1 - 1.5, "23.5' house to existing wall (measured)", fontsize=7.4, color=INK,
                    ha="center", va="bottom", weight="semibold", zorder=42)
        t.set_path_effects([pe.withStroke(linewidth=2.8, foreground="#FBFAF6")])
    fig.savefig(out, facecolor=PAPER)


if __name__ == "__main__":
    draw(sys.argv[1])

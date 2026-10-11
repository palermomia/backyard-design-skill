"""Design-development drawing set for the backyard project (Option A, flat).

Local plan coordinates (feet): origin = rear corner of the house at the AC units,
+x along the rear wall toward the sunroom, -y away from the house toward the pool.
Survey frame: u along the front lot line (east), v into the lot (toward the back).
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle, Circle, FancyBboxPatch, Arc
from matplotlib.transforms import Affine2D
import matplotlib.patheffects as pe
from shapely.geometry import Polygon, LineString, box, Point
from shapely.ops import unary_union

import plan  # noqa: registers fonts
from plan_angled import (W, BW, BE, FW, FE, NEW_CURVE_A, WALL_KEPT, KEEP_FROM, CENTER, THETA, U_LONG,
                         N_FRONT, PT)
from plan import POOL_PATIO, PATIO_E, WALK, WALK_STEPS, WALL_Y

INK = "#1E252B"; MID = "#5B646C"; LIGHT = "#C9CED2"; PAPER = "#FFFFFF"; FILL = "#EEF0F1"
STONE = "#B9B2A6"; WATER = "#CFE9EC"; GREEN = "#E3EBD8"; BLUE = "#1F6FB2"; RED = "#B23A2B"
ORANGE = "#C77A12"; PLANT = "#6E8F4E"

DATE = "2026-10-11"
from config import PROJECT_NAME, SITE_LINE
PROJECT = PROJECT_NAME + " — " + SITE_LINE


# ------------------------------------------------------------------ geometry (local)
HOUSE = [(0, 0), (34, 0), (34, 40), (0, 40)]
SUNROOM = [(34, -3), (58, -3), (58, 12), (34, 12)]
COL_LOCAL = [(-36, -22), (-26, -22), (-14, -22), (-4, -22), (-4, 0), (-36, 0)]
COLS = [W(*c) for c in COL_LOCAL]
ROOF = [W(-37.5, 1.5), W(-2.5, 1.5), W(-2.5, -23.5), W(-37.5, -23.5)]
PAV_FLOOR = [W(-37.5, 0.7), W(-2.5, 0.7), W(-2.5, -22.8), W(-37.5, -22.8)]
OUTLINE = Polygon([BW, BE, (-9.5, 1.6), (-9.5, 0), (0, 0), (26, 0), (26, WALL_Y), (-10, WALL_Y),
                   (-13.5, -25.0), (-15.6, -28.0), (-16, -32.0), (-16, KEEP_FROM[1])]
                  + NEW_CURVE_A[::-1] + [FW]).buffer(0)
PAVE = unary_union([POOL_PATIO, OUTLINE]).difference(box(26, -12, 80, 0)).difference(box(30, WALL_Y, 80, -12))
PAVE = PAVE.intersection(box(-80, -90, PATIO_E, 10))
STAIRWELL = (6.5, -6.9, 13.0, 0.0)          # x0, y0, x1, y1
LANDING_Y = -4.0
SIDE_PATH = unary_union([box(-9, 1.6, -5, 29.5), box(-9, 22.5, -3.5, 29.5)])
WALLS = {   # name: (polyline, height note)
    "W1 pavilion back wall": ([W(-37.5, 0.7), W(-2.5, 0.7)], "3'-6\" to 4'-0\" exposed"),
    "W2 pavilion end wall": ([W(-36.7, 0.7), W(-36.7, -22.8)], "4'-0\" tapering to 1'-0\""),
    "W3 link wall to side steps": ([BE, (-9.5, 1.6)], "2'-6\" to 3'-6\""),
    "W4 curved wall": (NEW_CURVE_A, "1'-0\" to 2'-6\""),
    "W5 house-corner wall": ([(-4.6, 0.7), (0, 0.7)], "2'-6\""),
}


def tf_local_to_world():
    """local (x,y) -> survey E,N.  u = 184.5 - x, v = 105 - y."""
    from config import FRONT_BEARING as _FB
    uhat = np.array([np.cos(np.radians(_FB)), np.sin(np.radians(_FB))]); vhat = np.array([-uhat[1], uhat[0]])
    def f(p):
        x, y = p
        from config import HOUSE_U, HOUSE_V
        u, v = HOUSE_U - x, HOUSE_V - y
        return tuple(u * uhat + v * vhat)
    return f


# ------------------------------------------------------------------ sheet frame
def new_sheet(num, title, scale_note, notes=None):
    fig = plt.figure(figsize=(17, 11), dpi=150)
    fig.patch.set_facecolor(PAPER)
    frame = fig.add_axes([0, 0, 1, 1]); frame.set_axis_off(); frame.set_xlim(0, 17); frame.set_ylim(0, 11)
    frame.add_patch(Rectangle((0.3, 0.3), 16.4, 10.4, fill=False, ec=INK, lw=1.6))
    frame.add_patch(Rectangle((13.3, 0.3), 3.4, 10.4, fill=False, ec=INK, lw=1.0))
    # title block
    y = 10.45
    frame.text(13.5, y, PROJECT.split(" — ")[0], fontsize=12, weight="bold", color=INK, va="top")
    frame.text(13.5, y - 0.32, PROJECT.split(" — ")[1], fontsize=8, color=MID, va="top", wrap=True)
    frame.plot([13.3, 16.7], [9.75, 9.75], color=INK, lw=0.8)
    frame.text(13.5, 9.6, "DESIGN DEVELOPMENT\nfor review and pricing", fontsize=9, weight="semibold",
               color=INK, va="top", linespacing=1.3)
    frame.text(13.5, 9.0, "Not for construction. Walls over 4 ft, the foundation\nopening, pavilion "
               "footings and the fireplace\nrequire a licensed engineer or architect.\nGrades are "
               "estimated until a topographic\nsurvey is done.", fontsize=7.2, color=RED, va="top",
               linespacing=1.35)
    if notes:
        frame.text(13.5, 7.55, "NOTES", fontsize=8, weight="bold", color=INK, va="top")
        frame.text(13.5, 7.32, notes, fontsize=7.2, color=MID, va="top", linespacing=1.4)
    frame.plot([13.3, 16.7], [2.05, 2.05], color=INK, lw=0.8)
    frame.text(13.5, 1.9, title.upper(), fontsize=10.5, weight="bold", color=INK, va="top", linespacing=1.25)
    frame.text(13.5, 1.15, scale_note, fontsize=7.5, color=MID, va="top")
    frame.text(13.5, 0.75, f"Date {DATE}   Option A (flat)", fontsize=7.5, color=MID, va="top")
    frame.add_patch(Rectangle((15.6, 0.45), 0.95, 0.55, fill=False, ec=INK, lw=1.0))
    frame.text(16.075, 0.72, num, fontsize=13, weight="bold", color=INK, ha="center", va="center")
    return fig, frame


def plan_axes(fig, xlim, ylim, rect=(0.035, 0.05, 0.73, 0.9)):
    ax = fig.add_axes(rect); ax.set_axis_off(); ax.set_aspect("equal")
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    return ax


def P(ax, pts, fc="none", ec=INK, lw=0.8, z=2, ls="-", hatch=None, alpha=1):
    ax.add_patch(MPoly(pts, closed=True, fc=fc, ec=ec, lw=lw, zorder=z, ls=ls, hatch=hatch, alpha=alpha))


def G(ax, geom, **kw):
    for g in getattr(geom, "geoms", [geom]):
        if g.geom_type == "Polygon":
            P(ax, list(g.exterior.coords), **kw)


def L(ax, pts, color=INK, lw=0.8, ls="-", z=3):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=z, solid_capstyle="butt")


def T(ax, x, y, s, size=6.8, color=INK, ha="center", va="center", rot=0, weight="regular", z=20, bg=True):
    t = ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, rotation=rot, weight=weight, zorder=z,
                linespacing=1.25, rotation_mode="anchor")
    if bg:
        t.set_path_effects([pe.withStroke(linewidth=2.4, foreground="white")])
    return t


def wall(ax, pts, w=1.3, z=5):
    g = LineString(pts).buffer(w / 2, cap_style=2, join_style=2)
    G(ax, g, fc=STONE, ec=INK, lw=0.8, z=z)


def treads(ax, x0, y0, x1, y1, n, axis, z=4):
    P(ax, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fc="white", ec=INK, lw=0.8, z=z)
    for i in range(1, n):
        t = i / n
        if axis == "x":
            x = x0 + (x1 - x0) * t; L(ax, [(x, y0), (x, y1)], lw=0.5, z=z + 0.1)
        else:
            y = y0 + (y1 - y0) * t; L(ax, [(x0, y), (x1, y)], lw=0.5, z=z + 0.1)


def dimline(ax, p0, p1, text, off=2.0, size=6.6, color=INK, z=25):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = (p1 - p0) / np.linalg.norm(p1 - p0); n = np.array([-d[1], d[0]])
    a, b = p0 + off * n, p1 + off * n
    ax.annotate("", xy=tuple(b), xytext=tuple(a), arrowprops=dict(arrowstyle="<|-|>", color=color, lw=0.6,
                mutation_scale=6, shrinkA=0, shrinkB=0), zorder=z, annotation_clip=False)
    for p, q in ((p0, a), (p1, b)):
        ax.plot([p[0] + 0.4 * np.sign(off) * n[0], q[0] + 0.6 * np.sign(off) * n[0]],
                [p[1] + 0.4 * np.sign(off) * n[1], q[1] + 0.6 * np.sign(off) * n[1]], color=color, lw=0.4, zorder=z)
    ang = np.degrees(np.arctan2(d[1], d[0]))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    m = (a + b) / 2 + 0.9 * np.sign(off) * n
    T(ax, m[0], m[1], text, size=size, color=color, rot=ang, weight="semibold", z=z)


def north_arrow_local(ax, x, y, size=4):
    """True north in local coords. local->world is a 180deg rotation of (u,v) then (u,v)->(E,N)."""
    from config import FRONT_BEARING as _FB
    _u = np.array([np.cos(np.radians(_FB)), np.sin(np.radians(_FB))]); _v = np.array([-_u[1], _u[0]])
    n = -np.array([_u[1], _v[1]]); n /= np.linalg.norm(n)
    tip = np.array([x, y]) + n * size; tail = np.array([x, y]) - n * size * 0.4
    ax.annotate("", xy=tuple(tip), xytext=tuple(tail), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2,
                mutation_scale=14), zorder=30)
    T(ax, *(tip + n * 1.6), "N", size=9, weight="bold")


def base_context(ax, pave=True, light=False):
    """House, pool, pool house, walk and paving outline in plain line style."""
    if pave:
        G(ax, PAVE, fc=FILL, ec=INK, lw=0.7, z=1)
    for pts in (HOUSE, SUNROOM):
        P(ax, pts, fc="white", ec=INK, lw=1.4, z=6, hatch="////")
    T(ax, 17, 14, "EXISTING\nHOUSE", size=8, weight="bold", color=MID)
    P(ax, [(35, -6), (41, -6), (41, -3), (35, -3)], fc="white", ec=INK, lw=0.7, z=6)
    treads(ax, 35.5, -12, 40.5, -6, 7, "y", z=6)
    T(ax, 44, -9, "existing\ndeck stairs", size=6, color=MID, ha="left")
    P(ax, list(box(-5, -74, 17, -32).exterior.coords), fc="white", ec=INK, lw=0.7, z=2)
    P(ax, list(box(-4, -73, 16, -33).exterior.coords), fc=WATER, ec=INK, lw=0.9, z=2.1)
    T(ax, 6, -52, "EXISTING POOL\n20' x 40'", size=7, color=MID, weight="semibold")
    P(ax, [(-30, -64), (-16.4, -64), (-16.4, -50), (-30, -50)], fc="white", ec=INK, lw=1.0, z=6, hatch="////")
    T(ax, -23.2, -57, "POOL\nHOUSE", size=6.5, color=MID, weight="semibold")
    G(ax, WALK, fc="white", ec=INK, lw=0.8, z=4)
    treads(ax, *WALK_STEPS, 3, "y", z=4)
    # septic field
    ax.add_patch(FancyBboxPatch((44, -66), 22, 50, boxstyle="round,pad=0,rounding_size=4", fc="none", ec=MID,
                                lw=0.8, ls=(0, (4, 3)), zorder=1))
    T(ax, 55, -40, "SEPTIC FIELD\n(approx.) —\nno paving or\nequipment", size=6.2, color=MID)


def pavilion_outline(ax, cols=True, roof=True, z=8):
    P(ax, PAV_FLOOR, fc="white", ec=INK, lw=0.9, z=z - 1)
    if roof:
        P(ax, ROOF, ec=INK, lw=0.9, ls=(0, (6, 3)), z=z)
        a, b = W(-37.5, -11), W(-2.5, -11)
        L(ax, [a, b], lw=0.6, ls=(0, (10, 3, 2, 3)), z=z)
    if cols:
        for (x, y) in COLS:
            sq = Polygon([(-1.1, -1.1), (1.1, -1.1), (1.1, 1.1), (-1.1, 1.1)])
            pts = [tuple(np.array(PT().transform((x0, y0))) - np.array(PT().transform((0, 0)))) for x0, y0 in sq.exterior.coords]
            P(ax, [(x + px, y + py) for px, py in pts], fc=STONE, ec=INK, lw=0.8, z=z + 1)


def site_walls(ax):
    for name, (pts, h) in WALLS.items():
        wall(ax, pts, 1.4)
    wall(ax, list(WALL_KEPT.coords), 1.3)
    x0, y0, x1, y1 = STAIRWELL
    wall(ax, [(x0 - 0.45, 0), (x0 - 0.45, y0 - 0.3)], 0.9); wall(ax, [(x1 + 0.45, 0), (x1 + 0.45, y0 - 0.3)], 0.9)
    wall(ax, [(25.8, -12.0), (30.2, -12.0)], 0.9); wall(ax, [(25.8, -23.3), (30.2, -23.3)], 0.9)
    wall(ax, [(30.2, -23.5), (30.2, -21.0)], 0.9); wall(ax, [(PATIO_E - 0.2, -23.5), (PATIO_E - 0.2, -21.0)], 0.9)
    wall(ax, [(-9.5, 1.6), (-9.5, -4.4)], 0.9); wall(ax, [(-4.55, 1.6), (-4.55, -4.4)], 0.9)
    wall(ax, [(26.4, 0), (26.4, -12)], 1.2)


def site_steps(ax):
    treads(ax, 26, WALL_Y, 30, -12, 4, "x")
    x0, y0, x1, y1 = STAIRWELL
    P(ax, [(x0, LANDING_Y), (x1, LANDING_Y), (x1, y1), (x0, y1)], fc="white", ec=INK, lw=0.8, z=4)
    treads(ax, x0, y0, x1, LANDING_Y, 3, "y")
    treads(ax, -9, -4.4, -5, 1.6, 5, "y")
    G(ax, SIDE_PATH, fc="white", ec=INK, lw=0.7, z=3)


def kitchen_furniture(ax):
    from plan import furniture
    n_p, n_l = len(ax.patches), len(ax.lines)
    furniture(ax)
    tr = PT() + ax.transData
    for p in ax.patches[n_p:]:
        p.set_transform(tr); p.set_facecolor("white"); p.set_edgecolor(MID); p.set_hatch(None)
    for l in ax.lines[n_l:]:
        l.set_transform(tr); l.set_color(MID)

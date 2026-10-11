"""Angled-pavilion version of the site plans. Reuses the drawing kit in plan.py.

The pavilion is drawn in its original local coordinates (columns at x -36..-4, y -22..0,
centre (-20, -11)) and then rotated THETA degrees and placed so its centre line points at
the pool's north-west (near) corner.
"""
import sys
import numpy as np
from plan import *  # noqa: F401,F403  (drawing kit, palette, site constants)
from plan import (furniture, pavilion_frame, stone_wall, steps, arrow_down, flagstone, squarestone, shp, poly,
                  lines, shrub, label, callout, elev, house, pool_and_poolhouse, septic_field, trees_and_ac,
                  legend_panel, key_strip, setup, frame, base_layers, dim)
from matplotlib.transforms import Affine2D
from matplotlib.patches import Circle, Arc
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString, box
from shapely.ops import unary_union

THETA = 55.0                    # degrees the pavilion turns toward the pool corner
POOL_CORNER = (-5.0, -32.0)     # pool coping, north-west corner
D_AXIS = 30.0                   # pavilion centre to pool corner, ft
LOCAL_C = (-20.0, -11.0)

_t = np.radians(THETA)
N_FRONT = np.array([np.sin(_t), -np.cos(_t)])        # direction the open front faces
U_LONG = np.array([np.cos(_t), np.sin(_t)])          # along the long axis, toward the kitchen end
CENTER = np.array(POOL_CORNER) - D_AXIS * N_FRONT


def PT():
    return Affine2D().translate(-LOCAL_C[0], -LOCAL_C[1]).rotate_deg(THETA).translate(*CENTER)


def W(x, y):
    return tuple(PT().transform((x, y)))


def placed(ax, fn, *a, **kw):
    n_p, n_l = len(ax.patches), len(ax.lines)
    fn(ax, *a, **kw)
    tr = PT() + ax.transData
    for p in ax.patches[n_p:]:
        p.set_transform(tr)
    for l in ax.lines[n_l:]:
        l.set_transform(tr)


def bez(p0, c, p1, n=14):
    t = np.linspace(0, 1, n)[:, None]
    p0, c, p1 = map(np.array, (p0, c, p1))
    return [tuple(v) for v in ((1 - t) ** 2 * p0 + 2 * (1 - t) * t * c + t ** 2 * p1)]


def dim_any(ax, p0, p1, text, off, z=25, color=INK):
    p0, p1 = np.array(p0), np.array(p1)
    d = (p1 - p0) / np.linalg.norm(p1 - p0)
    n = np.array([-d[1], d[0]])
    a, b = p0 + off * n, p1 + off * n
    ax.annotate("", xy=tuple(b), xytext=tuple(a), arrowprops=dict(arrowstyle="<|-|>", color=color, lw=0.8,
                mutation_scale=7, shrinkA=0, shrinkB=0), zorder=z)
    for p, q in ((p0, a), (p1, b)):
        e = q + 0.9 * np.sign(off) * n
        ax.plot([p[0] + 0.6 * np.sign(off) * n[0], e[0]], [p[1] + 0.6 * np.sign(off) * n[1], e[1]],
                color=color, lw=0.5, zorder=z)
    ang = np.degrees(np.arctan2(d[1], d[0]))
    if ang > 90:
        ang -= 180
    if ang < -90:
        ang += 180
    m = (a + b) / 2 + 1.3 * np.sign(off) * n
    t = ax.text(m[0], m[1], text, rotation=ang, rotation_mode="anchor", fontsize=7.2, color=color, ha="center",
                va="center", zorder=z, weight="semibold")
    t.set_path_effects([pe.withStroke(linewidth=3, foreground=PAPER)])


def back_and_west_walls(ax, west=True):
    stone_wall(ax, LineString([(-37.5, 0.7), (-2.5, 0.7)]), 1.5)
    if west:
        stone_wall(ax, LineString([(-36.7, 0.7), (-36.7, -22.8)]), 1.5)


def pavilion(ax):
    placed(ax, furniture)
    placed(ax, pavilion_frame, west_steps=False)


def view_line(ax):
    """Dashed sight line from the hearth to the pool corner."""
    a = np.array(W(-20, -4))
    b = np.array(POOL_CORNER) + 1.0 * N_FRONT
    ax.plot([a[0], b[0]], [a[1], b[1]], color=ACCENT, lw=0.9, ls=(0, (1.5, 2.5)), zorder=16.5, alpha=0.8)


# key world points
BW = W(-37.5, 0.7)      # back-west outer corner
BE = W(-2.5, 0.7)       # back-east outer corner
FW = W(-37.5, -22.8)    # front-west
FE = W(-4.0, -22.0)     # front-east column
KEEP_FROM = (-16.6, -40.5)
NEW_CURVE_A = bez(W(-36.7, -22.8), (FW[0] + 1.5, KEEP_FROM[1] - 0.5), KEEP_FROM)
WALL_REMOVED = LineString([(30, WALL_Y), (-10, WALL_Y), (-13.5, -25.0), (-15.6, -28.0), (-16.6, -32.0),
                           KEEP_FROM])
WALL_KEPT = LineString([KEEP_FROM, (-16.6, -50.0)])


def pav_dims(ax):
    dim_any(ax, W(-36, -22), W(-4, -22), "32'", off=-3.2)
    dim_any(ax, W(-36, 0), W(-36, -22), "22'", off=-3.6)


def pav_callouts(ax):
    for n, (x, y) in [(1, (-30.5, 4.6)), (2, (-20, 6.2)), (3, (-12.3, -19.4)), (4, (-9.6, -4.4)),
                      (5, (-24.3, -17.2)), (6, (-31.2, -3.8))]:
        callout(ax, *W(x, y), n)


# ================================================================ OPTION A
def option_a(out):
    fig, ax = setup()
    base_layers(ax)
    septic_field(ax)

    outline = Polygon([BW, BE, (-9.5, 1.6), (-9.5, 0), (0, 0), (26, 0), (26, WALL_Y), (-10, WALL_Y),
                       (-13.5, -25.0), (-15.6, -28.0), (-16, -32.0), (-16, KEEP_FROM[1])]
                      + NEW_CURVE_A[::-1] + [FW])
    pave = unary_union([POOL_PATIO, outline.buffer(0)])
    pave = pave.difference(box(26, -12, 80, 0)).difference(box(30, WALL_Y, 80, -12))
    pave = pave.intersection(box(-80, -90, PATIO_E, 10))
    flagstone(ax, pave, z=2)

    for (x0, x1) in ((0, 6), (13.5, 26)):
        poly(ax, [(x0, -3), (x1, -3), (x1, 0), (x0, 0)], fc=MULCH, ec="#B7A688", lw=0.7, z=3)
    for x in (2.5, 16.5, 20.5, 24):
        shrub(ax, x, -1.6, 1.25)
    ax.plot([0, 34], [0.25, 0.25], color=STONE, lw=3.0, zorder=8.5, solid_capstyle="butt")

    # basement stairwell: landing at gym-floor level + 3 steps down, capped stone side walls
    poly(ax, [(6.5, -4.0), (13.0, -4.0), (13.0, 0), (6.5, 0)], fc="#BAC4CA", ec=SOFT, lw=0.9, z=4)
    ax.plot([7.0, 12.5], [-3.6, -3.6], color=SOFT, lw=0.6, ls=(0, (2, 1.5)), zorder=4.2)
    steps(ax, 6.5, -6.9, 13.0, -4.0, 3, "y", z=4)
    arrow_down(ax, 9.75, -6.5, 9.75, -4.4)
    stone_wall(ax, LineString([(6.05, 0), (6.05, -7.2)]), 0.9)
    stone_wall(ax, LineString([(13.45, 0), (13.45, -7.2)]), 0.9)
    ax.plot([7.6, 12], [0.12, 0.12], color="white", lw=3.2, zorder=9)
    ax.add_patch(Arc((7.6, 0), 4.4, 4.4, theta1=270, theta2=360, color=SOFT, lw=0.7, zorder=9))
    ax.add_patch(Arc((12, 0), 4.4, 4.4, theta1=180, theta2=270, color=SOFT, lw=0.7, zorder=9))

    poly(ax, [(26.8, -12), (35.5, -12), (35.5, -6), (34, -6), (34, 0), (26.8, 0)], fc=MULCH, ec="#B7A688",
         lw=0.7, z=3)
    shrub(ax, 29.5, -3.2, 1.6)
    shrub(ax, 31.8, -8.5, 1.4)
    stone_wall(ax, LineString([(26.4, 0), (26.4, -12)]), 1.2)

    squarestone(ax, WALK, z=4)
    steps(ax, *WALK_STEPS, 3, "y", z=4, fc=SQUARE)
    ax.add_patch(Circle((35.5, -14.3), 1.3, fc="none", ec=SOFT, lw=0.9, ls=(0, (2, 1.4)), zorder=5))
    label(ax, 35.5, -16.6, "septic access", size=6.2, color=SOFT)
    steps(ax, 26, WALL_Y, 30, -12, 4, "x", z=4)
    arrow_down(ax, 29.3, -17.8, 26.6, -17.8)
    # capped stone side walls at both ends of the new flight, and at the existing pool steps
    stone_wall(ax, LineString([(25.8, -12.0), (30.2, -12.0)]), 0.9)
    stone_wall(ax, LineString([(25.8, -23.3), (30.2, -23.3)]), 0.9)
    stone_wall(ax, LineString([(30.2, -23.5), (30.2, -21.0)]), 0.9)
    stone_wall(ax, LineString([(PATIO_E - 0.2, -23.5), (PATIO_E - 0.2, -21.0)]), 0.9)

    lines(ax, WALL_REMOVED, REMOVED, 1.6, 7, ls=(0, (4, 2.5)))
    stone_wall(ax, WALL_KEPT, 1.3)

    pool_and_poolhouse(ax)
    house(ax)

    # walls: pavilion back + west end (retaining), wall from back-east corner to the side-path steps,
    # stair cheeks, short wall to the house corner, new curve that opens the view to the pool
    placed(ax, back_and_west_walls)
    stone_wall(ax, LineString([BE, (-9.5, 1.6)]), 1.5)
    stone_wall(ax, LineString([(-4.6, 0.7), (0, 0.7)]), 1.5)
    stone_wall(ax, LineString([(-9.5, 1.6), (-9.5, -4.4)]), 0.9)
    stone_wall(ax, LineString([(-4.55, 1.6), (-4.55, -4.4)]), 0.9)
    stone_wall(ax, LineString(NEW_CURVE_A), 1.5)
    steps(ax, -9, -4.4, -5, 1.6, 5, "y", z=4)
    arrow_down(ax, -7, 0.6, -7, -3.6)

    pavilion(ax)
    view_line(ax)
    trees_and_ac(ax)

    elev(ax, 20, -29, "0'-0\" pool patio")
    elev(ax, 3, -14.5, "0'-0\" new patio")
    elev(ax, *W(-19.5, -19.8), "+0'-1\" pavilion")
    elev(ax, 31.4, -19.6, "+2'-6\" walk")
    elev(ax, -63, -2, "+3' to +5' side lawn (est.)")
    elev(ax, 14.6, -5.6, "–1'-3\" stairwell landing = gym floor (est.)")

    dim(ax, (19, 0), (19, WALL_Y), "23.5' (measured)", offset_text=-1.6)
    dim(ax, (0, -19.5), (30, -19.5), "30' (measured)", offset_text=1.5)
    pav_dims(ax)

    pav_callouts(ax)
    mid = NEW_CURVE_A[len(NEW_CURVE_A) // 2]
    for n, x, y in [(7, 7, -10), (8, 9.7, 2.3), (9, 28, -9.7), (10, 39.2, -13.2), (11, 6, -23.5),
                    (12, mid[0] - 1.6, mid[1] - 1.6), (13, -11.6, 16.5), (14, -2.4, 12.6), (15, -47, 25),
                    (16, 30.5, -1.4), (17, 52.5, -24)]:
        callout(ax, x, y, n)
    frame(ax)

    items = [
        (1, "Covered pavilion, 22 × 32 ft, turned 55°", "Faces the pool's near corner; shingle gable roof,\nwhite posts on fieldstone bases"),
        (2, "Wood-burning fireplace", "Sight line runs from the hearth to the pool corner"),
        (3, "Grill island + bar seating for 5", "Stools face the cook, backs to the house corner"),
        (4, "Back counter in the stone wall", "Fridge, ice maker, bar sink, storage"),
        (5, "Fireplace lounge", "Two sofas facing across the fire-to-pool view"),
        (6, "Dining for 8", None),
        (7, "New bluestone patio at pool level", "Old wall gone: pool to fireplace is one level"),
        (8, "Basement walkout to gym + bath", "3 steps down into a stone-walled stairwell;\ndrain at the landing, door alarm"),
        (9, "Steps down from the walk (yellow area)", "4 risers, capped stone side walls at both ends"),
        (10, "Square-bluestone walk over septic", "Stays at today's height; tank access kept"),
        (11, "Existing wall removed", "North part only; the wall by the pool house stays"),
        (12, "New fieldstone retaining walls", "Back wall follows the slope; curve in front opens\nthe view to the pool"),
        (13, "Side path from the French doors", "Runs along the house past the AC, then 5 steps\ndown at the corner; side lawn stays open"),
        (14, "AC units kept, screened from the path", None),
        (15, "Swing tree", "Back corner is about 13 ft away; arborist to confirm"),
        (16, "Raised bed at existing grade", None),
        (17, "Septic field: keep clear", "Patio stops in line with the deck stairs"),
    ]
    legend_panel(fig, LEGEND, "Option A — Flat (recommended)",
                 "Everything from the pool to the fireplace on one level.\nPlan view; house at top, pool at bottom.",
                 items)
    key_strip(fig, KEY, ax)
    fig.savefig(out, facecolor=PAPER)
    plt.close(fig)


# ================================================================ OPTION B
def option_b(out):
    fig, ax = setup()
    base_layers(ax)
    septic_field(ax)
    flagstone(ax, POOL_PATIO, z=2)

    pav_poly = Polygon([W(-37.5, 0.7), W(-2.5, 0.7), W(-2.5, -23.5), W(-37.5, -23.5)])
    edge = LineString([W(-2.5, -23.5), W(-37.5, -23.5)])
    xq = edge.intersection(LineString([(-60, -19.5), (0, -19.5)])).x
    link = Polygon([BE, (-9.2, 0.7), (-9.2, 0), (26.8, 0), (26.8, -12), (30, -12), (30, -19.5), (xq, -19.5),
                    W(-2.5, -23.5)])
    terrace = unary_union([pav_poly, link.buffer(0)])
    flagstone(ax, terrace.buffer(0), z=2.5)

    bed = box(-10, WALL_Y, 30, -19.5)
    shp(ax, bed, fc=MULCH, ec="#B7A688", lw=0.7, z=3)
    for x in np.arange(-7.5, 29, 3.4):
        if not (0.5 < x < 11.5):
            ax.add_patch(Circle((x, -21.4), 1.2, fc="#C9C29A", ec="#A39C74", lw=0.6, zorder=3.5))
    stone_wall(ax, EXIST_WALL, 1.3)
    steps(ax, 2, -27.5, 10, -19.5, 4, "y", z=7.5)
    arrow_down(ax, 6, -20.3, 6, -26.6)

    poly(ax, [(0, -3), (26.8, -3), (26.8, 0), (0, 0)], fc=MULCH, ec="#B7A688", lw=0.7, z=3)
    for x in (2.5, 9.5, 16.5, 20.5, 24):
        shrub(ax, x, -1.6, 1.25)
    poly(ax, [(26.8, -12), (35.5, -12), (35.5, -6), (34, -6), (34, 0), (26.8, 0)], fc=MULCH, ec="#B7A688",
         lw=0.7, z=3)
    shrub(ax, 29.5, -3.2, 1.6)

    squarestone(ax, WALK, z=4)
    steps(ax, *WALK_STEPS, 3, "y", z=4, fc=SQUARE)
    ax.add_patch(Circle((35.5, -14.3), 1.3, fc="none", ec=SOFT, lw=0.9, ls=(0, (2, 1.4)), zorder=5))
    label(ax, 35.5, -16.6, "septic access", size=6.2, color=SOFT)

    pool_and_poolhouse(ax)
    house(ax)

    placed(ax, back_and_west_walls, west=False)
    stone_wall(ax, LineString([BE, (-9.2, 0.7)]), 1.5)
    stone_wall(ax, LineString([(-4.8, 0.7), (0, 0.7)]), 1.5)
    steps(ax, -9, -0.2, -5, 1.6, 1, "y", z=4)

    pavilion(ax)
    view_line(ax)
    trees_and_ac(ax)

    elev(ax, 20, -29, "0'-0\" pool patio")
    elev(ax, 3, -14.5, "+2'-6\" terrace")
    elev(ax, *W(-19.5, -19.8), "+2'-7\" pavilion")
    elev(ax, -63, -2, "+3' to +5' side lawn (est.)")

    dim(ax, (19, 0), (19, WALL_Y), "23.5' (measured)", offset_text=-1.6)
    dim(ax, (0, -17.0), (30, -17.0), "30' (measured)", offset_text=1.5)
    pav_dims(ax)

    pav_callouts(ax)
    for n, x, y in [(7, 7, -10), (8, 22.5, -25.8), (9, 11.8, -25.4), (10, 39.2, -13.2), (11, 43.4, -4.6),
                    (12, -2.4, 12.6), (13, -47, 25), (14, -11.6, 16.5), (15, 52.5, -24)]:
        callout(ax, x, y, n)
    frame(ax)

    items = [
        (1, "Covered pavilion, 22 × 32 ft, turned 55°", "Same structure and angle as Option A"),
        (2, "Wood-burning fireplace", None),
        (3, "Grill island + bar seating for 5", None),
        (4, "Back counter in the stone wall", None),
        (5, "Fireplace lounge", None),
        (6, "Dining for 8", None),
        (7, "Raised bluestone terrace at today's grade", "About 2'-6\" above the pool patio, looks down on it"),
        (8, "Existing wall + planting bed kept", "Bed doubles as the safety buffer at the drop"),
        (9, "New steps to the pool", "4 risers, centered on the pool"),
        (10, "Square-bluestone walk over septic", "Unchanged"),
        (11, "Deck stairs land on the terrace level", None),
        (12, "AC units kept, screened from the path", None),
        (13, "Swing tree", "Less digging, easier to keep"),
        (14, "Side path from the French doors", "Along the house past the AC; one step down"),
        (15, "Septic field: keep clear", "Patio stops in line with the deck stairs"),
    ]
    legend_panel(fig, LEGEND, "Option B — Elevated terrace",
                 "Keeps the existing wall; terrace and pavilion sit at\ntoday's lawn level and look down on the pool.",
                 items)
    key_strip(fig, KEY, ax, show_removed=False)
    fig.savefig(out, facecolor=PAPER)
    plt.close(fig)


if __name__ == "__main__":
    print("center", CENTER.round(1), "BW", np.round(BW, 1), "BE", np.round(BE, 1), "FW", np.round(FW, 1),
          "FE", np.round(FE, 1))
    if sys.argv[1] == "a":
        option_a(sys.argv[2])
    else:
        option_b(sys.argv[2])

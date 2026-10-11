"""Schematic site plans for the backyard outdoor-living design.

Coordinates in feet. Origin = southwest corner of the main house (the corner
by the AC units). +x runs east along the house toward the sunroom/deck stairs,
+y runs north into the house. The pool sits to the south (down on the page).
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Polygon as MPoly, Circle, Rectangle, FancyBboxPatch, Arc
from matplotlib.lines import Line2D
from matplotlib.transforms import Affine2D
import matplotlib.patheffects as pe
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, LineString, MultiLineString, Point, box
from shapely.ops import unary_union

for f in fm.findSystemFonts():
    if "Inter" in f:
        fm.fontManager.addfont(f)
plt.rcParams["font.family"] = "Inter"

# ---------------------------------------------------------------- palette
PAPER = "#F6F4EE"
LAWN = "#DDE6CB"
LAWN_DOT = "#BFCDA2"
FLAG = "#CDD5DA"
FLAG_J = "#97A3AB"
SQUARE = "#B9C4CB"
SQUARE_J = "#8C99A2"
POOL = "#9AD3D8"
POOL_E = "#4E8F98"
COPING = "#E7E3D9"
STONE = "#8E877B"
STONE_E = "#4F4A42"
HOUSE = "#E8E2D2"
HOUSE_E = "#6B655A"
MULCH = "#D3C4A8"
SHRUB = "#A8BC88"
SHRUB_E = "#7D9466"
TREE = "#9CB585"
INK = "#2E3A43"
SOFT = "#5C6873"
FURN = "#FFFFFF"
REMOVED = "#C2573C"
ACCENT = "#1F5F6B"

WALL_Y = -23.5  # existing wall line, measured 23.5 ft from house face

rng = np.random.default_rng(7)


def poly(ax, pts, fc, ec="none", lw=0.8, z=1, alpha=1.0, ls="-", hatch=None):
    p = MPoly(pts, closed=True, fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha, ls=ls, hatch=hatch, joinstyle="round")
    ax.add_patch(p)
    return p


def shp(ax, geom, **kw):
    if geom.is_empty:
        return
    geoms = getattr(geom, "geoms", [geom])
    for g in geoms:
        if g.geom_type == "Polygon":
            poly(ax, list(g.exterior.coords), **kw)


def lines(ax, geom, color, lw, z, ls="-", alpha=1.0, cap="round"):
    if geom.is_empty:
        return
    geoms = getattr(geom, "geoms", [geom])
    for g in geoms:
        if g.geom_type == "LineString":
            x, y = g.xy
            ax.plot(x, y, color=color, lw=lw, zorder=z, ls=ls, alpha=alpha, solid_capstyle=cap)
        elif g.geom_type in ("MultiLineString", "GeometryCollection"):
            lines(ax, g, color, lw, z, ls, alpha)


def flagstone(ax, region, z, spacing=2.7):
    """Irregular bluestone: Voronoi joints clipped to region."""
    shp(ax, region, fc=FLAG, z=z)
    minx, miny, maxx, maxy = region.bounds
    xs = np.arange(minx - 4, maxx + 4, spacing)
    ys = np.arange(miny - 4, maxy + 4, spacing * 0.9)
    pts = np.array([(x + rng.uniform(-1, 1) * spacing * 0.45, y + rng.uniform(-1, 1) * spacing * 0.45)
                    for x in xs for y in ys])
    vor = Voronoi(pts)
    segs = []
    for (a, b) in vor.ridge_vertices:
        if a < 0 or b < 0:
            continue
        segs.append((tuple(vor.vertices[a]), tuple(vor.vertices[b])))
    ml = MultiLineString(segs).intersection(region)
    lines(ax, ml, FLAG_J, 0.45, z + 0.1)
    # subtle tonal variation on a few stones
    for p in pts[rng.choice(len(pts), size=len(pts) // 7, replace=False)]:
        pass
    shp(ax, region, fc="none", ec=FLAG_J, lw=0.9, z=z + 0.2)


def squarestone(ax, region, z, w=3.0, h=2.0):
    shp(ax, region, fc=SQUARE, z=z)
    minx, miny, maxx, maxy = region.bounds
    segs = []
    y = miny
    row = 0
    while y <= maxy:
        segs.append(((minx, y), (maxx, y)))
        off = (row % 2) * w / 2
        x = minx - off
        while x <= maxx:
            segs.append(((x, y), (x, y + h)))
            x += w
        y += h
        row += 1
    lines(ax, MultiLineString(segs).intersection(region), SQUARE_J, 0.5, z + 0.1)
    shp(ax, region, fc="none", ec=SQUARE_J, lw=0.9, z=z + 0.2)


def stone_wall(ax, line, width, z=6, ec=STONE_E):
    g = line.buffer(width / 2, cap_style=2, join_style=2)
    shp(ax, g, fc=STONE, ec=ec, lw=0.9, z=z)
    shp(ax, g, fc="none", ec="#B4AC9E", lw=0, z=z + 0.05, hatch="////")
    return g


def steps(ax, x0, y0, x1, y1, n, direction, z=5, fc=FLAG):
    """Rectangle of steps; direction is the axis treads change along: 'x' or 'y'."""
    poly(ax, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fc=fc, ec=FLAG_J, lw=0.9, z=z)
    for i in range(1, n):
        t = i / n
        if direction == "x":
            x = x0 + (x1 - x0) * t
            ax.plot([x, x], [y0, y1], color=SOFT, lw=0.8, zorder=z + 0.1)
        else:
            y = y0 + (y1 - y0) * t
            ax.plot([x0, x1], [y, y], color=SOFT, lw=0.8, zorder=z + 0.1)


def arrow_down(ax, x0, y0, x1, y1, z=9):
    """Small 'down' arrow showing direction of travel down the steps."""
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=SOFT, lw=0.8, mutation_scale=7), zorder=z)


def shrub(ax, x, y, r, z=4):
    ax.add_patch(Circle((x, y), r, fc=SHRUB, ec=SHRUB_E, lw=0.7, zorder=z))
    ax.add_patch(Circle((x - r * 0.25, y + r * 0.25), r * 0.45, fc="#B9CB9A", ec="none", zorder=z + 0.01))


def tree(ax, x, y, r, z=12, dashed=False, alpha=0.33):
    ax.add_patch(Circle((x, y), r, fc=TREE, ec="#6F8A5B", lw=0.9, alpha=alpha, zorder=z,
                        ls="--" if dashed else "-"))
    # canopy lobes
    for k in range(9):
        a = k / 9 * 2 * np.pi
        ax.add_patch(Arc((x + np.cos(a) * r * 0.82, y + np.sin(a) * r * 0.82), r * 0.5, r * 0.5,
                         theta1=np.degrees(a) - 70, theta2=np.degrees(a) + 70,
                         color="#6F8A5B", lw=0.6, alpha=0.7, zorder=z + 0.1))
    ax.add_patch(Circle((x, y), 0.9, fc="#6F5B45", ec="none", zorder=z + 0.2))


def label(ax, x, y, s, size=7.2, color=SOFT, ha="center", va="center", z=20, weight="regular", rot=0,
          style="normal"):
    t = ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, zorder=z, weight=weight, rotation=rot,
                style=style)
    t.set_path_effects([pe.withStroke(linewidth=2.6, foreground=PAPER, alpha=0.9)])
    return t


def callout(ax, x, y, n, z=30):
    ax.add_patch(Circle((x, y), 1.55, fc=INK, ec="white", lw=1.0, zorder=z))
    ax.text(x, y - 0.05, str(n), fontsize=7.4, color="white", ha="center", va="center", zorder=z + 1,
            weight="bold")


def elev(ax, x, y, s, z=22):
    ax.plot([x], [y], marker="D", ms=4.2, mfc="white", mec=ACCENT, mew=1.0, zorder=z)
    label(ax, x + 1.2, y, s, size=6.8, color=ACCENT, ha="left", weight="medium")


def dim(ax, p0, p1, text, offset_text=1.4, z=25, color=INK):
    (x0, y0), (x1, y1) = p0, p1
    ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="<|-|>", color=color, lw=0.8,
                                                     mutation_scale=7, shrinkA=0, shrinkB=0), zorder=z)
    for (x, y) in (p0, p1):
        if x0 == x1:
            ax.plot([x - 0.9, x + 0.9], [y, y], color=color, lw=0.8, zorder=z)
        else:
            ax.plot([x, x], [y - 0.9, y + 0.9], color=color, lw=0.8, zorder=z)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    if x0 == x1:
        t = ax.text(mx - offset_text, my, text, rotation=90, fontsize=7.2, color=color, ha="center",
                    va="center", zorder=z, weight="semibold")
    else:
        t = ax.text(mx, my + offset_text, text, fontsize=7.2, color=color, ha="center", va="center",
                    zorder=z, weight="semibold")
    t.set_path_effects([pe.withStroke(linewidth=3, foreground=PAPER)])


def furniture(ax):
    z = 15
    # fireplace mass on the back wall, protruding behind it
    poly(ax, [(-24.5, -1.2), (-15.5, -1.2), (-15.5, 3.6), (-24.5, 3.6)], fc=STONE, ec=STONE_E, lw=1.1, z=z)
    poly(ax, [(-24.5, -1.2), (-15.5, -1.2), (-15.5, 3.6), (-24.5, 3.6)], fc="none", ec="#B4AC9E", lw=0,
         z=z + 0.05, hatch="////")
    poly(ax, [(-22, -1.2), (-18, -1.2), (-18.6, 0.6), (-21.4, 0.6)], fc="#3B3530", ec=STONE_E, lw=0.8, z=z + 0.1)
    # raised hearth
    poly(ax, [(-25, -3.2), (-15, -3.2), (-15, -1.2), (-25, -1.2)], fc="#BBC5CB", ec=SOFT, lw=0.8, z=z)
    # wood niches
    for x0 in (-27.6, -15.2):
        poly(ax, [(x0, -1.5), (x0 + 2.4, -1.5), (x0 + 2.4, 0), (x0, 0)], fc="#C9B08A", ec=SOFT, lw=0.6, z=z)
    # back counter (fridge, ice, sink) along back wall, kitchen bay
    poly(ax, [(-13.4, -2.6), (-5.2, -2.6), (-5.2, 0), (-13.4, 0)], fc="#E9E6DF", ec=SOFT, lw=0.9, z=z)
    ax.add_patch(Rectangle((-10.6, -2.0), 1.8, 1.3, fc="white", ec=SOFT, lw=0.6, zorder=z + 0.1))  # sink
    # grill island with raised bar ledge on the east side
    poly(ax, [(-10.8, -17.2), (-7.6, -17.2), (-7.6, -6.2), (-10.8, -6.2)], fc="#E9E6DF", ec=SOFT, lw=0.9, z=z)
    poly(ax, [(-7.6, -17.6), (-6.2, -17.6), (-6.2, -5.8), (-7.6, -5.8)], fc="#D8D2C4", ec=SOFT, lw=0.9, z=z)
    ax.add_patch(Rectangle((-10.4, -13.6), 2.4, 3.4, fc="#5E6268", ec=SOFT, lw=0.6, zorder=z + 0.1))  # grill
    for y in (-13.1, -12.4, -11.7, -11.0):
        ax.plot([-10.2, -8.2], [y, y], color="#9AA0A6", lw=0.5, zorder=z + 0.2)
    ax.add_patch(Rectangle((-10.4, -16.4), 2.4, 1.6, fc="white", ec=SOFT, lw=0.6, zorder=z + 0.1))  # side burner
    for y in (-15.6, -13.4, -11.2, -9.0, -6.8):
        ax.add_patch(Circle((-5.15, y), 0.72, fc=FURN, ec=SOFT, lw=0.8, zorder=z))
    # lounge: two sofas facing each other, perpendicular to the fireplace
    for x0 in (-25.8, -17.2):
        ax.add_patch(FancyBboxPatch((x0, -14.6), 3.0, 8.4, boxstyle="round,pad=0,rounding_size=0.6",
                                    fc=FURN, ec=SOFT, lw=0.9, zorder=z))
        back = x0 if x0 < -20 else x0 + 2.2
        ax.add_patch(Rectangle((back, -14.6), 0.8, 8.4, fc="#EEEAE2", ec=SOFT, lw=0.6, zorder=z + 0.1))
        for k in range(3):
            ax.plot([x0, x0 + 3.0], [-14.6 + 2.8 * (k + 1), -14.6 + 2.8 * (k + 1)], color="#C4C9CD",
                    lw=0.5, zorder=z + 0.2) if k < 2 else None
    ax.add_patch(FancyBboxPatch((-21.6, -12.8), 3.2, 5.0, boxstyle="round,pad=0,rounding_size=0.3",
                                fc="#D9CBB2", ec=SOFT, lw=0.8, zorder=z))
    # dining for 8
    ax.add_patch(Rectangle((-32.6, -16.5), 3.4, 9.6, fc="#D9CBB2", ec=SOFT, lw=0.9, zorder=z))
    for y in (-14.9, -11.7, -8.5):
        for x in (-34.6, -28.8):
            ax.add_patch(FancyBboxPatch((x, y - 0.75), 1.6, 1.5, boxstyle="round,pad=0,rounding_size=0.3",
                                        fc=FURN, ec=SOFT, lw=0.8, zorder=z))
    for y in (-18.4, -6.6):
        ax.add_patch(FancyBboxPatch((-31.7, y - 0.75), 1.6, 1.5, boxstyle="round,pad=0,rounding_size=0.3",
                                    fc=FURN, ec=SOFT, lw=0.8, zorder=z))


def pavilion_frame(ax, west_steps=True):
    z = 17
    # roof outline (1.5 ft overhang), ridge line
    ax.add_patch(Rectangle((-37.5, -23.5), 35.0, 25.0, fc="none", ec=INK, lw=1.2, ls=(0, (5, 3)), zorder=z))
    ax.plot([-37.5, -2.5], [-11, -11], color=INK, lw=0.8, ls=(0, (9, 2, 2, 2)), zorder=z)
    # columns: stone bases with white posts
    cols = [(-36, -22), (-26, -22), (-14, -22), (-4, -22), (-4, 0), (-36, 0)]
    if not west_steps:
        cols.append((-36, -11))
    for (x, y) in cols:
        ax.add_patch(Rectangle((x - 1.1, y - 1.1), 2.2, 2.2, fc=STONE, ec=STONE_E, lw=0.9, zorder=z + 1))
        ax.add_patch(Rectangle((x - 0.45, y - 0.45), 0.9, 0.9, fc="white", ec=STONE_E, lw=0.7, zorder=z + 1.1))
    # chimney
    ax.add_patch(Rectangle((-21.8, 0.4), 3.6, 2.6, fc="#6E675C", ec=STONE_E, lw=0.9, zorder=z + 1))


def base_layers(ax):
    ax.add_patch(Rectangle((-90, -100), 220, 150, fc=LAWN, ec="none", zorder=0))
    n = 3400
    px = rng.uniform(XLIM[0], XLIM[1], n)
    py = rng.uniform(YLIM[0], YLIM[1], n)
    ax.scatter(px, py, s=0.6, c=LAWN_DOT, zorder=0.1, linewidths=0)


def shifted(ax, fn, dx, *args, **kw):
    """Draw with fn, then slide everything it drew dx feet east."""
    n_p, n_l = len(ax.patches), len(ax.lines)
    fn(ax, *args, **kw)
    tr = Affine2D().translate(dx, 0) + ax.transData
    for p in ax.patches[n_p:]:
        p.set_transform(tr)
    for l in ax.lines[n_l:]:
        l.set_transform(tr)


DX = -7.0                      # pavilion sits 11 ft past the house corner (room for side-path steps)
PAV_W, PAV_E = -43.0, -11.0    # pavilion column lines
WALL_W = -44.5                 # outer face of west end / back wall start
PATIO_E = 41.0                 # pool patio stops in line with the deck stairs (septic field beyond)


def house(ax):
    z = 8
    main = [(0, 0), (34, 0), (34, 40), (0, 40)]
    sun = [(34, -3), (58, -3), (58, 12), (34, 12)]
    for pts in (main, sun):
        poly(ax, pts, fc=HOUSE, ec=HOUSE_E, lw=1.4, z=z)
        poly(ax, pts, fc="none", ec="#D3CAB3", lw=0, z=z + 0.05, hatch="\\\\\\")
    label(ax, 17, 14, "HOUSE", size=9, color=HOUSE_E, weight="semibold")
    label(ax, 17, 11, "main level above basement gym", size=6.6, color=HOUSE_E)
    label(ax, 46, 4.5, "SUNROOM", size=8, color=HOUSE_E, weight="semibold")
    ax.plot([0, 0], [23, 29], color="white", lw=3.0, zorder=z + 1)
    ax.add_patch(Rectangle((-3.5, 22.5), 3.5, 7, fc=FLAG, ec=FLAG_J, lw=0.8, zorder=z))
    label(ax, 1.6, 26, "French\ndoors", size=6.4, color=HOUSE_E, ha="left")
    ax.add_patch(Rectangle((35, -6), 6, 3, fc="#A88F72", ec=HOUSE_E, lw=0.9, zorder=z))
    steps(ax, 35.5, -12, 40.5, -6, 7, "y", z=z, fc="#C8B497")


def pool_and_poolhouse(ax):
    z = 7
    shp(ax, box(-5, -74, 17, -32), fc=COPING, ec="#B9B3A5", lw=0.8, z=z)
    shp(ax, box(-4, -73, 16, -33), fc=POOL, ec=POOL_E, lw=1.0, z=z + 0.1)
    for k in range(9):
        y = -70 + k * 4.4
        xs = np.linspace(-2.5, 14.5, 40)
        ax.plot(xs, y + 0.35 * np.sin(xs / 1.6 + k), color="#C4E7EA", lw=0.8, zorder=z + 0.2)
    label(ax, 6, -51, "POOL", size=9, color=POOL_E, weight="semibold")
    label(ax, 6, -54, "20 × 40 ft", size=7, color=POOL_E)
    ph = [(-30, -64), (-16.4, -64), (-16.4, -50), (-30, -50)]
    poly(ax, ph, fc=HOUSE, ec=HOUSE_E, lw=1.2, z=z + 1)
    poly(ax, ph, fc="none", ec="#D3CAB3", lw=0, z=z + 1.05, hatch="\\\\\\")
    ax.plot([-16.4, -16.4], [-59, -55], color="white", lw=3.0, zorder=z + 1.2)
    label(ax, -23.2, -57, "POOL\nHOUSE", size=7, color=HOUSE_E, weight="semibold")


def septic_field(ax):
    ax.add_patch(FancyBboxPatch((44, -66), 22, 50, boxstyle="round,pad=0,rounding_size=4", fc="#E4E9D3",
                                ec="#9C7F5A", lw=1.1, ls=(0, (4, 2.5)), zorder=1))
    label(ax, 52.5, -38, "SEPTIC FIELD\n(approx.)\nkeep clear:\nno patio,\nno equipment", size=6.8,
          color="#7A6244", weight="medium")


EXIST_WALL = LineString([(30, WALL_Y), (-10, WALL_Y), (-13.5, -25.0), (-15.6, -28.0), (-16.6, -32.0),
                         (-16.6, -50.0)])
WALL_REMOVED_A = LineString([(30, WALL_Y), (-10, WALL_Y), (-13.5, -25.0), (-15.6, -28.0), (-16.6, -32.0),
                             (-16.6, -37.0)])
WALL_KEPT_A = LineString([(-16.6, -37.0), (-16.6, -50.0)])

POOL_PATIO = Polygon([(-10, WALL_Y), (PATIO_E, WALL_Y), (PATIO_E, -80), (-16, -80), (-16, -32.0),
                      (-15.6, -28.0), (-13.5, -25.0)])

WALK = box(30, -21, PATIO_E, -12)
WALK_STEPS = (30, -23.5, PATIO_E, -21)

PATH = unary_union([box(-9, 1.6, -5, 29.5), box(-9, 22.5, -3.5, 29.5)])


def trees_and_ac(ax):
    for y0 in (2.0, 5.6):
        ax.add_patch(Rectangle((-4.2, y0), 3.2, 3.0, fc="#C9CCCF", ec=SOFT, lw=0.9, zorder=9))
        ax.add_patch(Circle((-2.6, y0 + 1.5), 1.1, fc="none", ec=SOFT, lw=0.6, zorder=9.1))
    # slatted screen between the AC units and the side path
    ax.plot([-4.65, -4.65, 0], [1.6, 10.4, 10.4], color=HOUSE_E, lw=2.2, zorder=9.2, solid_capstyle="butt")
    ax.plot([-4.65, -4.65, 0], [1.6, 10.4, 10.4], color="white", lw=1.0, zorder=9.3, ls=(0, (1.2, 1.2)))
    squarestone(ax, PATH, z=3, w=2.4, h=2.0)
    shrub(ax, -11.2, 6.0, 1.6)
    shrub(ax, -11.0, 10.4, 1.5)
    tree(ax, -37, 16, 13, dashed=True)
    label(ax, -37, 11.6, "swing tree", size=6.6, color="#4E6B3E", weight="medium")
    tree(ax, -64, -32, 13)
    tree(ax, -60, -64, 14)
    tree(ax, 55, 26, 12)


def pavilion_common(ax):
    shifted(ax, furniture, DX)
    shifted(ax, pavilion_frame, DX, west_steps=False)


def legend_panel(fig, rect, title, subtitle, items):
    W, H = fig.get_size_inches()
    lw_in, lh_in = rect[2] * W, rect[3] * H
    lax = fig.add_axes(rect)
    lax.set_axis_off()
    lax.set_xlim(0, lw_in)
    lax.set_ylim(0, lh_in)
    y = lh_in - 0.05
    lax.text(0, y, title, fontsize=16, weight="bold", color=INK, va="top")
    y -= 0.42
    lax.text(0, y, subtitle, fontsize=8.6, color=SOFT, va="top", linespacing=1.45)
    y -= 0.62
    lax.plot([0, lw_in], [y + 0.18, y + 0.18], color="#D8D3C7", lw=0.8)
    for n, head, body in items:
        lax.plot([0.14], [y - 0.075], marker="o", ms=15, mfc=INK, mec="none")
        lax.text(0.14, y - 0.078, str(n), fontsize=7.4, color="white", ha="center", va="center",
                 weight="bold")
        lax.text(0.36, y, head, fontsize=8.8, color=INK, va="top", weight="semibold")
        if body:
            lax.text(0.36, y - 0.19, body, fontsize=7.8, color=SOFT, va="top", linespacing=1.35)
            y -= 0.19 + 0.16 * body.count("\n")
        y -= 0.40
    return lax


def key_strip(fig, rect, ax, show_removed=True):
    W, H = fig.get_size_inches()
    kw, kh = rect[2] * W, rect[3] * H
    kax = fig.add_axes(rect)
    kax.set_axis_off()
    kax.set_xlim(0, kw)
    kax.set_ylim(0, kh)
    items = [("swatch", FLAG, "Irregular bluestone (matches pool)"),
             ("swatch", SQUARE, "Square-cut bluestone"),
             ("swatch", STONE, "Fieldstone wall, bluestone cap"),
             ("swatch", MULCH, "Planting bed"),
             ("dash", INK, "Pavilion roof edge"),
             ("diamond", ACCENT, "Spot elevation (pool patio = 0'-0\")")]
    if show_removed:
        items.insert(5, ("dash", REMOVED, "Existing wall to be removed"))
    cols = 4
    colw = 2.55
    for i, (kind, c, t) in enumerate(items):
        cx = 0.05 + (i % cols) * colw
        cy = kh - 0.22 - (i // cols) * 0.3
        if kind == "swatch":
            kax.add_patch(Rectangle((cx, cy - 0.08), 0.32, 0.16, fc=c, ec=STONE_E, lw=0.6))
        elif kind == "dash":
            kax.plot([cx, cx + 0.32], [cy, cy], color=c, lw=1.5, ls=(0, (4, 2)))
        else:
            kax.plot([cx + 0.16], [cy], marker="D", ms=5, mfc="white", mec=c, mew=1.0)
        kax.text(cx + 0.45, cy, t, fontsize=7.8, color=SOFT, va="center")
    # scale bar (1 ft in plan -> inches)
    p0 = ax.transData.transform((0, 0)); p1 = ax.transData.transform((1, 0))
    ft = (p1[0] - p0[0]) / fig.dpi
    sx, sy = 0.05, kh - 0.95
    for i in range(4):
        kax.add_patch(Rectangle((sx + i * 5 * ft, sy), 5 * ft, 0.07, fc=INK if i % 2 == 0 else "white",
                                ec=INK, lw=0.7))
        kax.text(sx + i * 5 * ft, sy - 0.06, f"{i*5}", fontsize=7, color=SOFT, ha="center", va="top")
    kax.text(sx + 20 * ft, sy - 0.06, "20 ft", fontsize=7, color=SOFT, ha="center", va="top")
    kax.text(sx + 20 * ft + 0.5, sy + 0.03,
             "Schematic only. Measured: 23.5 ft house to wall, 30 ft walk to house corner, 20 \u00d7 40 ft pool, "
             "27\u201333 in wall, 45 in floor to sill.\nEverything else is estimated from photos; a survey sets final "
             "dimensions and elevations before pricing.",
             fontsize=7.4, color=SOFT, va="center", linespacing=1.45, style="italic")


XLIM = (-68, 62)
YLIM = (-84, 32)


def setup():
    fig = plt.figure(figsize=(18.5, 12.6), dpi=170)
    fig.patch.set_facecolor(PAPER)
    ax = fig.add_axes([0.012, 0.105, 0.635, 0.885], anchor="N")
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal")
    ax.set_axis_off()
    return fig, ax


def frame(ax):
    ax.add_patch(Rectangle((XLIM[0], YLIM[0]), XLIM[1] - XLIM[0], YLIM[1] - YLIM[0], fc="none", ec=INK,
                           lw=1.4, zorder=50))


def common_dims(ax, y30):
    dim(ax, (19, 0), (19, WALL_Y), "23.5' (measured)", offset_text=-1.6)
    dim(ax, (0, y30), (30, y30), "30' (measured)", offset_text=1.5)
    dim(ax, (PAV_W, -26.0), (PAV_E, -26.0), "32'", offset_text=1.5)
    dim(ax, (-51, 0), (-51, -22), "22'", offset_text=1.6)
    for y in (0, -22):
        ax.plot([WALL_W - 1, -52], [y, y], color=INK, lw=0.5, zorder=24, ls=(0, (1, 1.5)))


LEGEND = [0.665, 0.02, 0.325, 0.96]
KEY = [0.012, 0.0, 0.635, 0.1]


# ================================================================ OPTION A
NEW_CURVE = [(WALL_W, -22), (-44.2, -26), (-42.5, -30), (-39, -33.3), (-33.5, -35.5), (-26, -36.6),
             (-16.6, -37.0)]


def option_a(out):
    fig, ax = setup()
    base_layers(ax)
    septic_field(ax)

    apron = Polygon(NEW_CURVE + [(-10, WALL_Y), (WALL_W, WALL_Y)])
    pave = unary_union([POOL_PATIO, box(WALL_W, WALL_Y, 26, 0), apron.buffer(0)])
    pave = pave.difference(box(26, -12, 80, 0)).difference(box(30, WALL_Y, 80, -12))
    pave = pave.intersection(box(-80, -90, PATIO_E, 0))
    flagstone(ax, pave, z=2)

    for (x0, x1) in ((0, 6), (13.5, 26)):
        poly(ax, [(x0, -3), (x1, -3), (x1, 0), (x0, 0)], fc=MULCH, ec="#B7A688", lw=0.7, z=3)
    for x in (2.5, 16.5, 20.5, 24):
        shrub(ax, x, -1.6, 1.25)
    ax.plot([0, 34], [0.25, 0.25], color=STONE, lw=3.0, zorder=8.5, solid_capstyle="butt")

    poly(ax, [(6, -4.8), (13.5, -4.8), (13.5, 0), (6, 0)], fc="#BAC4CA", ec=SOFT, lw=0.9, z=4)
    ax.plot([6.6, 12.9], [-4.4, -4.4], color=SOFT, lw=0.6, ls=(0, (2, 1.5)), zorder=4.2)
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

    lines(ax, WALL_REMOVED_A, REMOVED, 1.6, 7, ls=(0, (4, 2.5)))
    stone_wall(ax, WALL_KEPT_A, 1.3)

    pool_and_poolhouse(ax)
    house(ax)

    # pavilion walls: back wall (retaining), solid west end, new curve; side-path stair at the house corner
    stone_wall(ax, LineString([(WALL_W, 0.7), (-9.6, 0.7)]), 1.5)
    stone_wall(ax, LineString([(-4.6, 0.7), (0, 0.7)]), 1.5)
    stone_wall(ax, LineString([(-43.7, 0.7), (-43.7, -22)]), 1.5)
    stone_wall(ax, LineString(NEW_CURVE), 1.5)
    stone_wall(ax, LineString([(-9.5, 1.6), (-9.5, -4.4)]), 0.9)
    stone_wall(ax, LineString([(-4.55, 1.6), (-4.55, -4.4)]), 0.9)
    steps(ax, -9, -4.4, -5, 1.6, 5, "y", z=4)
    arrow_down(ax, -7, 0.6, -7, -3.6)

    pavilion_common(ax)
    trees_and_ac(ax)

    elev(ax, 20, -29, "0'-0\" pool patio")
    elev(ax, 3, -14.5, "0'-0\" new patio")
    elev(ax, -32.5, -20.6, "+0'-1\" pavilion")
    elev(ax, 31.4, -19.6, "+2'-6\" walk")
    elev(ax, -30, 7.6, "+3' to +5' side lawn (est.)")
    elev(ax, 7.4, -6.3, "–0'-9\" walkout landing (est.)")

    common_dims(ax, -19.5)

    C = [(1, -37.5, 3.6), (2, -27, 5.6), (3, -19.3, -19.2), (4, -16.4, -4.3), (5, -27, -16.6),
         (6, -38, -3.6), (7, 7, -10), (8, 9.7, 2.3), (9, 28, -9.7), (10, 39.2, -13.2), (11, 6, -23.5),
         (12, -41.2, -31.2), (13, -11.6, 16.5), (14, -2.4, 12.6), (15, -47, 25), (16, 30.5, -1.4),
         (17, 52.5, -24)]
    for n, x, y in C:
        callout(ax, x, y, n)
    frame(ax)

    items = [
        (1, "Covered pavilion, 22 × 32 ft", "Shingle gable roof, white posts on fieldstone bases"),
        (2, "Wood-burning fireplace", "Fieldstone, raised bluestone hearth, wood niches"),
        (3, "Grill island + bar seating for 5", "Stools face the cook, backs to the house corner"),
        (4, "Back counter in the stone wall", "Fridge, ice maker, bar sink, storage"),
        (5, "Fireplace lounge", "Two sofas facing across the fire-to-pool view"),
        (6, "Dining for 8", None),
        (7, "New bluestone patio at pool level", "Old wall gone: pool to fireplace is one level"),
        (8, "Basement walkout to gym + bath", "1–2 steps down, trench drain, door alarm"),
        (9, "Wrap-around steps (yellow area)", "4 risers up to the square-bluestone walk"),
        (10, "Square-bluestone walk over septic", "Stays at today's height; tank access kept"),
        (11, "Existing wall removed", "North part only; the wall by the pool house stays"),
        (12, "New fieldstone retaining walls", "Pavilion back + west walls and a curve that opens\nthe view to the pool"),
        (13, "Side path from the French doors", "Runs along the house past the AC, then 5 steps\ndown at the corner; side lawn stays open"),
        (14, "AC units kept, screened from the path", None),
        (15, "Swing tree", "Keep if arborist clears the dig"),
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
    terrace = Polygon([(WALL_W, 0), (26.8, 0), (26.8, -12), (30, -12), (30, -19.5), (-10, -19.5), (-10, -22),
                       (WALL_W, -22)])
    flagstone(ax, terrace, z=2.5)

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

    stone_wall(ax, LineString([(WALL_W, 0.7), (-9.2, 0.7)]), 1.5)
    stone_wall(ax, LineString([(-4.8, 0.7), (0, 0.7)]), 1.5)
    steps(ax, -9, -0.2, -5, 1.6, 1, "y", z=4)

    pavilion_common(ax)
    trees_and_ac(ax)

    elev(ax, 20, -29, "0'-0\" pool patio")
    elev(ax, 3, -14.5, "+2'-6\" terrace")
    elev(ax, -32.5, -20.6, "+2'-7\" pavilion")
    elev(ax, -30, 7.6, "+3' to +5' side lawn (est.)")

    common_dims(ax, -17.0)

    C = [(1, -37.5, 3.6), (2, -27, 5.6), (3, -19.3, -19.2), (4, -16.4, -4.3), (5, -27, -16.6),
         (6, -38, -3.6), (7, 7, -10), (8, 22.5, -25.8), (9, 11.8, -25.4), (10, 39.2, -13.2),
         (11, 43.4, -4.6), (12, -2.4, 12.6), (13, -47, 25), (14, -11.6, 16.5), (15, 52.5, -24)]
    for n, x, y in C:
        callout(ax, x, y, n)
    frame(ax)

    items = [
        (1, "Covered pavilion, 22 × 32 ft", "Same structure as Option A"),
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
    which = sys.argv[1]
    if which == "a":
        option_a(sys.argv[2])
    else:
        option_b(sys.argv[2])

from sheets import *
from config import *

f = tf_local_to_world()
uhat = np.array([np.cos(np.radians(FRONT_BEARING)), np.sin(np.radians(FRONT_BEARING))]); vhat = np.array([-uhat[1], uhat[0]])
def _dir(deg): return np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg))])
PW = np.array([0.0, 0.0]); PE = PW + FRONT_LEN * _dir(FRONT_BEARING)
NE = PE + EAST_LEN * _dir(EAST_DIR); NWc = NE + BACK_LEN * _dir(BACK_DIR)
LOT = Polygon([tuple(PW), tuple(PE), tuple(NE), tuple(NWc)])
EAST = LineString([tuple(PE), tuple(NE)]); WEST = LineString([tuple(NWc), tuple(PW)])
FRONT = LineString([tuple(PW), tuple(PE)])

def W2(pts): return [f(p) for p in pts]

new_pave = OUTLINE.difference(POOL_PATIO)
roof = Polygon(ROOF)
print("lot", round(LOT.area), "new paving (incl pavilion floor)", round(new_pave.area), "roof", round(roof.area))
dE = min(Point(f(p)).distance(EAST) for p in ROOF)
dHouseE = Point(f((0, 0))).distance(EAST)
print("pavilion to east line", round(dE, 1), "house corner to east", round(dHouseE, 1))

def draw_world(ax, detail):
    G(ax, LOT, fc="white", ec=INK, lw=1.6, z=1, ls=(0, (12, 3, 2, 3)))
    # front setback line 60'
    a = PW + FRONT_SETBACK * vhat - 40 * uhat; b = PE + FRONT_SETBACK * vhat + 40 * uhat
    sb = LineString([tuple(a), tuple(b)]).intersection(LOT)
    L(ax, list(sb.coords), color=RED, lw=0.9, ls=(0, (6, 3)), z=2)
    pave = Polygon(W2(list(PAVE.exterior.coords))) if PAVE.geom_type == "Polygon" else None
    G(ax, Polygon(W2(list(POOL_PATIO.exterior.coords))), fc=FILL, ec=MID, lw=0.6, z=2)
    G(ax, Polygon(W2(list(OUTLINE.exterior.coords))), fc="#F6E2B8", ec=ORANGE, lw=1.0, z=3)
    for pts in (HOUSE, SUNROOM):
        P(ax, W2(pts), fc="white", ec=INK, lw=1.2, z=5, hatch="////")
    P(ax, W2(list(box(-5, -74, 17, -32).exterior.coords)), fc=WATER, ec=INK, lw=0.8, z=4)
    P(ax, W2([(-30, -64), (-16.4, -64), (-16.4, -50), (-30, -50)]), fc="white", ec=INK, lw=0.8, z=5, hatch="////")
    P(ax, W2(ROOF), fc="#F0C27A", ec=ORANGE, lw=1.2, z=6)
    P(ax, W2([(44, -66), (66, -66), (66, -16), (44, -16)]), ec=MID, lw=0.7, ls=(0, (4, 3)), z=2)
    if detail:
        c = np.mean(W2(ROOF), axis=0); T(ax, c[0], c[1], "NEW\nPAVILION", size=6.5, weight="bold", color=ORANGE)
        c = np.mean(W2(HOUSE), axis=0); T(ax, c[0], c[1], "HOUSE", size=7, weight="bold", color=MID)
        c = np.mean(W2([(-4, -73), (16, -33)]), axis=0); T(ax, c[0], c[1], "POOL", size=6.5, color=MID)
        c = np.mean(W2([(44, -66), (66, -16)]), axis=0); T(ax, c[0], c[1], "septic\nfield\n(approx.)", size=6, color=MID)
        c = np.array(f((10, -12))); T(ax, c[0], c[1], "new patio\n(orange)", size=6, color=ORANGE)

# whole lot
fig, frame = new_sheet("L-001", "Base plan and\nsite analysis", "Lot plan and enlarged plan: graphic only, use dimensions",
    notes=("1. " + SURVEY_NOTE + "\n"
           "2. House placed by survey offsets\n   (see survey). New work placed\n"
           "   from site measurements; accuracy\n   about +/- 2 ft until staked.\n"
           "3. Survey shows no contours, septic\n   or utilities: order a topographic\n   survey of the rear yard.\n"
           "4. Zone and side/rear setbacks to be\n   confirmed with the town zoning\n   officer (see permits list)."))
allpts = np.array(W2(HOUSE + SUNROOM + [(-5, -74), (17, -74), (-30, -64), (66, -66), (66, -16)] + ROOF + list(OUTLINE.exterior.coords)))
mn, mx = allpts.min(0) - 22, allpts.max(0) + 22
side = max(mx - mn); cx, cy = (mn + mx) / 2
WIN = (cx - side / 2, cx + side / 2, cy - side / 2, cy + side / 2)
lb = np.array(LOT.bounds)
ax1 = plan_axes(fig, (lb[0] - 30, lb[2] + 30), (lb[1] - 30, lb[3] + 30), rect=(0.03, 0.06, 0.30, 0.88))
draw_world(ax1, False)
m = (PW + PE) / 2 - 22 * vhat; T(ax1, m[0], m[1], STREET_NAME, size=6.5, rot=FRONT_BEARING, color=MID, weight="semibold")
cen = np.array(LOT.centroid.coords[0]); T(ax1, cen[0], cen[1] + 60, f"{LOT_LABEL}\n{LOT.area:,.0f} sq ft\n({LOT.area/43560:.2f} ac)", size=7, weight="bold")
m = PW + FRONT_SETBACK * vhat + 40 * uhat; T(ax1, m[0], m[1] + 14, f"{FRONT_SETBACK:.0f}' front setback", size=5.5, color=RED, rot=FRONT_BEARING)
ax1.annotate("", xy=(lb[0] + 20, lb[3]), xytext=(lb[0] + 20, lb[3] - 80), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2, mutation_scale=14))
T(ax1, lb[0] + 20, lb[3] + 18, "N", size=9, weight="bold")
P(ax1, [(WIN[0], WIN[2]), (WIN[1], WIN[2]), (WIN[1], WIN[3]), (WIN[0], WIN[3])], ec=BLUE, lw=0.9, ls=(0, (3, 2)), z=7)
T(ax1, (WIN[0] + WIN[1]) / 2, WIN[3] + 14, "enlarged at right", size=6, color=BLUE)

ax2 = plan_axes(fig, (WIN[0], WIN[1]), (WIN[2], WIN[3]), rect=(0.34, 0.06, 0.43, 0.88))
draw_world(ax2, True)
# dims: house corner to east line, pavilion to east line
hc = np.array(f((0, 0)))
foot = hc + float(EAST.distance(Point(hc))) * uhat
dimline(ax2, hc, foot, "to east line (survey)", off=-6)
pv = min(W2(ROOF), key=lambda p: Point(p).distance(EAST)); pv = np.array(pv)
foot2 = np.array(EAST.interpolate(EAST.project(Point(pv))).coords[0])
dimline(ax2, pv, foot2, f"about {dE:.0f}' to east line", off=3, color=ORANGE)
hf = np.array(f((17, 40))); foot3 = np.array(FRONT.interpolate(FRONT.project(Point(hf))).coords[0])

G(ax2, LOT, fc="none", ec=INK, lw=1.6, z=9, ls=(0, (12, 3, 2, 3)))
em = np.array(EAST.interpolate(EAST.project(Point(hc))).coords[0]); T(ax2, em[0] - 14, em[1] + 60, "EAST\nLINE", size=6.5, color=MID)
ax2.annotate("", xy=(WIN[0] + 12, WIN[3] - 6), xytext=(WIN[0] + 12, WIN[3] - 30), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2, mutation_scale=12))
T(ax2, WIN[0] + 12, WIN[3] - 2, "N", size=8, weight="bold")

tbl = ("SITE DATA (estimates)\n"
       f"Lot area                      {LOT.area:,.0f} sq ft\n"
       f"New paving incl. pavilion floor  {new_pave.area:,.0f} sq ft\n"
       f"Pavilion roof                    {roof.area:,.0f} sq ft\n"
       f"All accessory bldgs (pavilion,\n  pool house, tree house)      about 1,150 sq ft\n"
       f"  check town limit on accessory bldgs\n"
       f"Pavilion to east line         about {dE:.0f} ft\n"
       f"  must meet principal side setback\n  — confirm with zoning officer")
frame.text(13.5, 4.95, tbl, fontsize=6.6, family="DejaVu Sans Mono", color=INK, va="top",
           bbox=dict(fc="white", ec=INK, lw=0.6, pad=5))
fig.savefig("L-001.png", facecolor=PAPER); print("ok")

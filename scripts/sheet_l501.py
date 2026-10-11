from sheets import *
fig, frame = new_sheet("L-501", "Lighting and\nutilities plan", "Graphic only — see lighting schedule",
    notes=("1. All fixtures 2700K, dimmable, low-\n   voltage where possible; shielded per\n   town rules (no glare past lot line).\n"
           "2. New 60A outdoor subpanel fed from\n   house panel; GFCI on all circuits.\n"
           "3. Gas: size line for grill + side burner\n   + existing pool heater together\n   (plumber to confirm meter capacity).\n"
           "4. Bar sink drains to dry well, not\n   septic, unless septic designer\n   approves. Winter shutoff + drain.\n"
           "5. Spare 1\" conduit to pavilion for\n   speakers, heaters, Wi-Fi.\n"
           "6. Call 811 before any digging."))
ax = plan_axes(fig, (-66, 66), (-82, 34))
base_context(ax); site_steps(ax); site_walls(ax); pavilion_outline(ax); kitchen_furniture(ax)
def fx(p, code, col):
    ax.add_patch(Circle(p, 0.9, fc=col, ec=INK, lw=0.6, zorder=40))
    T(ax, p[0] + 1.2, p[1] + 1.0, code, size=5.4, color=col, ha="left", z=41, weight="bold")
YEL = "#C9A100"
for x in (27, 29): 
    for y in (-14.5, -17.5, -20.5): fx((x, y), "S1", YEL)
for (x, y) in [(8, -5.5), (11.5, -5.5)]: fx((x, y), "S1", YEL)
for (x, y) in [(-7, -1.5), (-7, 0.8)]: fx((x, y), "S1", YEL)
for i in range(6): fx((-7, 4 + i * 4.3), "P1", YEL)
for lp in [(-30, -6), (-20, -6), (-10, -6), (-30, -16), (-20, -16), (-10, -16)]: fx(W(*lp), "D1", YEL)
for lp in [(-25, -11), (-15, -11)]: fx(W(*lp), "F1", MID)
for lp in [(-36, -22), (-4, -22), (-36, 0), (-4, 0)]: fx(W(*lp), "C1", YEL)
fx(W(-20, -2.5), "U1", YEL); fx((-37, 22), "U2", YEL); fx((-37, 10), "U2", YEL)
fx((7.6, 1.0), "W1", YEL)
# utilities
L(ax, [(2, 0.5), (2, -2.5), (-3, -6), W(-8, -2)], color=RED, lw=1.6, ls=(0, (6, 2)), z=20)
T(ax, -1, -7.5, "E: 1-1/4\" conduit to\npavilion subpanel", size=5.6, color=RED)
ax.add_patch(Rectangle((1.2, 0.2), 1.6, 1.0, fc=RED, ec=INK, zorder=21)); T(ax, 3.5, 2.4, "SP", size=5.6, color=RED, weight="bold")
L(ax, [(-14, 26), (-14, 6), W(-6, 4), W(-8, -2.5)], color=ORANGE, lw=1.6, ls=(0, (2, 2)), z=20)
T(ax, -17, 18, "G: gas from\nexisting meter\n(swing-tree side)", size=5.6, color=ORANGE, rot=90)
L(ax, [(16, 0.5), (16, -3), (-2, -9), W(-9, -3)], color=BLUE, lw=1.4, ls=(0, (8, 2, 2, 2)), z=20)
T(ax, 14, -10.5, "W: 3/4\" water to bar sink\n(frost-free, drain-down)", size=5.6, color=BLUE)
north_arrow_local(ax, 58, 22)
lg = ("FIXTURE KEY\nS1 step/riser light (10)\nP1 path light (6)\nD1 recessed downlight (6)\nF1 ceiling fan + light (2)\n"
      "C1 column sconce (4)\nU1 fireplace wash (1)\nU2 tree uplight (2)\nW1 door wall light (1)\n"
      "─ ─ E electric   ··· G gas\n─·─ W water     SP subpanel")
frame.text(0.6, 2.6, lg, fontsize=6.3, family="DejaVu Sans Mono", color=INK, va="top", bbox=dict(fc="white", ec=INK, lw=0.6, pad=5))
fig.savefig("L-501.png", facecolor=PAPER); print("ok")

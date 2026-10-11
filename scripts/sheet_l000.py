from sheets import *
from config import *
from PIL import Image
fig, frame = new_sheet("L-000", "Cover sheet and\ndrawing index", "",
    notes=("Prepared with AI assistance from owner\nphotos, owner measurements and the\nproperty boundary survey. It is a design-\n"
           "development set to communicate intent\nand get comparable bids. It does not\nreplace a licensed landscape architect,\n"
           "architect or engineer. Hand this set\nto one to finish the construction\ndocuments and permit drawings."))
frame.text(0.7, 10.2, "BACKYARD OUTDOOR LIVING", fontsize=22, weight="bold", color=INK, va="top")
frame.text(0.7, 9.6, SITE_LINE + "  —  " + LOT_LABEL, fontsize=11, color=MID, va="top")
frame.text(0.7, 9.2, "Design development set  ·  Option A: flat patio, angled pavilion with fireplace and outdoor kitchen", fontsize=10, color=MID, va="top")
img = Image.open(COVER_RENDER)
ia = fig.add_axes([0.04, 0.24, 0.46, 0.55]); ia.imshow(img); ia.set_axis_off()
frame.text(0.7, 2.45, "Concept rendering — illustrative only; drawings govern dimensions and levels.", fontsize=7.5, color=MID, style="italic")
idx = [("L-000", "Cover sheet and drawing index"), ("L-001", "Base plan and site analysis (on property survey)"),
       ("L-101", "Layout and dimension plan, staking points"), ("L-201", "Grading and drainage plan"),
       ("L-301", "Pavilion elevations and roof plan"), ("L-401", "Planting plan"),
       ("L-501", "Lighting and utilities plan"), ("L-601", "Construction details (typical)"),
       ("Doc", "Schedules, scope of work, bid form, permits, budget")]
frame.text(9.0, 8.4, "DRAWING INDEX", fontsize=10, weight="bold", color=INK, va="top")
for i, (n, t) in enumerate(idx):
    y = 7.95 - i * 0.42
    frame.text(9.0, y, n, fontsize=9, weight="bold", color=INK, va="top"); frame.text(9.75, y, t, fontsize=8.5, color=INK, va="top")
    frame.plot([9.0, 13.1], [y - 0.3, y - 0.3], color=LIGHT, lw=0.6)
frame.text(9.0, 3.9, "BEFORE BIDDING, ORDER", fontsize=9, weight="bold", color=INK, va="top")
frame.text(9.0, 3.6, "1. Topographic survey of rear yard (ask the surveyor who\n    did your boundary survey)\n"
           "2. Septic location (tank, lines, field)\n3. Zoning check with the town\n4. Structural engineer for walls, foundation\n    opening, pavilion and fireplace",
           fontsize=8, color=INK, va="top", linespacing=1.4)
fig.savefig("L-000.png", facecolor=PAPER); print("ok")

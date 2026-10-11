---
name: backyard-design
description: Guide a homeowner from photos and measurements to a backyard or landscape renovation plan: options, renderings, a drawing set, budget, bid form and permits list.
---

# Backyard Design

Act as a landscape architect working with a homeowner. Take them from "here's my yard and an idea" to a design-development package they can price with contractors or hand to a licensed professional, so nobody has to start from scratch.

The work runs in seven stages. Keep the homeowner in the loop at the end of each one: show what you produced and ask what's wrong before moving on. Most of the value comes from the questions you ask and the corrections they give you.

## Ground rules

- **Say what you can and can't do, early and plainly.** You produce concept and design-development drawings, not sealed construction drawings. Retaining walls over about 4 ft, foundation cuts, roofed structures and their footings, fireplaces and chimneys, gas lines and septic work need a licensed engineer or architect. Every sheet says so.
- **Label every number by its source:** measured by the homeowner, taken from a survey, or estimated by you. Never present an estimate as a measurement.
- **Restate before you design.** Rewrite the idea in your own words and ask them to confirm. Markup colors and phrases like "the wall" are often ambiguous.
- **Give a professional opinion, and change it when the facts change.**
- **Ask only what changes the design.** Batch and number questions so they can answer by number; say why each matters when it isn't obvious.
- **Keep one living plan document** with decisions, open questions, drawings and budget. Update it after every round.

## Stage 1. Intake

Ask for one wide photo of the area, a marked-up copy ("red = new patio, blue = covered area"), and a short description: how they want to use the space, what must stay, what they're unsure about. Restate the idea and the options they're weighing, and ask them to confirm.

## Stage 2. Photos from defined angles

Give a numbered shot list with exactly where to stand and which way to face, and ask them to number photos to match:

1. From the far side of the area looking back at the house, whole space in frame.
2. From where the main new feature will go, looking back at the house.
3. Each retaining wall or level change, with a tape measure held against it at its tallest and shortest points.
4. Each slope, from the high point looking down and the low point looking up.
5. Along the house foundation: windows, doors, AC units, downspouts.
6. From an upstairs window, straight down and across the area. This becomes the main overview rendering.
7. Existing details to copy: steps, wall caps, stone, column bases.
8. Side yards and approach paths.

## Stage 3. Measurements and design questions

Ask for a short list of measurements and say what each decides: height of every wall or level change at both ends; house to the main feature; length of the area; pool size and orientation; distances to property lines and big trees. For any basement walkout, ask for basement floor to window sill **and** sill to outside ground; both are needed.

Design questions: structure style and size, roof to match which building, wood or gas fireplace and which way it faces, kitchen and bar layout, what stays or goes, stone matching, gas, water and electric availability, AC units, budget range, phasing. **Always ask where the septic tank, lines and field are**, plus other buried utilities.

Show the step math. Example: floor 45 in. below sill, sill at grade, cut 27–33 in., so the floor sits 14–21 in. below the new patio: 3 steps of 5–7 in.

## Stage 4. The survey

Ask whether they have a property survey (often a PDF from the home purchase). If so: rasterize it and crop the house area at about 300 dpi; extract lot area, line bearings and lengths, setback lines, house offsets and north; rebuild the lot polygon, place the house by its offsets and the new work by measurements; recompute distances to property lines (a survey can move a structure). Most purchase surveys have no contours, septic or utilities, so recommend a topographic survey. Look up the town's accessory-structure setbacks, coverage limits and accessory-building limits; if they aren't online, put "confirm with zoning officer" on the permit list.

## Stage 5. Concept options and site plans

Draw two options as dimensioned plans (Python, matplotlib, shapely) with numbered callouts, a grade section through the critical spot with people for scale, and a trade-off table: feel, excavation, walls, drainage, access, trees, relative cost. Recommend one.

Conventions: origin at a house corner, x along the wall, y away from it; build angled structures in local coordinates and place them with an affine transform; draw irregular flagstone as clipped Voronoi cells and square stone as a running bond. Look at every render and fix overlaps before showing it. Expect rounds of corrections (pool orientation, patio limits at the septic field, path routes, structure angle) and redraw each time.

## Stage 6. Photoreal concept renderings

- **Edit the homeowner's photos** (image-edit mode with their photo as the reference) so the real house, pool and trees stay. Ask which image model they prefer; in the original project, OpenAI-family models followed edits better than Gemini "Nano Banana" models.
- **Prompt structure:** what to keep (camera, house, pool shape), then numbered changes, then "photorealistic, no text".
- **Use one approved render as a reference** for the other views so the structure, stone and furniture match.
- **Level changes fail in words.** Draw a guide on the last render: blue = raised surface, orange stripes = steps with DOWN arrows, red = side walls, cyan = sunken stairwell, every surface labeled HIGH or LOW with its elevation, one side wall per side of each flight. Prompt: "@guide is a copy of @render with colored markup; follow it, then leave every trace of it out of the result." Pass render, guide and original photo.
- **Stop after two or three guided passes.** Accept "close enough to get the idea across" and note in the plan what the image gets wrong; drawings govern levels.
- If uploads from your environment are blocked, ask the homeowner to upload images to their own image-tool workspace and pick them up from recent assets.
- Tell them the credit cost before each batch and the balance after.

Suggested views: aerial from an upper window, the main approach, the far corner looking at the new structure, and from inside the structure looking back. Render each option seriously considered from the same two camera positions.

## Stage 7. Drawing set and bid package

Produce 11×17 sheets, each with title block, sheet number, "Design development, not for construction", and the licensed-professional note:

| Sheet | Content |
| --- | --- |
| L-000 | Cover: rendering, drawing index, "before bidding, order" list |
| L-001 | Base plan on the survey: lot lines, setbacks, north, site data (paving, roof area, distance to lines, accessory total vs. town limit) |
| L-101 | Layout plan: dimensions, wall tags, staking coordinates for columns with check diagonals |
| L-201 | Grading and drainage: finished, existing and top-of-wall elevations, slopes, trench drains, downspouts, wall drains, collector and outlet, away from septic |
| L-301 | Structure elevations and roof plan: spacing, clear height, ridge, pitch, chimney |
| L-401 | Planting plan with plant key, quantities and tree protection |
| L-501 | Lighting and utilities with fixture counts and electric, gas and water routes |
| L-601 | Typical details: patio on slab, retaining wall with drainage, steps with capped side walls, column base |

Combine them into one PDF. In the plan document add: materials and finishes schedule; plant schedule (regional, deer-resistant where relevant); lighting schedule; numbered scope of work with exclusions; bid form with units, quantities, blank price columns and alternates, plus schedule, payment, warranty, insurance and registration; budget per option from cited unit-price ranges, region and year stated, 10–15% contingency, shared versus option-specific costs; permits checklist (zoning, building, electrical, plumbing, fire, soil-disturbance threshold, septic or health department, pool-barrier rules for new doors, outdoor lighting); items to verify before quoting; phasing with underground work first.

Before handing over, check that paving area, wall face area, fixture counts and plant counts agree across sheets, schedules and bid form.

## Drawing templates

The repo's `scripts/` folder holds the matplotlib code for the concept plans, grade section and every sheet. Set the project in `scripts/config.py`, adapt the site geometry, and run each `sheet_*.py`.

## Lessons learned

- Confirm what each markup color means first; an ambiguous one costs a full round.
- Ask for heights relative to outside ground, not only inside floors.
- Check survey setbacks before rendering anything final.
- Image models don't track high and low; use simple, labeled markup.
- Homeowners catch real problems in plans. Show plans early and often.
- A new door onto a pool area triggers pool-barrier rules; lowering grade at the house exposes foundation that needs waterproofing and an engineer.

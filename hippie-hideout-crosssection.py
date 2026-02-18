#!/Users/nathan.norman/.pyenv/versions/3.10.14/bin/python3
"""
Cross-section drawing from hand sketch to verify math.

Known dimensions:
- Left wall: 20' tall
- Right post: 8' tall
- Roof angle: 20° from horizontal (at top-left corner)
- Interior wall height labeled 12'
- Roof is shingled, slopes from top of left wall down to right
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(14, 10))

# --- Given dimensions ---
left_wall_h = 20.0   # feet
right_post_h = 8.0   # feet
roof_angle_deg = 20.0 # degrees from horizontal

# --- Derived geometry ---
roof_angle_rad = np.radians(roof_angle_deg)
roof_drop = left_wall_h - right_post_h  # 12 ft drop

# Horizontal distance for the roof to drop from 20' to 8'
# tan(20°) = rise / run  =>  run = rise / tan(20°)
horiz_span = roof_drop / np.tan(roof_angle_rad)

# Where does the roof hit 12' height? (interior wall)
drop_to_12 = left_wall_h - 12.0  # = 8 ft drop
wall_x = drop_to_12 / np.tan(roof_angle_rad)

print(f"=== GEOMETRY CHECK ===")
print(f"Roof angle: {roof_angle_deg}°")
print(f"Left wall:  {left_wall_h}'")
print(f"Right post: {right_post_h}'")
print(f"Roof drop:  {roof_drop}'")
print(f"")
print(f"Horizontal span (left wall to right post): {horiz_span:.2f}'")
print(f"Interior wall X position (at 12' height):  {wall_x:.2f}'")
print(f"")
print(f"Roof rafter length: {roof_drop / np.sin(roof_angle_rad):.2f}'")
print(f"")
print(f"tan(20°) = {np.tan(roof_angle_rad):.4f}")
print(f"Check: {horiz_span:.2f}' * tan(20°) = {horiz_span * np.tan(roof_angle_rad):.2f}' (should be {roof_drop}')")

# --- Draw the structure ---

# Ground line
ax.plot([0, horiz_span], [0, 0], 'k-', linewidth=2.5)

# Left wall (20')
ax.plot([0, 0], [0, left_wall_h], 'k-', linewidth=2.5)

# Right post (8')
ax.plot([horiz_span, horiz_span], [0, right_post_h], 'k-', linewidth=2.5)

# Roof line from top of left wall to top of right post
ax.plot([0, horiz_span], [left_wall_h, right_post_h], 'k-', linewidth=2.5)

# Interior wall from ground to roof at wall_x
ax.plot([wall_x, wall_x], [0, 12], 'k-', linewidth=2)

# X marks at corners/joints (like the sketch)
mark_size = 0.6
for (mx, my) in [(0, 0), (0, left_wall_h), (horiz_span, 0), (horiz_span, right_post_h), (wall_x, 0), (wall_x, 12)]:
    ax.plot([mx - mark_size, mx + mark_size], [my - mark_size, my + mark_size], 'k-', linewidth=1.5)
    ax.plot([mx - mark_size, mx + mark_size], [my + mark_size, my - mark_size], 'k-', linewidth=1.5)

# --- Dimension labels ---

# Left wall: 20'
ax.annotate("20'", xy=(-1.5, left_wall_h / 2), fontsize=14, fontweight='bold',
            ha='center', va='center')
ax.annotate('', xy=(-.8, 0), xytext=(-.8, left_wall_h),
            arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))

# Right post: 8'
ax.annotate("8' post", xy=(horiz_span + 2.5, right_post_h / 2), fontsize=14, fontweight='bold',
            ha='center', va='center')
ax.annotate('', xy=(horiz_span + .8, 0), xytext=(horiz_span + .8, right_post_h),
            arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))

# Interior wall: 12'
ax.annotate("12'", xy=(wall_x + 1.5, 6), fontsize=14, fontweight='bold',
            ha='center', va='center')
ax.annotate('', xy=(wall_x + .8, 0), xytext=(wall_x + .8, 12),
            arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))

# Angle arc at top-left
angle_arc = np.linspace(-np.radians(roof_angle_deg), 0, 50)
arc_r = 4
ax.plot(arc_r * np.cos(angle_arc), left_wall_h + arc_r * np.sin(angle_arc), 'r-', linewidth=1.5)
# Horizontal reference line at top
ax.plot([0, arc_r + 1], [left_wall_h, left_wall_h], 'r--', linewidth=1, alpha=0.5)
ax.annotate(f"{roof_angle_deg}°", xy=(arc_r + 0.5, left_wall_h - 1.2), fontsize=13,
            fontweight='bold', color='red', ha='left')

# Roof label
roof_mid_x = horiz_span * 0.4
roof_mid_y = left_wall_h - roof_mid_x * np.tan(roof_angle_rad)
ax.annotate("Shingled Roof", xy=(roof_mid_x, roof_mid_y + 1.5), fontsize=13,
            fontstyle='italic', ha='center', rotation=-np.degrees(np.arctan2(roof_drop, horiz_span)))

# Horizontal span dimension along bottom
ax.annotate(f"{horiz_span:.1f}'", xy=(horiz_span / 2, -2), fontsize=14, fontweight='bold',
            ha='center', va='center', color='darkgreen')
ax.annotate('', xy=(0, -1.5), xytext=(horiz_span, -1.5),
            arrowprops=dict(arrowstyle='<->', color='darkgreen', lw=1.5))

# Left section width
ax.annotate(f"A+C\n({wall_x:.1f}')", xy=(wall_x / 2, 5), fontsize=13,
            ha='center', va='center', color='gray')

# Right section width
right_section = horiz_span - wall_x
ax.annotate(f"{right_section:.1f}'", xy=(wall_x + right_section / 2, -3.5), fontsize=12,
            ha='center', va='center', color='purple')
ax.annotate('', xy=(wall_x, -3), xytext=(horiz_span, -3),
            arrowprops=dict(arrowstyle='<->', color='purple', lw=1.2))

# WALL label
ax.annotate("WALL", xy=(wall_x + 1, 12.8), fontsize=11, fontweight='bold', ha='left')

# Rafter length along the roof
rafter_len = roof_drop / np.sin(roof_angle_rad)
ax.annotate(f"Rafter: {rafter_len:.1f}'", xy=(horiz_span * 0.6, right_post_h + 2),
            fontsize=11, color='brown', ha='center',
            rotation=-np.degrees(np.arctan2(roof_drop, horiz_span)))

# --- Grid and formatting ---
ax.set_xlim(-4, horiz_span + 6)
ax.set_ylim(-5, left_wall_h + 3)
ax.set_aspect('equal')
ax.grid(True, which='both', linewidth=0.5, alpha=0.4, color='cyan')
ax.grid(True, which='major', linewidth=1.0, alpha=0.6, color='cyan')
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.set_xlabel("Horizontal Distance (feet)", fontsize=12)
ax.set_ylabel("Height (feet)", fontsize=12)
ax.set_title("Shed Cross-Section — Verify Roof Geometry", fontsize=15, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/nathan.norman/hippie-hideout-crosssection.png', dpi=150)
print(f"\nSaved to ~/hippie-hideout-crosssection.png")

#!/Users/nathan.norman/.pyenv/versions/3.10.14/bin/python3
"""Hippie Hideout — Top Down View (printer-friendly)."""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

fig, ax = plt.subplots(figsize=(16, 12))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Printer-friendly colors: all black/dark gray
LINE = 'k'
DOT = 'k'
LABEL = '#333'
DIM = '#333'
LIGHT = '#666'

r = 16.5

# --- DOME ---
theta = np.linspace(0, 2 * np.pi, 500)
ax.plot(r * np.cos(theta), r * np.sin(theta), LINE, lw=2.5)
ax.text(0, 0, 'B', fontsize=20, fontweight='bold', ha='center', va='center', color=LABEL)

# --- CONNECTION POINT ---
conn_angle = np.radians(20)
P = r * np.array([np.cos(conn_angle), np.sin(conn_angle)])
ax.plot(*P, 'ko', ms=8, zorder=5)
ax.text(P[0] + 1, P[1] + 2, "20° above\ncenter line", fontsize=9, color=LIGHT,
        ha='left', va='bottom')

# --- DOTTED HORIZONTAL REFERENCE LINE ---
ax.plot([P[0], P[0] + 35], [P[1], P[1]], 'k--', lw=1, alpha=0.4)

# --- WALL at 25° below horizontal, 30' long ---
wall_angle = np.radians(-25)
wall_end = P + 30 * np.array([np.cos(wall_angle), np.sin(wall_angle)])
ax.plot([P[0], wall_end[0]], [P[1], wall_end[1]], LINE, lw=2.5)

# --- 25° ARC between dotted line and wall ---
arc_r = 6
a_angles = np.linspace(0, wall_angle, 40)
ax.plot(P[0] + arc_r * np.cos(a_angles), P[1] + arc_r * np.sin(a_angles), 'k-', lw=1.5)
ax.text(P[0] + 8, P[1] - 2, '25°', fontsize=13, color=LABEL, fontweight='bold')

# --- LABEL the 30' wall ---
wall_mid = (P + wall_end) / 2
perp = np.array([np.sin(wall_angle), -np.cos(wall_angle)])
label_pos = wall_mid + 2 * perp
ax.text(label_pos[0], label_pos[1], "30'", fontsize=13, fontweight='bold',
        color=DIM, ha='center', va='center', rotation=np.degrees(wall_angle))

# --- 22' WALL at 90° to the 30' wall ---
wall2_angle = wall_angle - np.pi / 2
wall2_dir = np.array([np.cos(wall2_angle), np.sin(wall2_angle)])
wall2_end = wall_end + 22 * wall2_dir
ax.plot([wall_end[0], wall2_end[0]], [wall_end[1], wall2_end[1]], LINE, lw=2.5)
ax.plot(*wall_end, 'ko', ms=6, zorder=5)
ax.text(wall_end[0] + 2, wall_end[1] + 2, "20' high", fontsize=10, fontweight='bold', color=LIGHT)

# Label the 22' wall
wall2_mid = (wall_end + wall2_end) / 2
perp2 = np.array([np.sin(wall2_angle), -np.cos(wall2_angle)])
label2_pos = wall2_mid + 2 * perp2
ax.text(label2_pos[0], label2_pos[1], "22'", fontsize=13, fontweight='bold',
        color=DIM, ha='center', va='center', rotation=np.degrees(wall2_angle))

# --- 11' EXTENSION past the 22' wall (to the post) ---
post_end = wall2_end + 11 * wall2_dir
ax.plot([wall2_end[0], post_end[0]], [wall2_end[1], post_end[1]], LINE, lw=2.5)
ax.plot(*post_end, 'ks', ms=10, zorder=5)

# Label the 11' extension
ext_mid = (wall2_end + post_end) / 2
label_ext_pos = ext_mid + 2 * perp2
ax.text(label_ext_pos[0], label_ext_pos[1], "11'", fontsize=13, fontweight='bold',
        color=DIM, ha='center', va='center', rotation=np.degrees(wall2_angle))
ax.text(post_end[0] - 2, post_end[1] - 2, "Post (8')", fontsize=10, fontweight='bold',
        ha='center', color=LABEL)

# --- 3rd WALL: 90° from 22' wall, back to the dome ---
wall3_angle = wall2_angle - np.pi / 2
wall3_dir = np.array([np.cos(wall3_angle), np.sin(wall3_angle)])

a_coef = 1.0
b_coef = 2 * np.dot(wall2_end, wall3_dir)
c_coef = np.dot(wall2_end, wall2_end) - r**2
disc = b_coef**2 - 4 * a_coef * c_coef
t_hit = (-b_coef - np.sqrt(disc)) / (2 * a_coef)

wall3_end = wall2_end + t_hit * wall3_dir
ax.plot([wall2_end[0], wall3_end[0]], [wall2_end[1], wall3_end[1]], LINE, lw=2.5)
ax.plot(*wall2_end, 'ko', ms=6, zorder=5)
ax.text(wall2_end[0] + 2, wall2_end[1] + 2, "12' high", fontsize=10, fontweight='bold', color=LIGHT)
ax.plot(*wall3_end, 'ko', ms=6, zorder=5)

# Label
wall3_mid = (wall2_end + wall3_end) / 2
perp3 = np.array([np.sin(wall3_angle), -np.cos(wall3_angle)])
label3_pos = wall3_mid + 2.5 * perp3
ax.text(label3_pos[0], label3_pos[1], f"{t_hit:.1f}'", fontsize=13, fontweight='bold',
        color=DIM, ha='center', va='center', rotation=np.degrees(wall3_angle) + 180)

print(f"22' wall end: ({wall2_end[0]:.1f}, {wall2_end[1]:.1f})")
print(f"3rd wall hits dome at: ({wall3_end[0]:.1f}, {wall3_end[1]:.1f})")
print(f"3rd wall length: {t_hit:.1f}'")

# === LEFT WING (A) — mirror of right wing across y-axis ===
def mirror(pt):
    return np.array([-pt[0], pt[1]])

P_L = mirror(P)
ax.plot(*P_L, 'ko', ms=8, zorder=5)
ax.text(P_L[0] - 1, P_L[1] + 2, "20° above\ncenter line", fontsize=9, color=LIGHT,
        ha='right', va='bottom')

# Dotted horizontal reference (to the left)
ax.plot([P_L[0], P_L[0] - 35], [P_L[1], P_L[1]], 'k--', lw=1, alpha=0.4)

# 30' wall
wall_end_L = mirror(wall_end)
ax.plot([P_L[0], wall_end_L[0]], [P_L[1], wall_end_L[1]], LINE, lw=2.5)

# 25° arc (mirrored)
a_angles_L = np.linspace(np.pi, np.pi + np.radians(25), 40)
ax.plot(P_L[0] + arc_r * np.cos(a_angles_L), P_L[1] + arc_r * np.sin(a_angles_L), 'k-', lw=1.5)
ax.text(P_L[0] - 8, P_L[1] - 2, '25°', fontsize=13, color=LABEL, fontweight='bold')

# 30' label
wall_mid_L = (P_L + wall_end_L) / 2
label_pos_L = wall_mid_L - 2 * perp
ax.text(label_pos_L[0], label_pos_L[1], "30'", fontsize=13, fontweight='bold',
        color=DIM, ha='center', va='center', rotation=-np.degrees(wall_angle))

# 22' wall
wall2_end_L = mirror(wall2_end)
ax.plot([wall_end_L[0], wall2_end_L[0]], [wall_end_L[1], wall2_end_L[1]], LINE, lw=2.5)
ax.plot(*wall_end_L, 'ko', ms=6, zorder=5)
ax.text(wall_end_L[0] - 2, wall_end_L[1] + 2, "20' high", fontsize=10, fontweight='bold', color=LIGHT, ha='right')

# 22' label
wall2_mid_L = (wall_end_L + wall2_end_L) / 2
label2_pos_L = wall2_mid_L - 2 * perp2
ax.text(label2_pos_L[0], label2_pos_L[1], "22'", fontsize=13, fontweight='bold',
        color=DIM, ha='center', va='center', rotation=-np.degrees(wall2_angle))

# 11' extension to post
post_end_L = mirror(post_end)
ax.plot([wall2_end_L[0], post_end_L[0]], [wall2_end_L[1], post_end_L[1]], LINE, lw=2.5)
ax.plot(*post_end_L, 'ks', ms=10, zorder=5)

ext_mid_L = (wall2_end_L + post_end_L) / 2
label_ext_pos_L = ext_mid_L - 2 * perp2
ax.text(label_ext_pos_L[0], label_ext_pos_L[1], "11'", fontsize=13, fontweight='bold',
        color=DIM, ha='center', va='center', rotation=-np.degrees(wall2_angle))
ax.text(post_end_L[0] + 2, post_end_L[1] - 2, "Post (8')", fontsize=10, fontweight='bold',
        ha='center', color=LABEL)

# 28.8' wall back to dome
wall3_end_L = mirror(wall3_end)
ax.plot([wall2_end_L[0], wall3_end_L[0]], [wall2_end_L[1], wall3_end_L[1]], LINE, lw=2.5)
ax.plot(*wall2_end_L, 'ko', ms=6, zorder=5)
ax.text(wall2_end_L[0] - 2, wall2_end_L[1] + 2, "12' high", fontsize=10, fontweight='bold', color=LIGHT, ha='right')
ax.plot(*wall3_end_L, 'ko', ms=6, zorder=5)

wall3_mid_L = (wall2_end_L + wall3_end_L) / 2
label3_pos_L = wall3_mid_L - 2.5 * perp3
ax.text(label3_pos_L[0], label3_pos_L[1], f"{t_hit:.1f}'", fontsize=13, fontweight='bold',
        color=DIM, ha='center', va='center', rotation=-np.degrees(wall3_angle) + 180)

# --- HORIZONTAL LINE dropped to circle intersection ---
half_width = 4.0
y_intersect = -np.sqrt(r**2 - half_width**2)
left_int = np.array([-half_width, y_intersect])
right_int = np.array([half_width, y_intersect])

ax.plot([left_int[0], right_int[0]], [left_int[1], right_int[1]], LINE, lw=2.5)
ax.plot(*left_int, 'ko', ms=8, zorder=5)
ax.plot(*right_int, 'ko', ms=8, zorder=5)

ax.text(left_int[0] - 1, left_int[1] - 1.5,
        f"({left_int[0]:.1f}, {left_int[1]:.2f})", fontsize=10, fontweight='bold',
        color=LIGHT, ha='right', va='top')
ax.text(right_int[0] + 1, right_int[1] - 1.5,
        f"({right_int[0]:.1f}, {right_int[1]:.2f})", fontsize=10, fontweight='bold',
        color=LIGHT, ha='left', va='top')

# --- Two 5' vertical lines down, connected by 8' horizontal ---
left_bottom = left_int + np.array([0, -5])
right_bottom = right_int + np.array([0, -5])

ax.plot([left_int[0], left_bottom[0]], [left_int[1], left_bottom[1]], LINE, lw=2.5)
ax.plot([right_int[0], right_bottom[0]], [right_int[1], right_bottom[1]], LINE, lw=2.5)
bottom_y = left_bottom[1]
ax.plot([left_bottom[0], right_bottom[0]], [bottom_y, bottom_y], LINE, lw=2.5)

for pt in [left_bottom, right_bottom]:
    ax.plot(*pt, 'ko', ms=6, zorder=5)

ax.text(left_int[0] - 1, (left_int[1] + left_bottom[1]) / 2, "5'",
        fontsize=11, fontweight='bold', color=DIM, ha='right', va='center')
ax.text(right_int[0] + 1, (right_int[1] + right_bottom[1]) / 2, "5'",
        fontsize=11, fontweight='bold', color=DIM, ha='left', va='center')
ax.text(0, bottom_y - 1.5, "8'", fontsize=11, fontweight='bold',
        color=DIM, ha='center', va='top')

print(f"Vertical lines bottom points:")
print(f"  Left:  ({left_bottom[0]:.2f}, {left_bottom[1]:.2f})")
print(f"  Right: ({right_bottom[0]:.2f}, {right_bottom[1]:.2f})")
print(f"  Bottom horizontal: y = {bottom_y:.2f}, from x = -4 to x = 4")

print(f"Horizontal line intersection points:")
print(f"  Left:  ({left_int[0]:.2f}, {left_int[1]:.2f})")
print(f"  Right: ({right_int[0]:.2f}, {right_int[1]:.2f})")

# --- ARC from right post through bottom horizontal to left post ---
px, py = post_end[0], post_end[1]
by = bottom_y
arc_cy = (px**2 + py**2 - by**2) / (2 * (py - by))
arc_R = abs(arc_cy - by)

angle_right = np.arctan2(post_end[1] - arc_cy, post_end[0])
angle_left = np.arctan2(post_end_L[1] - arc_cy, post_end_L[0])

arc_angles = np.linspace(angle_right, angle_left, 200)
ax.plot(arc_R * np.cos(arc_angles), arc_cy + arc_R * np.sin(arc_angles), 'k-', lw=2, alpha=0.6)

arc_label_y = (post_end[1] + bottom_y) / 2
ax.text(0, arc_label_y, f"Arc diameter {2*arc_R:.1f}'", fontsize=12, fontweight='bold',
        color=LABEL, ha='center', va='center')

print(f"Arc center: (0, {arc_cy:.2f}), radius: {arc_R:.2f}")
print(f"Arc angles: {np.degrees(angle_right):.1f}° to {np.degrees(angle_left):.1f}°")

# --- GRID (light, printer-friendly) ---
ax.set_aspect('equal')
ax.set_xlim(-52, 52)
ax.set_ylim(-40, 22)
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.grid(True, which='major', lw=0.5, alpha=0.3, color='#aaa')
ax.grid(True, which='minor', lw=0.2, alpha=0.15, color='#ccc')
ax.set_xlabel("Feet", fontsize=12)
ax.set_ylabel("Feet", fontsize=12)
ax.set_title("Hippie Hideout — Top Down View", fontsize=16, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/nathan.norman/shed-floorplan.png', dpi=200, facecolor='white')
plt.savefig('/Users/nathan.norman/shed-floorplan.pdf', facecolor='white')
print(f"Connection: ({P[0]:.1f}, {P[1]:.1f})")
print(f"Wall end:   ({wall_end[0]:.1f}, {wall_end[1]:.1f})")
print(f"Saved to ~/shed-floorplan.png and ~/shed-floorplan.pdf")

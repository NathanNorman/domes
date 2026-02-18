#!/Users/nathan.norman/.pyenv/versions/3.10.14/bin/python3
"""
Interactive dual-view: cross-section + floor plan, driven by roof pitch slider.

Usage:
    python3 shed-crosssection-interactive.py              # Opens interactive slider window
    python3 shed-crosssection-interactive.py --angle 25   # Exports single PNG at 25°
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# --- Fixed dimensions ---
LEFT_WALL_H = 20.0    # feet (dome wall height)
RIGHT_POST_H = 8.0    # feet (post height)
ROOF_DROP = LEFT_WALL_H - RIGHT_POST_H  # 12 ft
INTERIOR_WALL_H = 12.0 # feet
BACK_WALL_LEN = 30.0  # feet (fixed)
DOME_R = 16.5          # dome radius
CONN_ANGLE = 20.0      # degrees above horizontal where wings attach
WALL_ANGLE_DEG = -25.0 # degrees below horizontal for the 30' back wall


def compute_geometry(pitch_deg):
    """Compute all derived dimensions from roof pitch angle."""
    rad = np.radians(pitch_deg)
    horiz_span = ROOF_DROP / np.tan(rad)
    wall_x = (LEFT_WALL_H - INTERIOR_WALL_H) / np.tan(rad)  # wing room width
    rafter_len = ROOF_DROP / np.sin(rad)
    right_section = horiz_span - wall_x  # post extension
    return {
        'pitch_deg': pitch_deg,
        'pitch_rad': rad,
        'horiz_span': horiz_span,
        'wall_x': wall_x,
        'rafter_len': rafter_len,
        'right_section': right_section,
    }


def draw_cross_section(ax, g):
    """Draw the cross-section (side view) on the given axes."""
    ax.clear()

    pitch_deg = g['pitch_deg']
    rad = g['pitch_rad']
    horiz_span = g['horiz_span']
    wall_x = g['wall_x']
    rafter_len = g['rafter_len']
    right_section = g['right_section']

    # Structure lines
    ax.plot([0, horiz_span], [0, 0], 'k-', lw=2.5)
    ax.plot([0, 0], [0, LEFT_WALL_H], 'k-', lw=2.5)
    ax.plot([horiz_span, horiz_span], [0, RIGHT_POST_H], 'k-', lw=2.5)
    ax.plot([0, horiz_span], [LEFT_WALL_H, RIGHT_POST_H], 'k-', lw=2.5)
    ax.plot([wall_x, wall_x], [0, INTERIOR_WALL_H], 'k-', lw=2)

    # X marks at joints
    ms = 0.5
    for (mx, my) in [(0, 0), (0, LEFT_WALL_H), (horiz_span, 0),
                      (horiz_span, RIGHT_POST_H), (wall_x, 0), (wall_x, INTERIOR_WALL_H)]:
        ax.plot([mx - ms, mx + ms], [my - ms, my + ms], 'k-', lw=1.5)
        ax.plot([mx - ms, mx + ms], [my + ms, my - ms], 'k-', lw=1.5)

    # Left wall: 20'
    ax.annotate("20'", xy=(-1.2, LEFT_WALL_H / 2), fontsize=12,
                fontweight='bold', ha='center', va='center')
    ax.annotate('', xy=(-.6, 0), xytext=(-.6, LEFT_WALL_H),
                arrowprops=dict(arrowstyle='<->', color='blue', lw=1.2))

    # Right post: 8'
    ax.annotate("8'", xy=(horiz_span + 1.8, RIGHT_POST_H / 2), fontsize=12,
                fontweight='bold', ha='center', va='center')
    ax.annotate('', xy=(horiz_span + .6, 0), xytext=(horiz_span + .6, RIGHT_POST_H),
                arrowprops=dict(arrowstyle='<->', color='blue', lw=1.2))

    # Interior wall: 12'
    ax.annotate("12'", xy=(wall_x + 1.2, 6), fontsize=12,
                fontweight='bold', ha='center', va='center')
    ax.annotate('', xy=(wall_x + .6, 0), xytext=(wall_x + .6, INTERIOR_WALL_H),
                arrowprops=dict(arrowstyle='<->', color='blue', lw=1.2))

    # Angle arc
    arc_angles = np.linspace(-rad, 0, 50)
    arc_r = 3
    ax.plot(arc_r * np.cos(arc_angles), LEFT_WALL_H + arc_r * np.sin(arc_angles), 'r-', lw=1.5)
    ax.plot([0, arc_r + 1], [LEFT_WALL_H, LEFT_WALL_H], 'r--', lw=1, alpha=0.5)
    ax.annotate(f"{pitch_deg:.0f}°", xy=(arc_r + 0.5, LEFT_WALL_H - 1.0),
                fontsize=12, fontweight='bold', color='red', ha='left')

    # Roof label
    roof_rot = -np.degrees(np.arctan2(ROOF_DROP, horiz_span))
    roof_mid_x = horiz_span * 0.35
    roof_mid_y = LEFT_WALL_H - roof_mid_x * np.tan(rad)
    ax.annotate("Roof", xy=(roof_mid_x, roof_mid_y + 1.2), fontsize=11,
                fontstyle='italic', ha='center', rotation=roof_rot)

    # Horizontal span
    ax.annotate(f"{horiz_span:.1f}'", xy=(horiz_span / 2, -1.8), fontsize=12,
                fontweight='bold', ha='center', va='center', color='darkgreen')
    ax.annotate('', xy=(0, -1.3), xytext=(horiz_span, -1.3),
                arrowprops=dict(arrowstyle='<->', color='darkgreen', lw=1.2))

    # Wing room width
    ax.annotate(f"Wing: {wall_x:.1f}'", xy=(wall_x / 2, 4), fontsize=11,
                ha='center', va='center', color='gray')

    # Extension width
    ax.annotate(f"{right_section:.1f}'", xy=(wall_x + right_section / 2, -3.2),
                fontsize=11, ha='center', va='center', color='purple')
    ax.annotate('', xy=(wall_x, -2.8), xytext=(horiz_span, -2.8),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=1))

    # Rafter
    ax.annotate(f"Rafter: {rafter_len:.1f}'",
                xy=(horiz_span * 0.55, RIGHT_POST_H + 1.5), fontsize=10,
                color='brown', ha='center', rotation=roof_rot)

    # WALL label
    ax.annotate("WALL", xy=(wall_x + 0.8, INTERIOR_WALL_H + 0.5), fontsize=10,
                fontweight='bold', ha='left')

    # Fixed axes so view doesn't jump
    max_span = ROOF_DROP / np.tan(np.radians(20))
    ax.set_xlim(-3, max_span + 4)
    ax.set_ylim(-4.5, LEFT_WALL_H + 2)
    ax.set_aspect('equal')
    ax.grid(True, which='major', lw=0.5, alpha=0.3, color='#aaa')
    ax.grid(True, which='minor', lw=0.2, alpha=0.15, color='#ccc')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.set_xlabel("Feet", fontsize=10)
    ax.set_ylabel("Feet", fontsize=10)
    ax.set_title("Cross-Section (Side View)", fontsize=13, fontweight='bold')


def draw_floorplan(ax, g):
    """Draw the top-down floor plan on the given axes, with wing dimensions from geometry."""
    ax.clear()

    wall_x = g['wall_x']          # was 22' at 20° pitch
    right_section = g['right_section']  # was 11' at 20° pitch
    pitch_deg = g['pitch_deg']

    r = DOME_R
    wall_angle = np.radians(WALL_ANGLE_DEG)
    conn_rad = np.radians(CONN_ANGLE)

    # --- DOME ---
    theta = np.linspace(0, 2 * np.pi, 500)
    ax.plot(r * np.cos(theta), r * np.sin(theta), 'k-', lw=2)
    ax.text(0, 0, 'B', fontsize=16, fontweight='bold', ha='center', va='center', color='#333')

    # --- RIGHT WING ---
    # Connection point
    P = r * np.array([np.cos(conn_rad), np.sin(conn_rad)])
    ax.plot(*P, 'ko', ms=6, zorder=5)

    # 30' back wall at angle
    wall_end = P + BACK_WALL_LEN * np.array([np.cos(wall_angle), np.sin(wall_angle)])
    ax.plot([P[0], wall_end[0]], [P[1], wall_end[1]], 'k-', lw=2)

    # Wing wall (was 22', now = wall_x) perpendicular to back wall
    wall2_angle = wall_angle - np.pi / 2
    wall2_dir = np.array([np.cos(wall2_angle), np.sin(wall2_angle)])
    wall2_end = wall_end + wall_x * wall2_dir
    ax.plot([wall_end[0], wall2_end[0]], [wall_end[1], wall2_end[1]], 'k-', lw=2)
    ax.plot(*wall_end, 'ko', ms=5, zorder=5)

    # Extension to post (was 11', now = right_section)
    post_end = wall2_end + right_section * wall2_dir
    ax.plot([wall2_end[0], post_end[0]], [wall2_end[1], post_end[1]], 'k-', lw=2)
    ax.plot(*post_end, 'ks', ms=8, zorder=5)
    ax.plot(*wall2_end, 'ko', ms=5, zorder=5)

    # Wall back to dome from wall2_end
    wall3_angle = wall2_angle - np.pi / 2
    wall3_dir = np.array([np.cos(wall3_angle), np.sin(wall3_angle)])
    a_coef = 1.0
    b_coef = 2 * np.dot(wall2_end, wall3_dir)
    c_coef = np.dot(wall2_end, wall2_end) - r**2
    disc = b_coef**2 - 4 * a_coef * c_coef
    if disc >= 0:
        t_hit = (-b_coef - np.sqrt(disc)) / (2 * a_coef)
        wall3_end = wall2_end + t_hit * wall3_dir
        ax.plot([wall2_end[0], wall3_end[0]], [wall2_end[1], wall3_end[1]], 'k-', lw=2)
        ax.plot(*wall3_end, 'ko', ms=5, zorder=5)

    # --- Dimension labels (right wing) ---
    perp = np.array([np.sin(wall_angle), -np.cos(wall_angle)])
    wall_mid = (P + wall_end) / 2
    ax.text(*(wall_mid + 1.5 * perp), f"30'", fontsize=11, fontweight='bold',
            color='#333', ha='center', va='center', rotation=np.degrees(wall_angle))

    perp2 = np.array([np.sin(wall2_angle), -np.cos(wall2_angle)])
    wall2_mid = (wall_end + wall2_end) / 2
    ax.text(*(wall2_mid + 1.5 * perp2), f"{wall_x:.1f}'", fontsize=11, fontweight='bold',
            color='#333', ha='center', va='center', rotation=np.degrees(wall2_angle))

    ext_mid = (wall2_end + post_end) / 2
    ax.text(*(ext_mid + 1.5 * perp2), f"{right_section:.1f}'", fontsize=11, fontweight='bold',
            color='#333', ha='center', va='center', rotation=np.degrees(wall2_angle))

    # Height labels
    ax.text(wall_end[0] + 1.5, wall_end[1] + 1.5, "20' high", fontsize=9, color='#666')
    ax.text(wall2_end[0] + 1.5, wall2_end[1] + 1.5, "12' high", fontsize=9, color='#666')
    ax.text(post_end[0] - 1.5, post_end[1] - 1.5, f"Post (8')", fontsize=9,
            fontweight='bold', ha='center', color='#333')

    if disc >= 0:
        perp3 = np.array([np.sin(wall3_angle), -np.cos(wall3_angle)])
        wall3_mid = (wall2_end + wall3_end) / 2
        ax.text(*(wall3_mid + 2 * perp3), f"{t_hit:.1f}'", fontsize=11, fontweight='bold',
                color='#333', ha='center', va='center',
                rotation=np.degrees(wall3_angle) + 180)

    # --- LEFT WING (mirror) ---
    def mirror(pt):
        return np.array([-pt[0], pt[1]])

    P_L = mirror(P)
    ax.plot(*P_L, 'ko', ms=6, zorder=5)

    wall_end_L = mirror(wall_end)
    ax.plot([P_L[0], wall_end_L[0]], [P_L[1], wall_end_L[1]], 'k-', lw=2)

    wall2_end_L = mirror(wall2_end)
    ax.plot([wall_end_L[0], wall2_end_L[0]], [wall_end_L[1], wall2_end_L[1]], 'k-', lw=2)
    ax.plot(*wall_end_L, 'ko', ms=5, zorder=5)

    post_end_L = mirror(post_end)
    ax.plot([wall2_end_L[0], post_end_L[0]], [wall2_end_L[1], post_end_L[1]], 'k-', lw=2)
    ax.plot(*post_end_L, 'ks', ms=8, zorder=5)
    ax.plot(*wall2_end_L, 'ko', ms=5, zorder=5)

    if disc >= 0:
        wall3_end_L = mirror(wall3_end)
        ax.plot([wall2_end_L[0], wall3_end_L[0]], [wall2_end_L[1], wall3_end_L[1]], 'k-', lw=2)
        ax.plot(*wall3_end_L, 'ko', ms=5, zorder=5)

    # Left wing labels
    wall_mid_L = (P_L + wall_end_L) / 2
    ax.text(*(wall_mid_L - 1.5 * perp), f"30'", fontsize=11, fontweight='bold',
            color='#333', ha='center', va='center', rotation=-np.degrees(wall_angle))

    wall2_mid_L = (wall_end_L + wall2_end_L) / 2
    ax.text(*(wall2_mid_L - 1.5 * perp2), f"{wall_x:.1f}'", fontsize=11, fontweight='bold',
            color='#333', ha='center', va='center', rotation=-np.degrees(wall2_angle))

    ext_mid_L = (wall2_end_L + post_end_L) / 2
    ax.text(*(ext_mid_L - 1.5 * perp2), f"{right_section:.1f}'", fontsize=11, fontweight='bold',
            color='#333', ha='center', va='center', rotation=-np.degrees(wall2_angle))

    ax.text(wall_end_L[0] - 1.5, wall_end_L[1] + 1.5, "20' high", fontsize=9, color='#666', ha='right')
    ax.text(wall2_end_L[0] - 1.5, wall2_end_L[1] + 1.5, "12' high", fontsize=9, color='#666', ha='right')
    ax.text(post_end_L[0] + 1.5, post_end_L[1] - 1.5, f"Post (8')", fontsize=9,
            fontweight='bold', ha='center', color='#333')

    if disc >= 0:
        wall3_mid_L = (wall2_end_L + wall3_end_L) / 2
        ax.text(*(wall3_mid_L - 2 * perp3), f"{t_hit:.1f}'", fontsize=11, fontweight='bold',
                color='#333', ha='center', va='center',
                rotation=-np.degrees(wall3_angle) + 180)

    # --- Front rectangle + arc ---
    half_width = 4.0
    y_int = -np.sqrt(r**2 - half_width**2)
    left_int = np.array([-half_width, y_int])
    right_int = np.array([half_width, y_int])
    ax.plot([left_int[0], right_int[0]], [left_int[1], right_int[1]], 'k-', lw=2)
    ax.plot(*left_int, 'ko', ms=6, zorder=5)
    ax.plot(*right_int, 'ko', ms=6, zorder=5)

    left_bot = left_int + np.array([0, -5])
    right_bot = right_int + np.array([0, -5])
    ax.plot([left_int[0], left_bot[0]], [left_int[1], left_bot[1]], 'k-', lw=2)
    ax.plot([right_int[0], right_bot[0]], [right_int[1], right_bot[1]], 'k-', lw=2)
    ax.plot([left_bot[0], right_bot[0]], [left_bot[1], right_bot[1]], 'k-', lw=2)

    # Front arc
    bot_y = left_bot[1]
    px, py = post_end[0], post_end[1]
    arc_cy = (px**2 + py**2 - bot_y**2) / (2 * (py - bot_y))
    arc_R = abs(arc_cy - bot_y)
    a_right = np.arctan2(post_end[1] - arc_cy, post_end[0])
    a_left = np.arctan2(post_end_L[1] - arc_cy, post_end_L[0])
    arc_th = np.linspace(a_right, a_left, 200)
    ax.plot(arc_R * np.cos(arc_th), arc_cy + arc_R * np.sin(arc_th), 'k-', lw=1.5, alpha=0.5)

    # --- Grid ---
    ax.set_aspect('equal')
    ax.set_xlim(-52, 52)
    ax.set_ylim(-42, 22)
    ax.grid(True, which='major', lw=0.5, alpha=0.3, color='#aaa')
    ax.grid(True, which='minor', lw=0.2, alpha=0.15, color='#ccc')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.set_xlabel("Feet", fontsize=10)
    ax.set_ylabel("Feet", fontsize=10)
    ax.set_title("Floor Plan (Top Down)", fontsize=13, fontweight='bold')


def run_interactive():
    """Open interactive window with both views and a roof pitch slider."""
    from matplotlib.widgets import Slider

    fig, (ax_cross, ax_floor) = plt.subplots(1, 2, figsize=(22, 10))
    plt.subplots_adjust(bottom=0.12, wspace=0.25)

    # Initial draw at 20°
    g = compute_geometry(20.0)
    draw_cross_section(ax_cross, g)
    draw_floorplan(ax_floor, g)

    # Slider
    ax_slider = fig.add_axes([0.15, 0.02, 0.7, 0.03])
    slider = Slider(ax_slider, 'Roof Pitch', 20, 35, valinit=20, valstep=0.5,
                    color='steelblue')
    ax_slider.set_xlabel('degrees', fontsize=10)

    def update(_):
        g = compute_geometry(slider.val)
        draw_cross_section(ax_cross, g)
        draw_floorplan(ax_floor, g)
        fig.suptitle(f"Hippie Hideout — Roof Pitch {slider.val:.0f}°    |    "
                     f"Wing room: {g['wall_x']:.1f}'    Post extension: {g['right_section']:.1f}'    "
                     f"Total span: {g['horiz_span']:.1f}'",
                     fontsize=13, fontweight='bold', y=0.98)
        fig.canvas.draw_idle()

    slider.on_changed(update)

    # Initial title
    fig.suptitle(f"Hippie Hideout — Roof Pitch 20°    |    "
                 f"Wing room: {g['wall_x']:.1f}'    Post extension: {g['right_section']:.1f}'    "
                 f"Total span: {g['horiz_span']:.1f}'",
                 fontsize=13, fontweight='bold', y=0.98)

    plt.show()


def export_single(angle_deg, output_path=None):
    """Export a single PNG with both views at the given angle."""
    if output_path is None:
        output_path = f'/Users/nathan.norman/hippie-hideout-{angle_deg:.0f}deg.png'

    fig, (ax_cross, ax_floor) = plt.subplots(1, 2, figsize=(22, 10))
    plt.subplots_adjust(wspace=0.25)

    g = compute_geometry(angle_deg)
    draw_cross_section(ax_cross, g)
    draw_floorplan(ax_floor, g)

    fig.suptitle(f"Hippie Hideout — Roof Pitch {angle_deg:.0f}°    |    "
                 f"Wing room: {g['wall_x']:.1f}'    Post extension: {g['right_section']:.1f}'    "
                 f"Total span: {g['horiz_span']:.1f}'",
                 fontsize=13, fontweight='bold')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=200, facecolor='white')
    plt.close(fig)
    print(f"Saved dual view at {angle_deg:.0f}° to {output_path}")


if __name__ == '__main__':
    if '--angle' in sys.argv:
        idx = sys.argv.index('--angle')
        angle = float(sys.argv[idx + 1])
        export_single(angle)
    else:
        run_interactive()

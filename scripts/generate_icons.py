"""Generate CiCi launcher icons (pure Python, no dependencies)
Design: Cute AI assistant robot face — modern, friendly, recognizable."""

import struct
import zlib
import os
import math


def blend(a, b, t):
    """Blend two RGB colors"""
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_png(width, height):
    """Generate PNG with a cute robot assistant face"""
    def chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack(">I", len(data)) + c + struct.pack(
            ">I", zlib.crc32(c) & 0xFFFFFFFF
        )

    header = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(
        b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    )

    cx, cy = width / 2, height / 2
    scale = width / 192.0

    # Colors
    BG_DARK = (48, 35, 130)       # Deep purple
    BG_LIGHT = (90, 72, 210)      # Lighter purple
    FACE_WHITE = (245, 245, 255)  # Off-white
    EYE_DARK = (50, 36, 130)      # Dark purple for eyes
    BLUSH = (255, 180, 200)       # Blush pink
    ANTENNA_TIP = (120, 255, 180) # Green glow dot
    SCREEN_FRAME = (70, 55, 160)

    raw = b""
    for y in range(height):
        raw += b"\x00"
        for x in range(width):
            # Normalized coordinates (-1 to 1)
            nx = (x - cx) / (width * 0.42)
            ny = (y - cy) / (height * 0.42)
            dist = math.sqrt(nx*nx + ny*ny)

            # Sky gradient background (full canvas)
            bg_t = y / height
            bg = blend(BG_DARK, BG_LIGHT, 1.0 - bg_t * 0.6)

            # ===== Robot face =====
            face_outer = dist < 1.0

            if not face_outer:
                raw += struct.pack("BBB", *bg)
                continue

            # Face background (rounded square-like using superellipse approach)
            # Soft face interior
            face_inner_r = 0.85

            # Inside face
            if dist < face_inner_r:
                # Antenna
                is_antenna = False
                is_antenna_tip = False

                # Antenna line (vertical above center)
                ant_x = abs(nx)
                ant_draw = ny < -0.45 and ant_x < 0.04 and ny > -0.85
                if ant_draw:
                    is_antenna = True

                # Antenna tip dot
                ant_tip = ny < -0.78 and math.sqrt(nx*nx + (ny+0.82)**2) * width * 0.42 / scale < 8 * (scale / width * 192)
                tip_dist = math.sqrt(nx*nx + (ny+0.82)**2)
                if tip_dist < 0.08:
                    is_antenna_tip = True

                if is_antenna_tip:
                    # Green glowing dot
                    if tip_dist < 0.05:
                        raw += struct.pack("BBB", *ANTENNA_TIP)
                    else:
                        raw += struct.pack("BBB", *blend(ANTENNA_TIP, FACE_WHITE, (tip_dist-0.05)/0.04))
                    continue

                if is_antenna:
                    raw += struct.pack("BBB", *SCREEN_FRAME)
                    continue

                # Eyes — two rounded rectangles
                eye_left_x = nx + 0.28  # center offset left eye
                eye_right_x = nx - 0.28  # center offset right eye
                eye_y = ny + 0.1

                # Eye shape (horizontal oval)
                eye_w, eye_h = 0.12, 0.15
                in_left_eye = (abs(eye_left_x) / eye_w)**2 + (eye_y / eye_h)**2 < 1.0
                in_right_eye = (abs(eye_right_x) / eye_w)**2 + (eye_y / eye_h)**2 < 1.0

                if in_left_eye or in_right_eye:
                    # Pupil (slightly smaller, dark)
                    pupil_w, pupil_h = 0.07, 0.11
                    ex = eye_left_x if in_left_eye else eye_right_x
                    in_pupil = (ex / pupil_w)**2 + (eye_y / pupil_h)**2 < 1.0
                    if in_pupil:
                        # Eye shine
                        shine_y = eye_y - 0.045
                        if math.sqrt((ex+0.02)**2 + (shine_y)**2) * 3 < 0.03:
                            raw += struct.pack("BBB", 255, 255, 255)
                        else:
                            raw += struct.pack("BBB", *EYE_DARK)
                    else:
                        raw += struct.pack("BBB", *FACE_WHITE)
                    continue

                # Blush cheeks
                blush_dist_l = math.sqrt((nx+0.38)**2 + (ny-0.18)**2)
                blush_dist_r = math.sqrt((nx-0.38)**2 + (ny-0.18)**2)
                in_blush = blush_dist_l < 0.12 or blush_dist_r < 0.12
                if in_blush:
                    bd = blush_dist_l if blush_dist_l < blush_dist_r else blush_dist_r
                    alpha = max(0, 1.0 - bd / 0.12)
                    raw += struct.pack("BBB", *blend(FACE_WHITE, BLUSH, alpha * 0.5))
                    continue

                # Mouth (small arc/smile)
                mouth_dy = ny - 0.18
                mouth_dx = nx
                # Smile arc: bottom half of a small circle
                mouth_radius = 0.1
                mouth_dist = math.sqrt((mouth_dx/1.5)**2 + mouth_dy**2)
                # Only show bottom arc
                in_mouth = mouth_dist < mouth_radius and mouth_dy > -0.02 and mouth_dy < 0.09
                if in_mouth:
                    raw += struct.pack("BBB", *SCREEN_FRAME)
                    continue

                # Face color
                raw += struct.pack("BBB", *FACE_WHITE)

            else:
                # Edge ring — blend between face and bg
                edge_t = (dist - face_inner_r) / (1.0 - face_inner_r)
                edge_color = blend(FACE_WHITE, bg, edge_t)
                raw += struct.pack("BBB", *edge_color)

    idat = chunk(b"IDAT", zlib.compress(raw))
    iend = chunk(b"IEND", b"")
    return header + ihdr + idat + iend


def make_foreground_xml():
    """Vector XML foreground: cute robot face for adaptive icon"""
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
        '    android:width="108dp" android:height="108dp"\n'
        '    android:viewportWidth="108" android:viewportHeight="108">\n'
        # Face circle
        '    <path android:fillColor="#F5F5FF"\n'
        '        android:pathData="'
        'M54,18'
        'C34.1,18 18,34.1 18,54'
        'C18,73.9 34.1,90 54,90'
        'C73.9,90 90,73.9 90,54'
        'C90,34.1 73.9,18 54,18Z'
        '"/>\n'
        # Left antenna
        '    <path android:fillColor="#4634AE"\n'
        '        android:strokeWidth="1.5"\n'
        '        android:pathData="'
        'M52,20L50,12'
        '"/>\n'
        # Right antenna
        '    <path android:fillColor="#4634AE"\n'
        '        android:strokeWidth="1.5"\n'
        '        android:pathData="'
        'M56,20L58,12'
        '"/>\n'
        # Antenna tips
        '    <path android:fillColor="#78FFB4"\n'
        '        android:pathData="'
        'M50,12 A3,3 0 1,0 50,6 A3,3 0 1,0 50,12Z'
        '"/>\n'
        '    <path android:fillColor="#78FFB4"\n'
        '        android:pathData="'
        'M58,12 A3,3 0 1,0 58,6 A3,3 0 1,0 58,12Z'
        '"/>\n'
        # Left eye frame (outer)
        '    <path android:fillColor="#4634AE"\n'
        '        android:pathData="'
        'M40,38'
        'A8,10 0 1,0 40,58'
        'A8,10 0 1,0 40,38Z'
        '"/>\n'
        # Right eye frame (outer)
        '    <path android:fillColor="#4634AE"\n'
        '        android:pathData="'
        'M68,38'
        'A8,10 0 1,0 68,58'
        'A8,10 0 1,0 68,38Z'
        '"/>\n'
        # Left eye white
        '    <path android:fillColor="#FFFFFF"\n'
        '        android:pathData="'
        'M40,40'
        'A6,8 0 1,0 40,56'
        'A6,8 0 1,0 40,40Z'
        '"/>\n'
        # Right eye white
        '    <path android:fillColor="#FFFFFF"\n'
        '        android:pathData="'
        'M68,40'
        'A6,8 0 1,0 68,56'
        'A6,8 0 1,0 68,40Z'
        '"/>\n'
        # Left pupil
        '    <path android:fillColor="#322282"\n'
        '        android:pathData="'
        'M40,43'
        'A4,7 0 1,0 40,57'
        'A4,7 0 1,0 40,43Z'
        '"/>\n'
        # Right pupil
        '    <path android:fillColor="#322282"\n'
        '        android:pathData="'
        'M68,43'
        'A4,7 0 1,0 68,57'
        'A4,7 0 1,0 68,43Z'
        '"/>\n'
        # Left eye shine
        '    <path android:fillColor="#FFFFFF"\n'
        '        android:pathData="'
        'M38,42 A1.5,1.5 0 1,0 38,39 A1.5,1.5 0 1,0 38,42Z'
        '"/>\n'
        # Right eye shine
        '    <path android:fillColor="#FFFFFF"\n'
        '        android:pathData="'
        'M66,42 A1.5,1.5 0 1,0 66,39 A1.5,1.5 0 1,0 66,42Z'
        '"/>\n'
        # Smile (arc)
        '    <path android:fillColor="#00000000"\n'
        '        android:strokeColor="#4634AE"\n'
        '        android:strokeWidth="2.5"\n'
        '        android:strokeLineCap="round"\n'
        '        android:pathData="'
        'M48,66 Q54,72 60,66'
        '"/>\n'
        # Blush left
        '    <path android:fillColor="#FFB4C8"\n'
        '        android:fillAlpha="0.4"\n'
        '        android:pathData="'
        'M32,52 A6,4 0 1,0 32,44 A6,4 0 1,0 32,52Z'
        '"/>\n'
        # Blush right
        '    <path android:fillColor="#FFB4C8"\n'
        '        android:fillAlpha="0.4"\n'
        '        android:pathData="'
        'M76,52 A6,4 0 1,0 76,44 A6,4 0 1,0 76,52Z'
        '"/>\n'
        '</vector>\n'
    )


def main():
    base = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "hermes-android",
        "app",
        "src",
        "main",
        "res",
    )

    # PNG fallback icons for pre-v26
    icons = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }

    for folder, size in icons.items():
        dir_path = os.path.join(base, folder)
        os.makedirs(dir_path, exist_ok=True)
        filepath = os.path.join(dir_path, "ic_launcher.png")
        with open(filepath, "wb") as f:
            f.write(make_png(size, size))
        print(f"  {folder}/ic_launcher.png ({size}x{size})")

    # Drawable - background (purple gradient solid)
    drawable_dir = os.path.join(base, "drawable")
    os.makedirs(drawable_dir, exist_ok=True)

    with open(os.path.join(drawable_dir, "ic_launcher_background.xml"), "w") as f:
        f.write(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
            '    android:width="108dp" android:height="108dp"\n'
            '    android:viewportWidth="108" android:viewportHeight="108">\n'
            '    <path android:fillColor="#302382"\n'
            '        android:pathData="M0,0h108v108h-108z"/>\n'
            '</vector>\n'
        )

    # Drawable - foreground (robot face)
    with open(os.path.join(drawable_dir, "ic_launcher_foreground.xml"), "w") as f:
        f.write(make_foreground_xml())

    # Adaptive icon
    anydpi_dir = os.path.join(base, "mipmap-anydpi-v26")
    os.makedirs(anydpi_dir, exist_ok=True)

    with open(os.path.join(anydpi_dir, "ic_launcher.xml"), "w") as f:
        f.write(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
            '    <background android:drawable="@drawable/ic_launcher_background"/>\n'
            '    <foreground android:drawable="@drawable/ic_launcher_foreground"/>\n'
            '</adaptive-icon>\n'
        )

    print("  🤖 CiCi icons regenerated!")
    print("    - Cute robot assistant face")
    print("    - Purple gradient + adaptive icon")
    print("    - Antenna with green glow tips")


if __name__ == "__main__":
    main()

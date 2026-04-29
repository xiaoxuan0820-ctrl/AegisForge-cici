"""Generate CiCi launcher icons (pure Python, no dependencies)
Design: Dark navy shield with gold "C" crest — clean & professional."""

import struct
import zlib
import os
import math


def make_png(width, height):
    """Generate PNG with a shield + A crest design"""
    def chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack(">I", len(data)) + c + struct.pack(
            ">I", zlib.crc32(c) & 0xFFFFFFFF
        )

    header = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(
        b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    )

    cx, cy = width // 2, height // 2
    r = cx * 0.9  # shield radius

    raw = b""
    for y in range(height):
        raw += b"\x00"  # filter byte
        for x in range(width):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx * dx + dy * dy) / cx

            # Shield shape (squared circle with flat bottom)
            angle = math.atan2(dy, dx)
            shield_radius = r * (
                1.0 - 0.15 * abs(math.sin(angle))
            )
            inside = dist * cx < shield_radius

            if inside:
                # Gold crest area (central C shape — ring open on right)
                nx, ny = dx / cx, dy / cy
                dist = math.sqrt(nx*nx + ny*ny)
                angle = math.atan2(ny, nx)  # 0=right, ±π=left
                inner_r, outer_r = 0.28, 0.52
                in_ring = inner_r < dist < outer_r
                is_gap = abs(angle) < 0.55  # ~30° opening on right
                if in_ring and not is_gap:
                    raw += struct.pack("BBB", 255, 215, 50)  # Gold
                else:
                    raw += struct.pack("BBB", 15, 15, 46)  # Dark navy
            else:
                raw += struct.pack("BBB", 20, 20, 60)  # Outer edge

    idat = chunk(b"IDAT", zlib.compress(raw))
    iend = chunk(b"IEND", b"")
    return header + ihdr + idat + iend


def make_shield_foreground():
    """Return vector XML for the shield + C foreground"""
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
        '    android:width="108dp" android:height="108dp"\n'
        '    android:viewportWidth="108" android:viewportHeight="108">\n'
        # Shield outline (gold)
        '    <path android:fillColor="#FFD700"\n'
        '        android:pathData="'
        'M54,8L12,28v24c0,24 16,42 42,48'
        'c26,-6 42,-24 42,-48V28L54,8Z'
        '"/>\n'
        # Shield inner (dark)
        '    <path android:fillColor="#0F0F2E"\n'
        '        android:pathData="'
        'M54,16L20,32v20c0,19 13,34 34,39'
        'c21,-5 34,-20 34,-39V32L54,16Z'
        '"/>\n'
        # Gold C letter (crest)
        '    <path android:fillColor="#FFD700"\n'
        '        android:pathData="'
        'M54,26'
        'A28,28 0 1,0 54,82'
        'L54,74'
        'A20,20 0 1,1 54,34'
        'Z'
        '"/>\n'
        # Inner accent dot
        '    <path android:fillColor="#FFFFFF"\n'
        '        android:pathData="'
        'M54,50 A4,4 0 1,0 54,58 A4,4 0 1,0 54,50 Z'
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

    # Drawable - background
    drawable_dir = os.path.join(base, "drawable")
    os.makedirs(drawable_dir, exist_ok=True)

    with open(os.path.join(drawable_dir, "ic_launcher_background.xml"), "w") as f:
        f.write(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
            '    android:width="108dp" android:height="108dp"\n'
            '    android:viewportWidth="108" android:viewportHeight="108">\n'
            '    <path android:fillColor="#0F0F2E"\n'
            '        android:pathData="M0,0h108v108h-108z"/>\n'
            '</vector>\n'
        )

    # Drawable - foreground (shield + A)
    with open(os.path.join(drawable_dir, "ic_launcher_foreground.xml"), "w") as f:
        f.write(make_shield_foreground())

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

    print("  🎀 CiCi icons regenerated!")
    print("    - Shield + gold C crest design")
    print("    - Adaptive icon (v26+) + PNG fallback (pre-v26)")


if __name__ == "__main__":
    main()

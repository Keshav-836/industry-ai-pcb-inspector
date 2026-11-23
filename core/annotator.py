import base64

import cv2

# OpenCV BGR format me colors hain (RGB nahi)
RED = (40, 40, 220)
GREEN = (60, 180, 75)
WHITE = (255, 255, 255)


def _scale(image):
    # badi photo pe lines aur text bhi bade hone chahiye, warna dikhenge nahi
    return max(1.0, max(image.shape[:2]) / 1000)


def _draw_label(image, text, x, y, color, scale):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6 * scale
    thickness = max(1, int(1.5 * scale))
    (tw, th), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    # label box ke upar rakho, agar jagah nahi hai to box ke andar
    top = y - th - baseline - 6 if y - th - baseline - 6 > 0 else y
    cv2.rectangle(image, (x, top), (x + tw + 10, top + th + baseline + 6), color, -1)
    cv2.putText(image, text, (x + 5, top + th + 3), font, font_scale, WHITE,
                thickness, cv2.LINE_AA)


#-----------------------------------------------------------


def draw_results(aligned, comparison):
    # original image kharab na ho, isliye copy pe draw karte hain
    canvas = aligned.copy()
    scale = _scale(canvas)

    # pehle present wale (green), phir missing wale (red) taaki red upar dikhe
    ordered = sorted(comparison["parts"], key=lambda p: p["missing"])

    for part in ordered:
        box = part["box"]
        x, y, w, h = box["x"], box["y"], box["w"], box["h"]

        if part["missing"]:
            cv2.rectangle(canvas, (x, y), (x + w, y + h), RED, max(3, int(4 * scale)))
            _draw_label(canvas, f"MISSING: {part['name']}", x, y, RED, scale)
        else:
            cv2.rectangle(canvas, (x, y), (x + w, y + h), GREEN, max(1, int(2 * scale)))

    return canvas


def to_data_url(image, quality=90):
    # image ko base64 JPEG me badal do, taaki browser seedha <img src> me dikha sake
    ok, buffer = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        raise ValueError("Image encode nahi ho payi")
    encoded = base64.b64encode(buffer.tobytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


#---------------------------------------------------------------------


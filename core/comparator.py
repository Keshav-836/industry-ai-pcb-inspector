import cv2
import numpy as np
from skimage.metrics import structural_similarity

# isse upar score aaya to part missing maana jayega
# yeh value sample images pe test karke chuni hai:
# missing parts 0.58+ aaye, present parts 0.24 se neeche
MISSING_THRESHOLD = 0.35

# LAB color me itna farak ho to pixel "badla hua" maana jayega
COLOR_CHANGE_LIMIT = 20


def _crop(image, part):
    x, y, w, h = part["x"], part["y"], part["w"], part["h"]
    return image[y:y + h, x:x + w]


def _normalized_gray(crop):
    # gray + halka blur, phir mean 0 aur std 1 - isse lighting ka farak hat jata hai
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0).astype(np.float32)
    return (gray - gray.mean()) / (gray.std() + 1e-6)


def structure_similarity(ref_crop, test_crop):
    # SSIM: 1 matlab bilkul same shape, 0 ya negative matlab bilkul alag
    a = _normalized_gray(ref_crop)
    b = _normalized_gray(test_crop)
    data_range = float(max(a.max(), b.max()) - min(a.min(), b.min()))
    return float(structural_similarity(a, b, data_range=data_range))

#-----------------------------------------------------------------------------------------------------

def color_change_ratio(ref_crop, test_crop):
    # LAB me sirf A aur B channel dekhte hain (rang), L (brightness) ko chhod dete hain
    # isse roshni kam-zyada hone pe galat alarm nahi aata
    a = cv2.cvtColor(cv2.GaussianBlur(ref_crop, (5, 5), 0), cv2.COLOR_BGR2LAB)
    b = cv2.cvtColor(cv2.GaussianBlur(test_crop, (5, 5), 0), cv2.COLOR_BGR2LAB)
    diff = a[..., 1:].astype(np.float32) - b[..., 1:].astype(np.float32)
    distance = np.sqrt((diff ** 2).sum(axis=-1))
    return float((distance > COLOR_CHANGE_LIMIT).mean())


def check_part(reference, aligned, part):
    ref_crop = _crop(reference, part)
    test_crop = _crop(aligned, part)

    ssim = structure_similarity(ref_crop, test_crop)
    color = color_change_ratio(ref_crop, test_crop)

    # dono signals ka average - shape bhi badli aur rang bhi, to pakka missing
    missing_score = 0.5 * (1 - ssim) + 0.5 * color
    missing_score = max(0.0, min(1.0, missing_score))

    return {
        "name": part["name"],
        "box": {k: part[k] for k in ("x", "y", "w", "h")},
        "missing": missing_score > MISSING_THRESHOLD,
        "score": round(missing_score, 3),
        "ssim": round(ssim, 3),
        "color_change": round(color, 3),
    }


def compare_parts(reference, aligned, parts):
    # har named part check karo aur final verdict do
    results = [check_part(reference, aligned, p) for p in parts]
    missing = [r["name"] for r in results if r["missing"]]
    return {
        "status": "OK" if not missing else "MISSING",
        "missing_parts": missing,
        "parts": results,
    }


#  ------------------------------------------------------------------------------------------------------


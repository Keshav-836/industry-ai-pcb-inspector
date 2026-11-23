import cv2
import numpy as np

# kitne feature points dhoondhne hain - zyada matlab accurate par thoda slow
MAX_FEATURES = 4000

# sabse achhe kitne matches use karenge homography ke liye
KEEP_MATCHES = 500

# itne se kam matches mile to alignment pe bharosa nahi
MIN_MATCHES = 30


def _to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def _find_matches(ref_gray, test_gray):
    # dono photos me ORB feature points nikaalo
    orb = cv2.ORB_create(MAX_FEATURES)
    ref_kp, ref_desc = orb.detectAndCompute(ref_gray, None)
    test_kp, test_desc = orb.detectAndCompute(test_gray, None)

    if ref_desc is None or test_desc is None:
        return [], ref_kp, test_kp

    # crossCheck=True matlab dono taraf se match hona chahiye, galat match kam honge
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(test_desc, ref_desc)
    matches = sorted(matches, key=lambda m: m.distance)[:KEEP_MATCHES]
    return matches, ref_kp, test_kp

#  ---------------------------------------------------------------------------------------------------


def _is_sane(homography, width, height):
    # check karo ki homography pagal to nahi - board ulta ya bahut chhota na ho jaye
    if homography is None:
        return False
    corners = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    moved = cv2.perspectiveTransform(corners.reshape(-1, 1, 2), homography)
    area = cv2.contourArea(moved)
    original_area = width * height
    # area 50% se kam ya double se zyada ho gaya to kuch gadbad hai
    return 0.5 * original_area < area < 2.0 * original_area


def align_to_reference(reference, test):
    """
    Test photo ko reference ke upar fit karta hai.
    Return: (aligned_image, info) - info me batate hain ki alignment hua ya nahi
    """
    height, width = reference.shape[:2]

    # pehle size same kar do, kabhi kabhi 1-2 pixel ka farak hota hai
    if test.shape[:2] != (height, width):
        test = cv2.resize(test, (width, height))

    matches, ref_kp, test_kp = _find_matches(_to_gray(reference), _to_gray(test))

    info = {"aligned": False, "matches": len(matches), "shift_x": 0.0, "shift_y": 0.0}

    if len(matches) < MIN_MATCHES:
        # matches bahut kam - jaisi photo hai waisi hi use karo
        return test, info

    test_pts = np.float32([test_kp[m.queryIdx].pt for m in matches])
    ref_pts = np.float32([ref_kp[m.trainIdx].pt for m in matches])

    # RANSAC galat matches ko ignore kar deta hai (jaise missing part wali jagah)
    homography, _ = cv2.findHomography(test_pts, ref_pts, cv2.RANSAC, 3.0)

    if not _is_sane(homography, width, height):
        return test, info

    aligned = cv2.warpPerspective(test, homography, (width, height),
                                  borderMode=cv2.BORDER_REPLICATE)

    info["aligned"] = True
    info["shift_x"] = round(float(homography[0, 2]), 1)
    info["shift_y"] = round(float(homography[1, 2]), 1)
    return aligned, info

#----------------------------------------------------------------------------------


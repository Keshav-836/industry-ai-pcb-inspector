import json
import os
import sys

import cv2

# project root ko path me daalo taaki "core" import ho sake
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.aligner import align_to_reference
from core.comparator import compare_parts

SAMPLES = "sample_images"


def main():
    reference = cv2.imread(os.path.join(SAMPLES, "reference.png"))
    with open(os.path.join("tools", "sample_parts.json"), encoding="utf-8") as f:
        parts = json.load(f)

    test_dir = os.path.join(SAMPLES, "tests")
    for name in sorted(os.listdir(test_dir)):
        test = cv2.imread(os.path.join(test_dir, name))
        if test is None:
            continue
        aligned, _ = align_to_reference(reference, test)
        result = compare_parts(reference, aligned, parts)
        missing = ", ".join(result["missing_parts"]) or "-"
        print(f"{name:32} {result['status']:8} {missing}")


if __name__ == "__main__":
    main()
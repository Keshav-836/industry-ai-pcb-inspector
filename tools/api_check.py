import json
import os
import sys

# project root ko path me daalo taaki "app" import ho sake
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

SAMPLES = "sample_images"


def main():
    # test_client ek nakli browser hai - server chalaye bina routes call karta hai
    client = create_app().test_client()

    # 1. reference upload karke board banao
    with open(os.path.join(SAMPLES, "reference.png"), "rb") as f:
        res = client.post("/api/boards",
                          data={"image": (f, "reference.png"), "name": "Demo board"})
    board = res.get_json()
    print("1. Board created:", res.status_code, board.get("id"))

    # 2. saare named parts save karo
    with open(os.path.join("tools", "sample_parts.json"), encoding="utf-8") as f:
        parts = json.load(f)
    res = client.put(f"/api/boards/{board['id']}/parts", json={"parts": parts})
    print("2. Parts saved:", res.status_code, len(res.get_json().get("parts", [])))

    # 3. do test photos ek saath check karo
    names = ["test_01_ok.png", "test_07_missing_3.png"]
    files = [(open(os.path.join(SAMPLES, "tests", n), "rb"), n) for n in names]
    res = client.post(f"/api/boards/{board['id']}/inspect", data={"images": files})
    print("3. Inspect:", res.status_code)
    for r in res.get_json()["results"]:
        print("  ", r["filename"], r["status"], r["missing_parts"])


if __name__ == "__main__":
    main()
    
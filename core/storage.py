import json
import os
import re
import uuid
from datetime import datetime

import cv2
import numpy as np

from config import Config

REFERENCE_FILE = "reference.png"
BOARD_FILE = "board.json"

# board id sirf 8 hex characters ki hogi, isse koi galat path nahi bana payega
BOARD_ID_PATTERN = re.compile(r"^[a-f0-9]{8}$")


def allowed_file(filename):
    # extension check karo - sirf images allowed hain
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS


def read_image_from_upload(file_storage):
    # upload ki file ko disk pe save kiye bina seedha OpenCV image bana lo
    data = np.frombuffer(file_storage.read(), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("This file is not a valid image")
    return image


def _board_dir(board_id):
    # galat id aayi to yahin rok do
    if not BOARD_ID_PATTERN.match(board_id or ""):
        raise ValueError("Invalid board id")
    return os.path.join(Config.BOARDS_DIR, board_id)


def _write_board(board):
    path = os.path.join(_board_dir(board["id"]), BOARD_FILE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=2)


def create_board(image, name=""):
    # naya board banao: folder + reference photo + khaali parts list
    board_id = uuid.uuid4().hex[:8]
    folder = _board_dir(board_id)
    os.makedirs(folder, exist_ok=True)

    # hamesha PNG me save karte hain taaki quality loss na ho
    cv2.imwrite(os.path.join(folder, REFERENCE_FILE), image)

    height, width = image.shape[:2]
    board = {
        "id": board_id,
        "name": name.strip() or f"Board {board_id}",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "width": width,
        "height": height,
        "parts": [],
    }
    _write_board(board)
    return board


def load_board(board_id):
    # board.json padho, agar board nahi mila to None
    try:
        path = os.path.join(_board_dir(board_id), BOARD_FILE)
    except ValueError:
        return None
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def reference_path(board_id):
    return os.path.join(_board_dir(board_id), REFERENCE_FILE)


def load_reference_image(board_id):
    image = cv2.imread(reference_path(board_id), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError("Reference photo not found")
    return image


def list_boards():
    # saare boards, naye wale sabse upar
    if not os.path.isdir(Config.BOARDS_DIR):
        return []
    boards = []
    for board_id in os.listdir(Config.BOARDS_DIR):
        board = load_board(board_id)
        if board:
            boards.append(board)
    boards.sort(key=lambda b: b["created_at"], reverse=True)
    return boards


def save_parts(board_id, parts):
    # user ne jo boxes draw kiye unko check karke save karo
    board = load_board(board_id)
    if board is None:
        raise ValueError("Board not found")

    width, height = board["width"], board["height"]
    clean_parts = []
    seen_names = set()

    for part in parts:
        name = str(part.get("name", "")).strip()
        if not name:
            raise ValueError("Every part needs a name")
        if name.lower() in seen_names:
            raise ValueError(f"The name '{name}' is used twice")
        seen_names.add(name.lower())

        # box ko image ke andar hi rakho, bahar nikla to kaat do
        x = max(0, int(part.get("x", 0)))
        y = max(0, int(part.get("y", 0)))
        w = min(int(part.get("w", 0)), width - x)
        h = min(int(part.get("h", 0)), height - y)

        # bahut chhota box matlab galti se click hua hoga
        if w < 5 or h < 5:
            raise ValueError(f"The '{name}' box is too small")

        clean_parts.append({"name": name, "x": x, "y": y, "w": w, "h": h})

    board["parts"] = clean_parts
    _write_board(board)
    return board
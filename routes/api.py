from flask import Blueprint, jsonify, request, send_file

from core import storage
from core.pipeline import inspect_image

# saare routes /api se shuru honge - yeh sab apne laptop pe hi chalte hain
api = Blueprint("api", __name__, url_prefix="/api")

# ek baar me kitni test photos check kar sakte hain
MAX_TEST_IMAGES = 10


def error(message, code=400):
    # saare errors ek hi format me jayenge, frontend ko easy padega
    return jsonify({"error": message}), code


def _read_upload(file):
    # file check + image me convert - galti hui to ValueError
    if file is None or file.filename == "":
        raise ValueError("Please choose an image")
    if not storage.allowed_file(file.filename):
        raise ValueError("Only PNG, JPG or BMP images are allowed")
    return storage.read_image_from_upload(file)


@api.get("/boards")
def list_boards():
    return jsonify(storage.list_boards())


@api.post("/boards")
def create_board():
    try:
        image = _read_upload(request.files.get("image"))
    except ValueError as e:
        return error(str(e))
    board = storage.create_board(image, request.form.get("name", ""))
    return jsonify(board), 201


@api.get("/boards/<board_id>")
def get_board(board_id):
    board = storage.load_board(board_id)
    if board is None:
        return error("Board not found", 404)
    return jsonify(board)


@api.get("/boards/<board_id>/reference")
def get_reference(board_id):
    # browser me reference photo dikhane ke liye
    if storage.load_board(board_id) is None:
        return error("Board not found", 404)
    return send_file(storage.reference_path(board_id), mimetype="image/png")


@api.put("/boards/<board_id>/parts")
def save_parts(board_id):
    data = request.get_json(silent=True) or {}
    try:
        board = storage.save_parts(board_id, data.get("parts", []))
    except ValueError as e:
        return error(str(e))
    return jsonify(board)


@api.post("/boards/<board_id>/inspect")
def inspect(board_id):
    board = storage.load_board(board_id)
    if board is None:
        return error("Board not found", 404)
    if not board["parts"]:
        return error("Name at least one part on the reference first")

    files = request.files.getlist("images")
    if not files:
        return error("Please upload at least one photo")
    if len(files) > MAX_TEST_IMAGES:
        return error(f"You can check up to {MAX_TEST_IMAGES} photos at once")

    # reference ek hi baar load karo, har photo ke liye nahi
    reference = storage.load_reference_image(board_id)
    results = []
    for file in files:
        try:
            test = _read_upload(file)
            result = inspect_image(reference, board["parts"], test)
            results.append({"filename": file.filename, **result})
        except ValueError as e:
            # ek photo kharab hai to baaki photos ka result phir bhi aana chahiye
            results.append({"filename": file.filename, "error": str(e)})

    return jsonify({"board": board["name"], "results": results})
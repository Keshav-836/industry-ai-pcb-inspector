import os

# project ka root folder - baaki saare paths isi se banenge
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # secret key sirf local use ke liye hai, koi online cheez nahi
    SECRET_KEY = os.environ.get("SECRET_KEY", "local-dev-key")

    # yahan saare boards aur unki photos save hongi
    DATA_DIR = os.path.join(BASE_DIR, "data")
    BOARDS_DIR = os.path.join(DATA_DIR, "boards")

    # 20 MB se badi file upload nahi hogi
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024

    # sirf yeh image types allowed hain
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp"}
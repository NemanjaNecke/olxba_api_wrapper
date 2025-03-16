from PIL import Image
from io import BytesIO
import base64

image_file = r"C:\Users\Pc\Downloads\20250301_151109.jpg"


def compress_and_encode(image_path, max_size=(800, 800), quality=85):
    """
    Opens an image, resizes it (keeping aspect ratio) and compresses it,
    then returns a base64 encoded string of the compressed image.

    :param image_path: Path to the image file.
    :param max_size: Maximum width and height as a tuple (width, height).
    :param quality: JPEG quality (1 to 95).
    :return: Base64 encoded string of the compressed image.
    """
    img = Image.open(image_path)
    # Use LANCZOS resampling filter (replacing the removed ANTIALIAS constant)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=quality)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


# One-line example usage to write the encoded string to a file:
open("compressed_image.txt", "w").write(compress_and_encode(image_file))

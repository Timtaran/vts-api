import base64
import aiofiles


class Icon:
    def __init__(self, b64_str):
        self.icon_data = b64_str

    @staticmethod
    def from_file(path: str):
        with open(path, "rb") as image_file:
            return Icon(base64.b64encode(image_file.read()))

    @staticmethod
    async def from_file_async(path: str):
        async with aiofiles.open(path, "rb") as image_file:
            return Icon(base64.b64encode(await image_file.read()))

    @staticmethod
    async def from_bytes(byte_image: bytes):
        return Icon(base64.b64encode(byte_image))

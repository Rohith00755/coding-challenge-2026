import qrcode
import os
import secrets
import string

class Developer:
    def __init__(self, data, file_name):
        self.data = data
        self.file_name = file_name

    def qr_generator(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )

        qr.add_data(self.data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(self.file_name)
    def file_size(self):
        if os.path.isfile(self.file_name):
            file_info = os.stat(self.file_name)
            return self.convert_bytes(file_info.st_size)
        return 0

    def convert_bytes(self, bytes_value):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} TB"
    def generate_random_string(self, length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
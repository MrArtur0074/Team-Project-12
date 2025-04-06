import base64

with open("../files/mark.xlsx", "rb") as photo_file:
    photo_base64 = base64.b64encode(photo_file.read()).decode("utf-8")

print(photo_base64)
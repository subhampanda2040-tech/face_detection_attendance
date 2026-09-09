from PIL import Image, ImageDraw, ImageFont
import urllib.request
import os

img = Image.new('RGB', (1280, 720), color='white')
draw = ImageDraw.Draw(img)

red_color = (226, 92, 73)
light_gray = (240, 240, 240)
dark_gray = (130, 130, 130)
blue_color = (43, 64, 102)
orange_text = (235, 122, 85)

draw.rounded_rectangle([(55, 60), (695, 120)], radius=15, fill=red_color)
draw.rounded_rectangle([(55, 162), (695, 642)], radius=20, fill=red_color)
draw.rounded_rectangle([(55, 660), (695, 705)], radius=15, fill=light_gray)
draw.rounded_rectangle([(720, 115), (1170, 690)], radius=25, fill=blue_color)

try:
    if not os.path.exists("Roboto-Bold.ttf"):
        urllib.request.urlretrieve("https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Bold.ttf", "Roboto-Bold.ttf")
    title_font = ImageFont.truetype("Roboto-Bold.ttf", 26)
    subtitle_font = ImageFont.truetype("Roboto-Bold.ttf", 18)
    req_title_font = ImageFont.truetype("Roboto-Bold.ttf", 38)
    req_list_font = ImageFont.truetype("Roboto-Bold.ttf", 34)
except Exception as e:
    print(e)
    title_font = ImageFont.load_default()
    subtitle_font = title_font
    req_title_font = title_font
    req_list_font = title_font

def draw_centered_text(draw, text, font, fill, x, y, width, height):
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        w, h = draw.textsize(text, font=font)
    draw.text((x + (width - w) / 2, y + (height - h) / 2), text, font=font, fill=fill)

draw_centered_text(draw, "FACE RECOGNITION & ATTENDANCE", title_font, "white", 55, 60, 640, 60)
draw_centered_text(draw, "P R E S S   ' O '   F O R   T A K E   A T T E N D A N C E", subtitle_font, dark_gray, 55, 660, 640, 45)

draw.text((770, 200), "REQUIREMENT", font=req_title_font, fill=orange_text)
draw.text((770, 280), "1.PYTHON", font=req_list_font, fill="white")
draw.text((770, 340), "2.OPENCV", font=req_list_font, fill="white")
draw.text((770, 400), "3.SCIKIT-LEARN", font=req_list_font, fill="white")

if os.path.exists("background.png"):
    import shutil
    shutil.copy("background.png", "background_old.png")
img.save("background.png")
print("Background generated successfully!")

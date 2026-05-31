from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
import os


def apply_watermark(image_field, settings):
    """
    Накладывает водяной знак на изображение.
    Возвращает ContentFile с готовым изображением.
    """
    img = Image.open(image_field).convert('RGBA')
    width, height = img.size

    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    opacity = int(255 * settings.watermark_opacity)

    if settings.watermark_type == 'logo' and settings.logo:
        # Режим: логотип
        try:
            logo = Image.open(settings.logo).convert('RGBA')
            logo_width = width // 4
            ratio = logo_width / logo.width
            logo_height = int(logo.height * ratio)
            logo = logo.resize((logo_width, logo_height), Image.LANCZOS)

            # Накладываем прозрачность
            r, g, b, a = logo.split()
            a = a.point(lambda x: int(x * settings.watermark_opacity))
            logo.putalpha(a)

            # Позиция — правый нижний угол
            position = (width - logo_width - 20, height - logo_height - 20)
            overlay.paste(logo, position, logo)
        except Exception:
            pass
    else:
        # Режим: текст
        text = settings.watermark_text or settings.salon_name
        try:
            font = ImageFont.truetype('arial.ttf', size=max(20, width // 30))
        except Exception:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Позиция — правый нижний угол
        x = width - text_width - 20
        y = height - text_height - 20

        # Тень для читаемости
        draw.text((x + 1, y + 1), text, font=font, fill=(0, 0, 0, opacity // 2))
        draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))

    # Склеиваем слои
    watermarked = Image.alpha_composite(img, overlay)
    watermarked = watermarked.convert('RGB')

    output = BytesIO()
    watermarked.save(output, format='JPEG', quality=90)
    output.seek(0)

    return ContentFile(output.read())
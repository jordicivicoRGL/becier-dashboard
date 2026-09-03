import os
import base64
import requests
from pathlib import Path
from datetime import datetime

OUTPUTS_BASE = Path(__file__).parent.parent / "outputs"

TOGETHER_API_URL = "https://api.together.xyz/v1/images/generations"
MODEL = "black-forest-labs/FLUX.1.1-pro"

FORMAT_SIZES = {
    "1:1":  (1024, 1024),
    "9:16": (576, 1024),
    "4:5":  (1024, 1280),
}

OVERLAY_FONT_CANDIDATES = [
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def generate_image(prompt: str, filename: str = None, client: str = None) -> dict:
    api_key = os.environ.get("TOGETHER_API_KEY")
    if not api_key:
        return {"error": "TOGETHER_API_KEY no está configurada en el archivo .env"}

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"imagen_{timestamp}"

    output_dir = OUTPUTS_BASE / client / "images" if client else OUTPUTS_BASE / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{filename}.png"

    try:
        response = requests.post(
            TOGETHER_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "prompt": prompt,
                "n": 1,
                "width": 1024,
                "height": 1024
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()

        image_data = data["data"][0]

        if "b64_json" in image_data:
            image_bytes = base64.b64decode(image_data["b64_json"])
            with open(output_path, "wb") as f:
                f.write(image_bytes)
        elif "url" in image_data:
            img_response = requests.get(image_data["url"], timeout=30)
            img_response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(img_response.content)
        else:
            return {"error": "Formato de respuesta inesperado de la API de imágenes."}

        return {
            "success": True,
            "filename": f"{filename}.png",
            "path": str(output_path),
            "prompt": prompt,
            "message": f"Imagen generada y guardada en: {output_path}"
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Error de red al generar la imagen: {str(e)}"}
    except Exception as e:
        return {"error": f"Error generando la imagen: {str(e)}"}


def _apply_text_overlay(image_path: Path, text: str, position: str = "bottom", brand_color: str = "#000000") -> Path:
    """Añade un overlay de texto sobre la imagen. Devuelve la ruta del archivo con overlay."""
    from PIL import Image, ImageDraw, ImageFont
    import textwrap

    img = Image.open(image_path).convert("RGBA")
    w, h = img.size

    band_h = int(h * 0.28)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    if position == "bottom":
        y0, y1 = h - band_h, h
    elif position == "top":
        y0, y1 = 0, band_h
    else:
        y0, y1 = (h - band_h) // 2, (h + band_h) // 2

    # Gradiente simulado: 3 bandas de opacidad creciente hacia el borde
    steps = 6
    for i in range(steps):
        alpha = int(180 * (i + 1) / steps)
        if position == "bottom":
            sy = y0 + i * (band_h // steps)
            ey = y0 + (i + 1) * (band_h // steps)
        elif position == "top":
            sy = y1 - (i + 1) * (band_h // steps)
            ey = y1 - i * (band_h // steps)
        else:
            sy = y0 + i * (band_h // steps)
            ey = y0 + (i + 1) * (band_h // steps)
        draw.rectangle([0, sy, w, ey], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    font = None
    font_size = max(28, w // 18)
    for font_path in OVERLAY_FONT_CANDIDATES:
        if Path(font_path).exists():
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except Exception:
                continue
    if font is None:
        font = ImageFont.load_default()

    max_chars = max(10, w // (font_size // 2))
    lines = textwrap.wrap(text, width=max_chars)

    line_h = font_size + 8
    total_text_h = len(lines) * line_h
    text_y = y0 + (band_h - total_text_h) // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        x = (w - text_w) // 2
        # sombra sutil
        draw.text((x + 2, text_y + 2), line, font=font, fill=(0, 0, 0, 180))
        draw.text((x, text_y), line, font=font, fill=(255, 255, 255, 255))
        text_y += line_h

    out_path = image_path.parent / (image_path.stem + "_overlay.png")
    img.save(out_path, "PNG")
    return out_path


def generate_meta_image(
    prompt: str,
    client: str,
    filename: str,
    format: str = "1:1",
    overlay_text: str = None,
    overlay_position: str = "bottom",
) -> dict:
    """Genera una imagen para Meta Ads con soporte de ratio y overlay de texto."""
    api_key = os.environ.get("TOGETHER_API_KEY")
    if not api_key:
        return {"error": "TOGETHER_API_KEY no está configurada en el archivo .env"}

    width, height = FORMAT_SIZES.get(format, (1024, 1024))

    output_dir = OUTPUTS_BASE / client / "imagenes-meta"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{filename}.png"

    try:
        response = requests.post(
            TOGETHER_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "prompt": prompt,
                "n": 1,
                "width": width,
                "height": height,
            },
            timeout=90,
        )
        response.raise_for_status()
        data = response.json()

        image_data = data["data"][0]
        if "b64_json" in image_data:
            image_bytes = base64.b64decode(image_data["b64_json"])
            with open(output_path, "wb") as f:
                f.write(image_bytes)
        elif "url" in image_data:
            img_response = requests.get(image_data["url"], timeout=30)
            img_response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(img_response.content)
        else:
            return {"error": "Formato de respuesta inesperado de la API de imágenes."}

        result = {
            "success": True,
            "filename": f"{filename}.png",
            "path": str(output_path),
            "format": format,
            "size": f"{width}x{height}",
            "prompt": prompt,
        }

        if overlay_text:
            overlay_path = _apply_text_overlay(output_path, overlay_text, overlay_position)
            result["overlay_path"] = str(overlay_path)
            result["overlay_filename"] = overlay_path.name

        result["message"] = f"Imagen guardada en: {output_path}"
        if overlay_text:
            result["message"] += f"\nCon overlay: {result['overlay_path']}"

        return result

    except requests.exceptions.RequestException as e:
        return {"error": f"Error de red al generar la imagen: {str(e)}"}
    except Exception as e:
        return {"error": f"Error generando la imagen: {str(e)}"}

import os
import base64
import mimetypes
import requests
from pathlib import Path
from datetime import datetime

OUTPUTS_BASE = Path(__file__).parent.parent / "outputs"

# "Nano Banana" = Gemini 2.5 Flash Image (API de Google AI Studio / Gemini)
GEMINI_MODEL = "gemini-2.5-flash-image"
GEMINI_API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
)


def _api_key() -> str | None:
    return os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")


def _extract_and_save(data: dict, output_path: Path) -> dict:
    """Recorre la respuesta de Gemini, guarda la primera imagen y devuelve texto adjunto si lo hay."""
    candidates = data.get("candidates", [])
    if not candidates:
        feedback = data.get("promptFeedback", {})
        return {"error": f"Gemini no devolvió ninguna imagen. promptFeedback: {feedback}"}

    parts = candidates[0].get("content", {}).get("parts", [])
    saved = False
    text_note = None

    for part in parts:
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            image_bytes = base64.b64decode(inline["data"])
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            saved = True
        elif "text" in part and part["text"]:
            text_note = part["text"]

    if not saved:
        return {"error": f"La respuesta no contenía datos de imagen. Nota del modelo: {text_note or 'ninguna'}"}

    return {"saved": True, "text_note": text_note}


def generate_image_gemini(prompt: str, filename: str = None, client: str = None) -> dict:
    """Genera una imagen desde cero con Nano Banana (Gemini 2.5 Flash Image)."""
    api_key = _api_key()
    if not api_key:
        return {"error": "GOOGLE_API_KEY no está configurada en el archivo .env"}

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gemini_{timestamp}"

    output_dir = OUTPUTS_BASE / client / "images" if client else OUTPUTS_BASE / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{filename}.png"

    try:
        response = requests.post(
            GEMINI_API_URL,
            headers={
                "x-goog-api-key": api_key,
                "Content-Type": "application/json",
            },
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()

        saved = _extract_and_save(data, output_path)
        if "error" in saved:
            return saved

        result = {
            "success": True,
            "filename": f"{filename}.png",
            "path": str(output_path),
            "prompt": prompt,
            "model": GEMINI_MODEL,
            "message": f"Imagen generada con Nano Banana y guardada en: {output_path}",
        }
        if saved.get("text_note"):
            result["model_note"] = saved["text_note"]
        return result

    except requests.exceptions.RequestException as e:
        detail = ""
        if e.response is not None:
            detail = f" — {e.response.text[:300]}"
        return {"error": f"Error de red al generar la imagen con Gemini: {str(e)}{detail}"}
    except Exception as e:
        return {"error": f"Error generando la imagen con Gemini: {str(e)}"}


def edit_image_gemini(prompt: str, input_path: str, filename: str = None, client: str = None) -> dict:
    """Edita una imagen existente con Nano Banana (Gemini 2.5 Flash Image).

    Permite cambiar fondos, quitar/añadir objetos, modificar estilo o añadir texto,
    manteniendo la coherencia con la imagen original.
    """
    api_key = _api_key()
    if not api_key:
        return {"error": "GOOGLE_API_KEY no está configurada en el archivo .env"}

    src = Path(input_path)
    if not src.exists():
        return {"error": f"No se encontró la imagen de entrada: {input_path}"}

    mime_type = mimetypes.guess_type(str(src))[0] or "image/png"
    with open(src, "rb") as f:
        b64_image = base64.b64encode(f.read()).decode("utf-8")

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{src.stem}_edit_{timestamp}"

    output_dir = OUTPUTS_BASE / client / "images" if client else OUTPUTS_BASE / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{filename}.png"

    try:
        response = requests.post(
            GEMINI_API_URL,
            headers={
                "x-goog-api-key": api_key,
                "Content-Type": "application/json",
            },
            json={
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {"inline_data": {"mime_type": mime_type, "data": b64_image}},
                        ]
                    }
                ]
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()

        saved = _extract_and_save(data, output_path)
        if "error" in saved:
            return saved

        result = {
            "success": True,
            "filename": f"{filename}.png",
            "path": str(output_path),
            "source": str(src),
            "prompt": prompt,
            "model": GEMINI_MODEL,
            "message": f"Imagen editada con Nano Banana y guardada en: {output_path}",
        }
        if saved.get("text_note"):
            result["model_note"] = saved["text_note"]
        return result

    except requests.exceptions.RequestException as e:
        detail = ""
        if e.response is not None:
            detail = f" — {e.response.text[:300]}"
        return {"error": f"Error de red al editar la imagen con Gemini: {str(e)}{detail}"}
    except Exception as e:
        return {"error": f"Error editando la imagen con Gemini: {str(e)}"}

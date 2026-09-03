import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import anthropic

from tools.calendar_tools import get_events, create_event, update_event, delete_event
from tools.gmail_tools import search_emails, send_email
from tools.image_tools import generate_image
from tools.gemini_image_tools import generate_image_gemini, edit_image_gemini
from tools.pdf_tools import create_proposal_pdf
from tools.ads_tools import get_campaigns_stats, set_campaign_status, create_campaign, delete_campaign
from tools.docs_tools import edit_google_doc

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-opus-4-7"
MADRID_TZ = ZoneInfo("Europe/Madrid")

SYSTEM_PROMPT = """Eres Claudito, el asistente personal de Jordi Civico. Eres proactivo, eficiente y hablas siempre en español de manera natural y cercana.

Fecha y hora actual: {current_datetime}

Puedes ayudar a Jordi con:
- 📅 Gestionar su calendario de Google: ver, crear, modificar y eliminar eventos
- 📧 Leer y enviar emails desde su Gmail
- 🎨 Generar imágenes a partir de descripciones de texto (FLUX para algo rápido, o Nano Banana / Gemini para más calidad, texto en imagen o edición de imágenes existentes)
- 📄 Redactar propuestas profesionales en formato PDF
- 📊 Gestionar Google Ads: ver estadísticas de campañas, activar, pausar, crear y eliminar campañas

Cuando Jordi te pida algo relacionado con estas capacidades, usa las herramientas disponibles sin dudar. Si necesitas información adicional, pregúntala de forma concisa. Sé directo y útil."""

TOOLS = [
    {
        "name": "get_calendar_events",
        "description": "Obtiene los eventos del calendario de Google de Jordi para los próximos días.",
        "input_schema": {
            "type": "object",
            "properties": {
                "days_ahead": {
                    "type": "integer",
                    "description": "Número de días hacia adelante para buscar eventos (por defecto 7).",
                    "default": 7
                }
            },
            "required": []
        }
    },
    {
        "name": "create_calendar_event",
        "description": "Crea un nuevo evento en el calendario de Google de Jordi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Título del evento."},
                "start_datetime": {"type": "string", "description": "Fecha y hora de inicio en formato ISO 8601 (ej: 2024-01-15T10:00:00)."},
                "end_datetime": {"type": "string", "description": "Fecha y hora de fin en formato ISO 8601."},
                "description": {"type": "string", "description": "Descripción opcional del evento."},
                "location": {"type": "string", "description": "Ubicación opcional del evento."}
            },
            "required": ["title", "start_datetime", "end_datetime"]
        }
    },
    {
        "name": "update_calendar_event",
        "description": "Modifica un evento existente en el calendario de Google de Jordi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "ID del evento a modificar."},
                "title": {"type": "string", "description": "Nuevo título del evento."},
                "start_datetime": {"type": "string", "description": "Nueva fecha y hora de inicio en formato ISO 8601."},
                "end_datetime": {"type": "string", "description": "Nueva fecha y hora de fin en formato ISO 8601."},
                "description": {"type": "string", "description": "Nueva descripción del evento."},
                "location": {"type": "string", "description": "Nueva ubicación del evento."}
            },
            "required": ["event_id"]
        }
    },
    {
        "name": "delete_calendar_event",
        "description": "Elimina un evento del calendario de Google de Jordi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "ID del evento a eliminar."}
            },
            "required": ["event_id"]
        }
    },
    {
        "name": "search_emails",
        "description": "Busca emails en el Gmail de Jordi usando una consulta.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Consulta de búsqueda (usa sintaxis de Gmail, ej: 'from:example@gmail.com subject:reunión')."},
                "max_results": {"type": "integer", "description": "Número máximo de resultados (por defecto 10).", "default": 10}
            },
            "required": ["query"]
        }
    },
    {
        "name": "send_email",
        "description": "Envía un email desde el Gmail de Jordi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Dirección de email del destinatario."},
                "subject": {"type": "string", "description": "Asunto del email."},
                "body": {"type": "string", "description": "Cuerpo del email. Puede incluir HTML básico."}
            },
            "required": ["to", "subject", "body"]
        }
    },
    {
        "name": "generate_image",
        "description": "Genera una imagen a partir de una descripción de texto usando IA.",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Descripción detallada de la imagen a generar."},
                "filename": {"type": "string", "description": "Nombre del archivo de salida sin extensión (opcional)."}
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "generate_image_gemini",
        "description": "Genera una imagen desde cero con Nano Banana (Gemini 2.5 Flash Image de Google). Mejor que generate_image para prompts con texto, instrucciones complejas o cuando se necesita más realismo y control. Úsala como alternativa a generate_image cuando Jordi lo pida o cuando la calidad importe.",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Descripción detallada de la imagen a generar."},
                "filename": {"type": "string", "description": "Nombre del archivo de salida sin extensión (opcional)."},
                "client": {"type": "string", "description": "Nombre del cliente para organizar el output en outputs/[cliente]/images/ (opcional)."}
            },
            "required": ["prompt"]
        }
    },
    {
        "name": "edit_image_gemini",
        "description": "Edita una imagen existente con Nano Banana (Gemini 2.5 Flash Image). Permite cambiar fondos, quitar o añadir objetos, modificar estilo, añadir texto o mantener la coherencia de un producto o personaje entre varias imágenes. Requiere la ruta de la imagen de entrada.",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Instrucción de edición. Ej: 'cambia el fondo a un estudio blanco', 'quita la persona del fondo', 'añade el texto OFERTA arriba'."},
                "input_path": {"type": "string", "description": "Ruta completa de la imagen a editar."},
                "filename": {"type": "string", "description": "Nombre del archivo de salida sin extensión (opcional)."},
                "client": {"type": "string", "description": "Nombre del cliente para organizar el output en outputs/[cliente]/images/ (opcional)."}
            },
            "required": ["prompt", "input_path"]
        }
    },
    {
        "name": "create_proposal_pdf",
        "description": "Crea una propuesta profesional en formato PDF a partir de una transcripción o briefing.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Título de la propuesta."},
                "sections": {
                    "type": "array",
                    "description": "Lista de secciones de la propuesta.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "heading": {"type": "string", "description": "Título de la sección."},
                            "content": {"type": "string", "description": "Contenido de la sección. Usar '- ' para listas con viñetas."}
                        },
                        "required": ["heading", "content"]
                    }
                },
                "client_name": {"type": "string", "description": "Nombre del cliente (opcional)."},
                "filename": {"type": "string", "description": "Nombre del archivo de salida sin extensión (opcional)."}
            },
            "required": ["title", "sections"]
        }
    },
    {
        "name": "get_campaigns_stats",
        "description": "Obtiene estadísticas de las campañas de Google Ads: impresiones, clics, coste, conversiones, CTR y CPC medio.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date_range": {
                    "type": "string",
                    "description": "Período de tiempo. Valores posibles: LAST_7_DAYS, LAST_14_DAYS, LAST_30_DAYS, THIS_MONTH, LAST_MONTH, THIS_YEAR. Por defecto LAST_30_DAYS.",
                    "default": "LAST_30_DAYS"
                }
            },
            "required": []
        }
    },
    {
        "name": "set_campaign_status",
        "description": "Activa o pausa una campaña de Google Ads.",
        "input_schema": {
            "type": "object",
            "properties": {
                "campaign_id": {"type": "string", "description": "ID numérico de la campaña."},
                "action": {"type": "string", "description": "Estado a aplicar: 'ENABLED' para activar, 'PAUSED' para pausar."}
            },
            "required": ["campaign_id", "action"]
        }
    },
    {
        "name": "create_campaign",
        "description": "Crea una nueva campaña de búsqueda en Google Ads. Se crea en estado PAUSED para revisión antes de activar.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Nombre de la campaña."},
                "daily_budget_eur": {"type": "number", "description": "Presupuesto diario en euros."},
                "start_date": {"type": "string", "description": "Fecha de inicio en formato YYYYMMDD (opcional)."},
                "end_date": {"type": "string", "description": "Fecha de fin en formato YYYYMMDD (opcional)."}
            },
            "required": ["name", "daily_budget_eur"]
        }
    },
    {
        "name": "delete_campaign",
        "description": "Elimina permanentemente una campaña de Google Ads. Esta acción es irreversible.",
        "input_schema": {
            "type": "object",
            "properties": {
                "campaign_id": {"type": "string", "description": "ID numérico de la campaña a eliminar."}
            },
            "required": ["campaign_id"]
        }
    },
    {
        "name": "edit_google_doc",
        "description": "Edita un Google Doc aplicando reemplazos de texto. Útil para corregir errores ortográficos o actualizar contenido.",
        "input_schema": {
            "type": "object",
            "properties": {
                "document_id": {"type": "string", "description": "ID del documento de Google Docs (extraído de la URL del doc)."},
                "replacements": {
                    "type": "array",
                    "description": "Lista de reemplazos a aplicar.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "find": {"type": "string", "description": "Texto a buscar."},
                            "replace": {"type": "string", "description": "Texto de sustitución."}
                        },
                        "required": ["find", "replace"]
                    }
                }
            },
            "required": ["document_id", "replacements"]
        }
    }
]

TOOL_ICONS = {
    "get_calendar_events": "📅",
    "create_calendar_event": "📅",
    "update_calendar_event": "📅",
    "delete_calendar_event": "📅",
    "search_emails": "📧",
    "send_email": "📧",
    "generate_image": "🎨",
    "generate_image_gemini": "🍌",
    "edit_image_gemini": "🍌",
    "create_proposal_pdf": "📄",
    "get_campaigns_stats": "📊",
    "set_campaign_status": "📊",
    "create_campaign": "📊",
    "delete_campaign": "📊",
    "edit_google_doc": "📝",
}


def execute_tool(tool_name: str, tool_input: dict) -> str:
    try:
        if tool_name == "get_calendar_events":
            result = get_events(**tool_input)
        elif tool_name == "create_calendar_event":
            result = create_event(**tool_input)
        elif tool_name == "update_calendar_event":
            result = update_event(**tool_input)
        elif tool_name == "delete_calendar_event":
            result = delete_event(**tool_input)
        elif tool_name == "search_emails":
            result = search_emails(**tool_input)
        elif tool_name == "send_email":
            result = send_email(**tool_input)
        elif tool_name == "generate_image":
            result = generate_image(**tool_input)
        elif tool_name == "generate_image_gemini":
            result = generate_image_gemini(**tool_input)
        elif tool_name == "edit_image_gemini":
            result = edit_image_gemini(**tool_input)
        elif tool_name == "create_proposal_pdf":
            result = create_proposal_pdf(**tool_input)
        elif tool_name == "get_campaigns_stats":
            result = get_campaigns_stats(**tool_input)
        elif tool_name == "set_campaign_status":
            result = set_campaign_status(**tool_input)
        elif tool_name == "create_campaign":
            result = create_campaign(**tool_input)
        elif tool_name == "delete_campaign":
            result = delete_campaign(**tool_input)
        elif tool_name == "edit_google_doc":
            result = edit_google_doc(**tool_input)
        else:
            result = {"error": f"Herramienta desconocida: {tool_name}"}
        return str(result)
    except Exception as e:
        return str({"error": f"Error ejecutando {tool_name}: {str(e)}"})


def print_tool_call(tool_name: str, tool_input: dict):
    icon = TOOL_ICONS.get(tool_name, "🔧")
    print(f"\n{icon} Usando herramienta: {tool_name}")
    if tool_input:
        for key, value in tool_input.items():
            val_str = str(value)
            if len(val_str) > 80:
                val_str = val_str[:80] + "..."
            print(f"   {key}: {val_str}")


def chat(messages: list) -> str:
    current_datetime = datetime.now(MADRID_TZ).strftime("%A, %d de %B de %Y a las %H:%M")
    system = SYSTEM_PROMPT.format(current_datetime=current_datetime)

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=system,
            tools=TOOLS,
            messages=messages,
            thinking={"type": "adaptive"}
        )

        if response.stop_reason == "end_turn":
            text_blocks = [b.text for b in response.content if hasattr(b, "text")]
            return "\n".join(text_blocks)

        tool_calls = [b for b in response.content if b.type == "tool_use"]
        if not tool_calls:
            text_blocks = [b.text for b in response.content if hasattr(b, "text")]
            return "\n".join(text_blocks)

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for tool_call in tool_calls:
            print_tool_call(tool_call.name, tool_call.input)
            result = execute_tool(tool_call.name, tool_call.input)
            print(f"   ✓ Resultado: {result[:100]}{'...' if len(result) > 100 else ''}")
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": result
            })

        messages.append({"role": "user", "content": tool_results})


def main():
    print("=" * 60)
    print("  🤖 Claudito — Tu asistente personal")
    print("=" * 60)
    print("  Escribe 'salir' o 'exit' para terminar la sesión.")
    print("=" * 60)
    print()

    conversation_history = []

    while True:
        try:
            user_input = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n¡Hasta luego, Jordi! 👋")
            sys.exit(0)

        if not user_input:
            continue

        if user_input.lower() in ("salir", "exit", "quit", "bye"):
            print("\n¡Hasta luego, Jordi! 👋")
            sys.exit(0)

        conversation_history.append({"role": "user", "content": user_input})

        print("\nClaudito: ", end="", flush=True)
        response = chat(conversation_history)
        print(response)
        print()

        conversation_history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()

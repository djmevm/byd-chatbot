from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from fuzzywuzzy import fuzz

# Catálogo de modelos BYD con información detallada
CATALOGO_BYD = {
    "seal": {
        "nombre": "BYD Seal",
        "precio": 35000,
        "tipo": "Sedán eléctrico",
        "autonomia": "570 km",
        "potencia": "313 HP (versión AWD)",
        "carga_rapida": "Sí, DC hasta 150 kW",
        "caracteristicas": "Pantalla giratoria 15.6\", sistema DiLink, techo panorámico, carga bidireccional V2L",
        "colores": ["Blanco", "Negro", "Azul", "Gris", "Rojo"],
    },
    "han": {
        "nombre": "BYD Han",
        "precio": 45000,
        "tipo": "Sedán eléctrico premium",
        "autonomia": "605 km",
        "potencia": "469 HP (AWD)",
        "carga_rapida": "Sí, DC hasta 120 kW",
        "caracteristicas": "Diseño Dragon Face, pantalla 12.8\", sistema de sonido premium, suspensión adaptativa",
        "colores": ["Blanco Perla", "Negro", "Azul Océano", "Gris Titanio"],
    },
    "atto 3": {
        "nombre": "BYD Atto 3",
        "precio": 30000,
        "tipo": "SUV eléctrico",
        "autonomia": "480 km",
        "potencia": "201 HP",
        "carga_rapida": "Sí, DC hasta 80 kW",
        "caracteristicas": "SUV compacto, pantalla 12.8\" giratoria, techo panorámico, 5 plazas",
        "colores": ["Blanco", "Rojo", "Verde", "Azul", "Gris"],
    },
    "tang": {
        "nombre": "BYD Tang",
        "precio": 50000,
        "tipo": "SUV eléctrico 7 plazas",
        "autonomia": "530 km",
        "potencia": "517 HP (AWD)",
        "carga_rapida": "Sí, DC hasta 110 kW",
        "caracteristicas": "7 plazas, tracción total, pantalla 15.6\", sistema de sonido Dynaudio",
        "colores": ["Blanco", "Negro", "Gris Espacial"],
    },
    "song plus": {
        "nombre": "BYD Song Plus",
        "precio": 28000,
        "tipo": "SUV híbrido enchufable / eléctrico",
        "autonomia": "100 km eléctrico / 1200 km híbrido",
        "potencia": "197 HP",
        "carga_rapida": "Carga AC 7 kW",
        "caracteristicas": "Híbrido DM-i, bajo consumo, pantalla 12.8\", ideal para ciudad y carretera",
        "colores": ["Blanco", "Negro", "Azul", "Gris"],
    },
    "dolphin": {
        "nombre": "BYD Dolphin",
        "precio": 22000,
        "tipo": "Hatchback eléctrico",
        "autonomia": "427 km",
        "potencia": "177 HP",
        "carga_rapida": "Sí, DC hasta 60 kW",
        "caracteristicas": "Diseño divertido, pantalla 12.8\" giratoria, ideal para ciudad, 5 plazas",
        "colores": ["Blanco", "Azul Cielo", "Verde Menta", "Naranja", "Gris"],
    },
    "seagull": {
        "nombre": "BYD Seagull",
        "precio": 15000,
        "tipo": "City car eléctrico",
        "autonomia": "405 km",
        "potencia": "74 HP",
        "carga_rapida": "Carga AC 6.6 kW",
        "caracteristicas": "El más accesible de BYD, perfecto para ciudad, 4 plazas, bajo costo de mantenimiento",
        "colores": ["Blanco", "Azul", "Amarillo", "Gris", "Verde"],
    },
}


def buscar_modelo(texto: str) -> dict | None:
    """Busca un modelo usando fuzzy matching para mayor tolerancia a errores."""
    if not texto:
        return None
    texto_lower = texto.lower()
    mejor_match = None
    mejor_score = 0
    for key, modelo in CATALOGO_BYD.items():
        score = fuzz.partial_ratio(texto_lower, key)
        if score > mejor_score and score >= 60:
            mejor_score = score
            mejor_match = modelo
    return mejor_match


class ActionInfoModelo(Action):
    def name(self) -> Text:
        return "action_info_modelo"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        modelo_slot = tracker.get_slot("modelo_auto")
        modelo = buscar_modelo(modelo_slot) if modelo_slot else None

        if modelo:
            mensaje = (
                f"🚗 *{modelo['nombre']}*\n\n"
                f"💰 Precio: desde ${modelo['precio']:,} USD\n"
                f"🔋 Autonomía: {modelo['autonomia']}\n"
                f"⚡ Potencia: {modelo['potencia']}\n"
                f"🔌 Carga rápida: {modelo['carga_rapida']}\n"
                f"✨ Características: {modelo['caracteristicas']}\n"
                f"🎨 Colores: {', '.join(modelo['colores'])}\n\n"
                f"¿Te gustaría agendar una prueba de manejo o conocer las opciones de financiamiento?"
            )
        else:
            mensaje = (
                "No encontré ese modelo específico. Nuestros modelos disponibles son:\n"
                "Seal, Han, Atto 3, Tang, Song Plus, Dolphin y Seagull.\n"
                "¿Sobre cuál te gustaría información?"
            )

        dispatcher.utter_message(text=mensaje)
        return []


class ActionCalcularFinanciamiento(Action):
    def name(self) -> Text:
        return "action_calcular_financiamiento"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        modelo_slot = tracker.get_slot("modelo_auto")
        modelo = buscar_modelo(modelo_slot) if modelo_slot else None

        if modelo:
            precio = modelo["precio"]
            enganche = precio * 0.20
            monto_financiar = precio - enganche
            cuota_36 = (monto_financiar * 0.08 / 12) / (1 - (1 + 0.08 / 12) ** -36)
            cuota_48 = (monto_financiar * 0.08 / 12) / (1 - (1 + 0.08 / 12) ** -48)
            cuota_60 = (monto_financiar * 0.08 / 12) / (1 - (1 + 0.08 / 12) ** -60)

            mensaje = (
                f"💳 Financiamiento para {modelo['nombre']} (${precio:,} USD)\n\n"
                f"📌 Enganche mínimo (20%): ${enganche:,.0f} USD\n"
                f"📌 Monto a financiar: ${monto_financiar:,.0f} USD\n\n"
                f"Cuotas mensuales estimadas (tasa 8% anual):\n"
                f"• 36 meses: ${cuota_36:,.0f}/mes\n"
                f"• 48 meses: ${cuota_48:,.0f}/mes\n"
                f"• 60 meses: ${cuota_60:,.0f}/mes\n\n"
                f"*Valores referenciales. Un asesor te dará la cotización exacta.*\n"
                f"¿Te gustaría que un asesor te contacte?"
            )
        else:
            mensaje = (
                "💳 Opciones de financiamiento BYD:\n\n"
                "• Contado: descuento del 5%\n"
                "• Crédito directo: hasta 60 meses, tasa desde 8% anual\n"
                "• Enganche mínimo: 20% del valor\n"
                "• Crédito bancario con los principales bancos\n\n"
                "¿Sobre qué modelo quieres calcular las cuotas?"
            )

        dispatcher.utter_message(text=mensaje)
        return []


class ActionGuardarLead(Action):
    def name(self) -> Text:
        return "action_guardar_lead"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        nombre = tracker.get_slot("nombre_cliente") or "Cliente"
        telefono = tracker.get_slot("telefono") or "No proporcionado"
        modelo = tracker.get_slot("modelo_auto") or "No especificado"
        presupuesto = tracker.get_slot("presupuesto") or "No especificado"

        # Aquí puedes integrar con una base de datos o CRM
        # Por ahora lo registramos en consola (en producción usar DB)
        print(f"[LEAD BYD] Nombre: {nombre} | Tel: {telefono} | Modelo: {modelo} | Presupuesto: {presupuesto}")

        dispatcher.utter_message(
            text=f"¡Perfecto, {nombre}! Hemos registrado tu interés. "
            f"Un asesor de Concesionario BYD te contactará pronto al {telefono}. "
            f"¡Gracias por tu preferencia! 🚗"
        )
        return []

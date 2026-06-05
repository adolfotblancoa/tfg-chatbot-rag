from app.rag.prompt_builder import normalize_question


def get_static_response(message: str) -> str | None:
    text = normalize_question(message)

    greetings = {
        "hola", "buenas", "buenos dias", "buenas tardes",
        "buenas noches", "hey", "holi"
    }

    thanks = {
        "gracias", "muchas gracias", "graciass"
    }

    farewells = {
        "adios", "hasta luego", "nos vemos", "hasta pronto"
    }

    admission_keywords = [
        "admision", "matricula", "preinscripcion",
        "como entrar", "requisitos de acceso", "proceso de admision", "que necesito para aplicar"
    ]

    price_keywords = [
        "precio", "precios", "coste", "costo",
        "cuanto cuesta", "tasas"
    ]

    if text in greetings:
        return (
            "¡Hola! Soy el asistente de la Universidad CEU San Pablo. "
            "Puedo ayudarte con información sobre grados, dobles grados, idiomas, "
            "prácticas, campus, admisión y precios. ¿En qué puedo ayudarte?"
        )

    if text in thanks:
        return "¡De nada! Si necesitas más información sobre el CEU, aquí estoy para ayudarte."

    if text in farewells:
        return "¡Hasta luego! Ha sido un placer ayudarte."

    if any(keyword in text for keyword in admission_keywords):
        return (
            "El proceso de admisión para estudios de grado en la Universidad CEU San Pablo "
            "incluye la solicitud de admisión y la presentación de la documentación requerida. "
            "Puedes consultar la información oficial y actualizada aquí:\n\n"
            "https://www.uspceu.com/admision-ayuda/admision-grado/informacion-admision"
        )

    if any(keyword in text for keyword in price_keywords):
        return (
            "Los precios dependen del grado y del curso académico. "
            "Puedes consultar la información oficial y actualizada aquí:\n\n"
            "https://www.uspceu.com/admision-ayuda/admision-grado/precios"
        )

    return None
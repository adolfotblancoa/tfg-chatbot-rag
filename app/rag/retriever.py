import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings

COLLECTION_NAME = "ceu_knowledge"

client = chromadb.PersistentClient(path=settings.chroma_db_path)

embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=settings.openai_api_key,
    model_name="text-embedding-3-small"
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)


def detect_faculty_from_query(query: str) -> str | None:
    query_lower = query.lower()

    mappings = {
        "farmacia": [
            "farmacia",
            "farmacéutico",
            "farmaceutico",
            "farmacéutica",
            "farmaceutica",
            "biotecnologia",
            "biotecnología",
            "nutricion",
            "nutrición",
            "optica",
            "óptica",
            "optometria",
            "optometría"
        ],
        "medicina": [
            "medicina",
            "medico",
            "médico",
            "medica",
            "médica",
            "mir",
            "enfermeria",
            "enfermería",
            "fisioterapia",
            "odontologia",
            "odontología",
            "psicologia",
            "psicología",
            "genetica",
            "genética",
            "bioinformatica",
            "bioinformática",
            "big data"
        ],
        "derecho": [
            "derecho",
            "juridico",
            "jurídico",
            "juridica",
            "jurídica",
            "abogado",
            "abogada",
            "abogacia",
            "abogacía",
            "ley",
            "leyes",
            "legal",
            "legales",
            "fiscal",
            "criminologia",
            "criminología",
            "politica",
            "política",
            "relaciones internacionales"
        ],
        "eps": [
            "eps",
            "ingenieria",
            "ingeniería",
            "informatica",
            "informática",
            "arquitectura",
            "politecnica",
            "politécnica",
            "datos",
            "software",
            "hardware",
            "telecom",
            "telecomunicacion",
            "telecomunicación"
        ],
        "humanidades_comunicacion": [
            "humanidades",
            "comunicacion",
            "comunicación",
            "periodismo",
            "publicidad",
            "audiovisual",
            "marketing",
            "historia",
            "filologia",
            "filología",
            "arte"
        ],
        "economicas": [
            "economicas",
            "económicas",
            "economia",
            "economía",
            "empresa",
            "empresas",
            "ade",
            "administracion",
            "administración",
            "direccion de empresas",
            "dirección de empresas",
            "finanzas",
            "contabilidad",
            "negocios",
            "business",
            "management",
            "emprendimiento"
        ]
    }

    for faculty, keywords in mappings.items():
        if any(keyword in query_lower for keyword in keywords):
            return faculty

    return None


def retrieve_context(query: str, n_results: int = 3) -> list[str]:
    detected_faculty = detect_faculty_from_query(query)

    if detected_faculty:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"faculty": detected_faculty}
        )
    else:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )

    documents = results.get("documents", [[]])[0]
    return documents


def retrieve_context_with_metadata(query: str, n_results: int = 3) -> dict:
    detected_faculty = detect_faculty_from_query(query)

    if detected_faculty:
        return collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"faculty": detected_faculty}
        )

    return collection.query(
        query_texts=[query],
        n_results=n_results
    )
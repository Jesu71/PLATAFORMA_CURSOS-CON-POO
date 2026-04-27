"""
Configuración centralizada del sistema E-Learning.
Incluye credenciales de Supabase y parámetros generales.
"""

# ─── Configuración de Supabase ───────────────────────────────────────
SUPABASE_URL= "https://wmklctpjxnrocvaphxok.supabase.co"
SUPABASE_KEY= "sb_publishable_AMQMEZJXLT_S41DZw7WAvg_PqJKuGXU"

# ─── Configuración General ───────────────────────────────────────────
DATA_FOLDER = "data"
JSON_FILENAME = "elearning_datos.json"
CAPACIDAD_MAXIMA_CURSO = 30

# ─── Modo de almacenamiento ──────────────────────────────────────────
# Opciones: "supabase" | "json" | "hibrido" (guarda en ambos, carga de Supabase primero)
MODO_ALMACENAMIENTO = "hibrido"
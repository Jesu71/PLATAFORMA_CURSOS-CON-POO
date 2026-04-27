"""
Patrón Repositorio — Capa de persistencia abstracta.
Con Sincronización Offline/Online y Auto-Reconexión.

PILARES POO IMPLEMENTADOS:
  • ABSTRACCIÓN:    RepositorioDatos (ABC) define el contrato de persistencia.
  • HERENCIA:       RepositorioJSON, RepositorioSupabase y RepositorioHibrido heredan de RepositorioDatos.
  • POLIMORFISMO:   El sistema llama a guardar_todo() sin saber si hay internet o no.
  • ENCAPSULAMIENTO: La lógica de reconexión y timestamps está oculta dentro del repositorio.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime
import json
import os

from config import (
    SUPABASE_URL,
    SUPABASE_KEY,
    DATA_FOLDER,
    JSON_FILENAME,
    MODO_ALMACENAMIENTO,
)


class RepositorioDatos(ABC):
    """Clase abstracta que define el contrato de persistencia."""

    @abstractmethod
    def guardar_todo(self, datos: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def cargar_todo(self) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def esta_disponible(self) -> bool:
        pass


class RepositorioJSON(RepositorioDatos):
    """Persistencia en archivo JSON local."""

    def __init__(self) -> None:
        self.__ruta = os.path.join(DATA_FOLDER, JSON_FILENAME)
        self._asegurar_carpeta()

    def _asegurar_carpeta(self) -> None:
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)

    def esta_disponible(self) -> bool:
        return True

    def guardar_todo(self, datos: Dict[str, Any]) -> bool:
        try:
            datos["last_updated"] = datos.get("last_updated", datetime.now().isoformat())
            with open(self.__ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[RepositorioJSON] Error guardando: {e}")
            return False

    def cargar_todo(self) -> Optional[Dict[str, Any]]:
        if not os.path.exists(self.__ruta):
            return None
        try:
            with open(self.__ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
                if "last_updated" not in datos:
                    datos["last_updated"] = "1970-01-01T00:00:00"
                return datos
        except Exception as e:
            print(f"[RepositorioJSON] Error cargando: {e}")
            return None

    @property
    def ruta(self) -> str:
        return self.__ruta


class RepositorioSupabase(RepositorioDatos):
    """
    Persistencia en Supabase con Auto-Reconexión.
    Si se pierde la conexión, intentará reconectar automáticamente en el siguiente guardado/carga.
    """

    def __init__(self) -> None:
        self.__cliente: Any = None
        self.__disponible: bool = False
        self._inicializar_cliente()

    def _inicializar_cliente(self) -> None:
        """Intenta establecer conexión con Supabase."""
        try:
            from supabase import create_client
            self.__cliente = create_client(SUPABASE_URL, SUPABASE_KEY)
            self.__cliente.table("estudiantes").select("id").limit(1).execute()
            self.__disponible = True
            print("[RepositorioSupabase] ✅ Conexión exitosa.")
        except ImportError:
            print("[RepositorioSupabase] ❌ Librería 'supabase' no instalada.")
            self.__disponible = False
        except Exception:
            # Silenciamos el error para no spamear la consola cada vez que intenta reconectar
            self.__disponible = False

    def _intentar_reconectar(self) -> bool:
        """Si está caído, intenta reconectar. Retorna True si la conexión se restableció."""
        if not self.__disponible:
            print("[RepositorioSupabase] 🔄 Intentando reconectar a la nube...")
            self._inicializar_cliente()
        return self.__disponible

    def esta_disponible(self) -> bool:
        return self.__disponible

    def guardar_todo(self, datos: Dict[str, Any]) -> bool:
        # Intentamos reconectar si estaba caído
        if not self.__disponible and not self._intentar_reconectar():
            return False # Seguimos sin internet
            
        try:
            timestamp = datos.get("last_updated", datetime.now().isoformat())
            self.__cliente.table("system_state").delete().neq("id", -1).execute()
            self.__cliente.table("system_state").insert({"id": 1, "last_updated": timestamp}).execute()

            self.__cliente.table("inscripciones").delete().neq("estudiante_id", -1).execute()
            self.__cliente.table("prerequisitos").delete().neq("curso_id", -1).execute()
            self.__cliente.table("materiales").delete().neq("id", -1).execute()
            self.__cliente.table("cursos").delete().neq("id", -1).execute()
            self.__cliente.table("estudiantes").delete().neq("id", -1).execute()

            filas_est = [{"id": e["id"], "nombre": e["nombre"], "email": e.get("email", "")} for e in datos.get("estudiantes", [])]
            if filas_est:
                self.__cliente.table("estudiantes").insert(filas_est).execute()

            filas_cursos = []
            for c in datos.get("cursos", []):
                filas_cursos.append({"id": c["id"], "nombre": c["nombre"], "descripcion": c.get("descripcion", ""), "nivel": c.get("nivel", ""), "eliminado": False})
            for c in datos.get("cursos_eliminados", []):
                filas_cursos.append({"id": c["id"], "nombre": c["nombre"], "descripcion": c.get("descripcion", ""), "nivel": c.get("nivel", ""), "eliminado": True})
            if filas_cursos:
                self.__cliente.table("cursos").insert(filas_cursos).execute()

            filas_mat = []
            for c in datos.get("cursos", []):
                for m in c.get("materiales", []):
                    filas_mat.append({"id": m["id"], "curso_id": c["id"], "nombre": m["nombre"], "tipo": m.get("tipo", ""), "url": m.get("url", ""), "eliminado": False})
            for m in datos.get("materiales_eliminados", []):
                filas_mat.append({"id": m["id"], "curso_id": None, "nombre": m["nombre"], "tipo": m.get("tipo", ""), "url": m.get("url", ""), "eliminado": True})
            if filas_mat:
                self.__cliente.table("materiales").insert(filas_mat).execute()

            filas_pre = []
            for c in datos.get("cursos", []):
                for pre_id in c.get("prerequisitos", []):
                    filas_pre.append({"curso_id": c["id"], "prerequisito_id": pre_id, "eliminado": False})
            for key, pre_list in datos.get("prerequisitos_eliminados", {}).items():
                for pre_id in pre_list:
                    filas_pre.append({"curso_id": int(key), "prerequisito_id": int(pre_id), "eliminado": True})
            if filas_pre:
                self.__cliente.table("prerequisitos").insert(filas_pre).execute()

            filas_ins = []
            for c in datos.get("cursos", []):
                for est_id in c.get("estudiantes", []):
                    filas_ins.append({"estudiante_id": est_id, "curso_id": c["id"]})
            if filas_ins:
                self.__cliente.table("inscripciones").insert(filas_ins).execute()

            return True
        except Exception as e:
            print(f"[RepositorioSupabase] ❌ Error guardando en la nube: {e}")
            self.__disponible = False # Marcamos como caído para intentar reconectar después
            return False

    def cargar_todo(self) -> Optional[Dict[str, Any]]:
        # Intentamos reconectar si estaba caído
        if not self.__disponible and not self._intentar_reconectar():
            return None

        try:
            datos: Dict[str, Any] = {}

            res_time = self.__cliente.table("system_state").select("last_updated").eq("id", 1).execute()
            datos["last_updated"] = res_time.data[0]["last_updated"] if res_time.data else "1970-01-01T00:00:00Z"

            result = self.__cliente.table("estudiantes").select("*").execute()
            datos["estudiantes"] = [{"id": r["id"], "nombre": r["nombre"], "email": r.get("email", ""), "cursos": []} for r in result.data]

            result_cursos = self.__cliente.table("cursos").select("*").eq("eliminado", False).execute()
            result_mat = self.__cliente.table("materiales").select("*").eq("eliminado", False).execute()
            result_pre = self.__cliente.table("prerequisitos").select("*").eq("eliminado", False).execute()
            result_ins = self.__cliente.table("inscripciones").select("*").execute()

            mat_por_curso: Dict[int, list] = {}
            for m in result_mat.data:
                cid = m.get("curso_id")
                if cid is not None:
                    mat_por_curso.setdefault(cid, []).append({"id": m["id"], "nombre": m["nombre"], "tipo": m.get("tipo", ""), "url": m.get("url", "")})

            pre_por_curso: Dict[int, list] = {}
            for p in result_pre.data:
                pre_por_curso.setdefault(p["curso_id"], []).append(p["prerequisito_id"])

            est_por_curso: Dict[int, list] = {}
            for i in result_ins.data:
                est_por_curso.setdefault(i["curso_id"], []).append(i["estudiante_id"])

            datos["cursos"] = [{"id": c["id"], "nombre": c["nombre"], "descripcion": c.get("descripcion", ""), "nivel": c.get("nivel", ""), "materiales": mat_por_curso.get(c["id"], []), "estudiantes": est_por_curso.get(c["id"], []), "prerequisitos": pre_por_curso.get(c["id"], [])} for c in result_cursos.data]

            result_elim = self.__cliente.table("cursos").select("*").eq("eliminado", True).execute()
            result_mat_elim = self.__cliente.table("materiales").select("*").eq("eliminado", True).execute()

            mat_elim_por_curso: Dict[int, list] = {}
            for m in result_mat_elim.data:
                cid = m.get("curso_id")
                if cid is not None:
                    mat_elim_por_curso.setdefault(cid, []).append({"id": m["id"], "nombre": m["nombre"], "tipo": m.get("tipo", ""), "url": m.get("url", "")})

            datos["cursos_eliminados"] = [{"id": c["id"], "nombre": c["nombre"], "descripcion": c.get("descripcion", ""), "nivel": c.get("nivel", ""), "materiales": mat_elim_por_curso.get(c["id"], []), "estudiantes": [], "prerequisitos": pre_por_curso.get(c["id"], [])} for c in result_elim.data]

            datos["materiales_eliminados"] = [{"id": m["id"], "nombre": m["nombre"], "tipo": m.get("tipo", ""), "url": m.get("url", "")} for m in result_mat_elim.data if m.get("curso_id") is None]

            result_pre_elim = self.__cliente.table("prerequisitos").select("*").eq("eliminado", True).execute()
            pre_elim: Dict[str, list] = {}
            for p in result_pre_elim.data:
                key = str(p["curso_id"])
                pre_elim.setdefault(key, []).append(p["prerequisito_id"])
            datos["prerequisitos_eliminados"] = pre_elim

            return datos
        except Exception as e:
            print(f"[RepositorioSupabase] ❌ Error cargando desde la nube: {e}")
            self.__disponible = False # Marcamos como caído
            return None


class RepositorioHibrido(RepositorioDatos):
    """
    Persistencia dual: Local-First con Sincronización Inteligente.
    """

    def __init__(self) -> None:
        self.__repo_json = RepositorioJSON()
        self.__repo_supabase = RepositorioSupabase()

    def esta_disponible(self) -> bool:
        return self.__repo_json.esta_disponible() or self.__repo_supabase.esta_disponible()

    def guardar_todo(self, datos: Dict[str, Any]) -> bool:
        datos["last_updated"] = datetime.now().isoformat()
        
        exito_json = self.__repo_json.guardar_todo(datos)
        exito_supa = self.__repo_supabase.guardar_todo(datos) # Aquí adentro intenta reconectar si se había caído
        return exito_json or exito_supa

    def cargar_todo(self) -> Optional[Dict[str, Any]]:
        datos_json = self.__repo_json.cargar_todo()
        datos_supa = None
        
        if self.__repo_supabase.esta_disponible():
            datos_supa = self.__repo_supabase.cargar_todo()

        if not datos_json and not datos_supa:
            return None
        
        if datos_json and not datos_supa:
            return datos_json
            
        if datos_supa and not datos_json:
            self.__repo_json.guardar_todo(datos_supa)
            return datos_supa

        # Conflicto: El más reciente gana
        time_json = datos_json.get("last_updated", "1970-01-01T00:00:00")
        time_supa = datos_supa.get("last_updated", "1970-01-01T00:00:00")

        if time_json >= time_supa:
            print("[RepositorioHibrido] 🔄 Datos locales más recientes. Sincronizando hacia Supabase...")
            self.__repo_supabase.guardar_todo(datos_json)
            return datos_json
        else:
            print("[RepositorioHibrido] ☁️ Datos de nube más recientes. Sincronizando hacia local...")
            self.__repo_json.guardar_todo(datos_supa)
            return datos_supa


def crear_repositorio(modo: Optional[str] = None) -> RepositorioDatos:
    modo = modo or MODO_ALMACENAMIENTO
    if modo == "supabase":
        return RepositorioSupabase()
    elif modo == "json":
        return RepositorioJSON()
    else:
        return RepositorioHibrido()
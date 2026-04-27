"""
Lógica de negocio del sistema E-Learning.
Con Protección de Datos de Ejemplo y Sincronización Offline/Online.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime

from config import DATA_FOLDER, JSON_FILENAME, CAPACIDAD_MAXIMA_CURSO
from estructuras_datos import Pila, Cola, ArbolBusqueda, Grafo
from entidades import Curso, Estudiante, Material
from repositorio import crear_repositorio, RepositorioDatos

import os
import json


class ProteccionDatosEjemplo:
    """
    Responsabilidad Única (SRP): Garantizar que los datos base de ejemplo
    siempre existan en el sistema. Si el usuario los elimina, se regeneran.
    """
    DATOS_EJEMPLO = {
        "estudiantes": [
            {"id": 1, "nombre": "Ana Gómez", "email": "ana@example.com", "cursos": []},
            {"id": 2, "nombre": "Carlos López", "email": "carlos@example.com", "cursos": []},
            {"id": 3, "nombre": "María Pérez", "email": "maria@example.com", "cursos": []}
        ],
        "cursos": [
            {"id": 101, "nombre": "Python Básico", "descripcion": "Introducción a Python", "nivel": "Básico", "materiales": [], "estudiantes": [], "prerequisitos": []},
            {"id": 102, "nombre": "Python Intermedio", "descripcion": "Conceptos avanzados de Python", "nivel": "Intermedio", "materiales": [], "estudiantes": [], "prerequisitos": [101]},
            {"id": 103, "nombre": "Python Avanzado", "descripcion": "Programación avanzada con Python", "nivel": "Avanzado", "materiales": [], "estudiantes": [], "prerequisitos": [102]},
            {"id": 201, "nombre": "Bases de Datos Básico", "descripcion": "Introducción a las bases de datos", "nivel": "Básico", "materiales": [], "estudiantes": [], "prerequisitos": []},
            {"id": 202, "nombre": "Bases de Datos Avanzado", "descripcion": "Diseño avanzado de bases de datos", "nivel": "Avanzado", "materiales": [], "estudiantes": [], "prerequisitos": [201]},
            {"id": 301, "nombre": "Web Development", "descripcion": "Desarrollo web completo", "nivel": "Avanzado", "materiales": [], "estudiantes": [], "prerequisitos": [102, 201]}
        ],
        "cursos_eliminados": [],
        "materiales_eliminados": [],
        "prerequisitos_eliminados": {}
    }

    @staticmethod
    def obtener_datos() -> Dict[str, Any]:
        datos = ProteccionDatosEjemplo.DATOS_EJEMPLO.copy()
        datos["last_updated"] = "1970-01-01T00:00:00" # Para que no pise datos reales al inicio
        return datos

    @staticmethod
    def restaurar_si_faltan(sistema: "SistemaELearning") -> bool:
        cambio = False
        datos = ProteccionDatosEjemplo.DATOS_EJEMPLO

        for est_data in datos["estudiantes"]:
            if est_data["id"] not in sistema._estudiantes:
                sistema._estudiantes[est_data["id"]] = Estudiante.from_dict(est_data)
                cambio = True

        for cur_data in datos["cursos"]:
            cid = cur_data["id"]
            if cid not in sistema._cursos:
                if cid in sistema._cursos_eliminados:
                    curso = sistema._cursos_eliminados.pop(cid)
                else:
                    curso = Curso.from_dict(cur_data)
                
                sistema._cursos[cid] = curso
                sistema._grafo_cursos.agregar_vertice(cid, curso)
                clave = f"{curso.nombre.lower()}_{curso.nivel}"
                sistema._arbol_cursos.insertar(clave, curso)
                sistema._lista_espera[cid] = Cola()
                cambio = True

        for cur_data in datos["cursos"]:
            cid = cur_data["id"]
            if cid in sistema._cursos:
                curso = sistema._cursos[cid]
                for pre_id in cur_data.get("prerequisitos", []):
                    if pre_id not in curso.prerequisitos:
                        curso.agregar_prerequisito(pre_id)
                        sistema._grafo_cursos.agregar_arista(cid, pre_id)
                        cambio = True

        return cambio


class SistemaELearning:
    def __init__(self, modo_almacenamiento: Optional[str] = None) -> None:
        self._estudiantes: Dict[int, Estudiante] = {}
        self._cursos: Dict[int, Curso] = {}
        self._cursos_eliminados: Dict[int, Curso] = {}
        self._materiales_eliminados: Dict[int, Material] = {}
        self._prerequisitos_eliminados: Dict[str, List[int]] = {}

        self._historial_cambios: Pila = Pila()
        self._lista_espera: Dict[int, Cola] = {}
        self._arbol_cursos: ArbolBusqueda = ArbolBusqueda()
        self._grafo_cursos: Grafo = Grafo()

        self.__repositorio: RepositorioDatos = crear_repositorio(modo_almacenamiento)
        
        # Bandera para evitar múltiples guardados durante la carga inicial
        self._cargando_datos = True 
        self._cargar_datos()
        self._cargando_datos = False

    @property
    def estudiantes(self) -> Dict[int, Estudiante]:
        return self._estudiantes

    @property
    def cursos(self) -> Dict[int, Curso]:
        return self._cursos

    @property
    def cursos_eliminados(self) -> Dict[int, Curso]:
        return self._cursos_eliminados

    @property
    def materiales_eliminados(self) -> Dict[int, Material]:
        return self._materiales_eliminados

    @property
    def prerequisitos_eliminados(self) -> Dict[str, List[int]]:
        return self._prerequisitos_eliminados

    def _serializar_estado(self) -> Dict[str, Any]:
        """
        Serializa el estado. Ya no ponemos el timestamp aquí porque 
        el RepositorioHibrido.guardar_todo() lo inyecta automáticamente 
        con la hora exacta de la modificación.
        """
        return {
            "estudiantes": [e.to_dict() for e in self._estudiantes.values()],
            "cursos": [c.to_dict() for c in self._cursos.values()],
            "cursos_eliminados": [c.to_dict() for c in self._cursos_eliminados.values()],
            "materiales_eliminados": [m.to_dict() for m in self._materiales_eliminados.values()],
            "prerequisitos_eliminados": dict(self._prerequisitos_eliminados),
        }

    def _guardar(self) -> None:
        """Solo guarda si no está en proceso de carga inicial."""
        if self._cargando_datos:
            return
        datos = self._serializar_estado()
        self.__repositorio.guardar_todo(datos)

    def _cargar_datos(self) -> None:
        datos = self.__repositorio.cargar_todo()
        if datos is not None:
            self._cargar_desde_diccionario(datos)
        else:
            print("[Sistema] No se encontraron datos, creando datos de ejemplo...")
            self._cargar_desde_diccionario(ProteccionDatosEjemplo.obtener_datos())
        
        # Verificar y restaurar datos de ejemplo si faltan
        if ProteccionDatosEjemplo.restaurar_si_faltan(self):
            print("[Sistema] Datos de ejemplo restaurados porque faltaban.")
            datos = self._serializar_estado()
            self.__repositorio.guardar_todo(datos)

    def _cargar_desde_diccionario(self, datos: Dict[str, Any]) -> None:
        self._estudiantes.clear()
        self._cursos.clear()
        self._grafo_cursos = Grafo()
        self._arbol_cursos = ArbolBusqueda()
        self._lista_espera.clear()

        for est_data in datos.get("estudiantes", []):
            estudiante = Estudiante.from_dict(est_data)
            self._estudiantes[estudiante.id] = estudiante

        for cur_data in datos.get("cursos", []):
            curso = Curso.from_dict(cur_data)
            self._cursos[curso.id] = curso
            self._grafo_cursos.agregar_vertice(curso.id, curso)
            clave = f"{curso.nombre.lower()}_{curso.nivel}"
            self._arbol_cursos.insertar(clave, curso)
            self._lista_espera[curso.id] = Cola()

        for cur_data in datos.get("cursos", []):
            curso_id = cur_data["id"]
            for prereq_id in cur_data.get("prerequisitos", []):
                if prereq_id in self._cursos:
                    self._grafo_cursos.agregar_arista(curso_id, prereq_id)

        for cur_data in datos.get("cursos", []):
            curso_id = cur_data["id"]
            if curso_id in self._cursos:
                curso = self._cursos[curso_id]
                for est_id in cur_data.get("estudiantes", []):
                    if est_id in self._estudiantes:
                        estudiante = self._estudiantes[est_id]
                        estudiante.agregar_curso(curso)
                        curso.agregar_estudiante(estudiante)

        for cur_data in datos.get("cursos_eliminados", []):
            curso = Curso.from_dict(cur_data)
            self._cursos_eliminados[curso.id] = curso

        for mat_data in datos.get("materiales_eliminados", []):
            material = Material.from_dict(mat_data)
            self._materiales_eliminados[material.id] = material

        self._prerequisitos_eliminados = datos.get("prerequisitos_eliminados", {})
        print(f"[Sistema] Datos cargados: {len(self._estudiantes)} estudiantes, {len(self._cursos)} cursos.")

    # ══════════════════════════════════════════════════════════════════
    #  CRUD Estudiantes
    # ══════════════════════════════════════════════════════════════════

    def registrar_estudiante(self, id: int, nombre: str, email: str) -> Optional[Estudiante]:
        if id not in self._estudiantes:
            nuevo = Estudiante(id, nombre, email)
            self._estudiantes[id] = nuevo
            self._guardar()
            return nuevo
        return None

    def eliminar_estudiante(self, estudiante_id: int) -> bool:
        if estudiante_id in self._estudiantes:
            estudiante = self._estudiantes.pop(estudiante_id)
            for curso in self._cursos.values():
                if estudiante in curso.estudiantes:
                    curso.remover_estudiante(estudiante)
            self._guardar()
            return True
        return False

    # ══════════════════════════════════════════════════════════════════
    #  CRUD Cursos
    # ══════════════════════════════════════════════════════════════════

    def crear_curso(self, id: int, nombre: str, descripcion: str, nivel: str) -> Optional[Curso]:
        if id not in self._cursos:
            nuevo = Curso(id, nombre, descripcion, nivel)
            self._cursos[id] = nuevo
            self._grafo_cursos.agregar_vertice(id, nuevo)
            clave = f"{nombre.lower()}_{nivel}"
            self._arbol_cursos.insertar(clave, nuevo)
            self._lista_espera[id] = Cola()
            self._guardar()
            return nuevo
        return None

    def eliminar_curso(self, curso_id: int) -> bool:
        if curso_id in self._cursos:
            curso = self._cursos.pop(curso_id)
            self._cursos_eliminados[curso_id] = curso
            for c in self._cursos.values():
                if curso_id in c.prerequisitos:
                    c.remover_prerequisito(curso_id)
            self._grafo_cursos.eliminar_vertice(curso_id)
            self._guardar()
            return True
        return False

    def restaurar_curso(self, curso_id: int) -> bool:
        if curso_id in self._cursos_eliminados:
            curso = self._cursos_eliminados.pop(curso_id)
            self._cursos[curso_id] = curso
            self._grafo_cursos.agregar_vertice(curso_id, curso)
            clave = f"{curso.nombre.lower()}_{curso.nivel}"
            self._arbol_cursos.insertar(clave, curso)
            self._lista_espera[curso_id] = Cola()
            for prereq_id in curso.prerequisitos:
                if prereq_id in self._cursos:
                    self._grafo_cursos.agregar_arista(curso_id, prereq_id)
            self._guardar()
            return True
        return False

    # ══════════════════════════════════════════════════════════════════
    #  Materiales
    # ══════════════════════════════════════════════════════════════════

    def agregar_material(self, curso_id: int, material: Material) -> bool:
        if curso_id in self._cursos:
            self._cursos[curso_id].agregar_material(material)
            self._guardar()
            return True
        return False

    def eliminar_material(self, curso_id: int, material_id: int) -> bool:
        if curso_id in self._cursos:
            curso = self._cursos[curso_id]
            for material in curso.materiales:
                if material.id == material_id:
                    curso.remover_material(material)
                    self._materiales_eliminados[material_id] = material
                    self._guardar()
                    return True
        return False

    def restaurar_material(self, material_id: int) -> bool:
        if material_id in self._materiales_eliminados:
            self._materiales_eliminados.pop(material_id)
            self._guardar()
            return True
        return False

    # ══════════════════════════════════════════════════════════════════
    #  Prerequisitos
    # ══════════════════════════════════════════════════════════════════

    def establecer_prerequisito(self, curso_id: int, prerequisito_id: int) -> bool:
        if curso_id in self._cursos and prerequisito_id in self._cursos:
            if curso_id == prerequisito_id:
                return False
            if prerequisito_id in self._cursos[curso_id].prerequisitos:
                return False
            self._cursos[curso_id].agregar_prerequisito(prerequisito_id)
            self._grafo_cursos.agregar_arista(curso_id, prerequisito_id)
            self._guardar()
            return True
        return False

    def eliminar_prerequisito(self, curso_id: int, prerequisito_id: int) -> bool:
        if curso_id in self._cursos and prerequisito_id in self._cursos[curso_id].prerequisitos:
            self._cursos[curso_id].remover_prerequisito(prerequisito_id)
            self._grafo_cursos.eliminar_arista(curso_id, prerequisito_id)
            self._guardar()
            return True
        return False

    # ══════════════════════════════════════════════════════════════════
    #  Inscripciones
    # ══════════════════════════════════════════════════════════════════

    def inscribir_estudiante(self, estudiante_id: int, curso_id: int, capacidad_maxima: int = CAPACIDAD_MAXIMA_CURSO) -> Any:
        if estudiante_id not in self._estudiantes or curso_id not in self._cursos:
            return False

        estudiante = self._estudiantes[estudiante_id]
        curso = self._cursos[curso_id]

        if curso in estudiante.cursos:
            return "ya_inscrito"

        cursos_completados_ids = estudiante.obtener_ids_cursos()
        if not self._grafo_cursos.verificar_cumple_prerequisitos(cursos_completados_ids, curso_id):
            return "prerequisitos_faltantes"

        if len(curso.estudiantes) < capacidad_maxima:
            estudiante.agregar_curso(curso)
            curso.agregar_estudiante(estudiante)
            self._historial_cambios.apilar({"tipo": "inscripcion", "estudiante_id": estudiante_id, "curso_id": curso_id})
            self._guardar()
            return True
        else:
            self._lista_espera[curso_id].encolar(estudiante)
            return "lista_espera"

    def cancelar_inscripcion(self, estudiante_id: int, curso_id: int) -> bool:
        if estudiante_id not in self._estudiantes or curso_id not in self._cursos:
            return False

        estudiante = self._estudiantes[estudiante_id]
        curso = self._cursos[curso_id]

        if curso in estudiante.cursos:
            estudiante.remover_curso(curso)
            curso.remover_estudiante(estudiante)
            self._historial_cambios.apilar({"tipo": "cancelacion", "estudiante_id": estudiante_id, "curso_id": curso_id})
            self._guardar()
            if not self._lista_espera[curso_id].esta_vacia():
                estudiante_espera = self._lista_espera[curso_id].desencolar()
                if estudiante_espera and estudiante_espera.id in self._estudiantes:
                    self.inscribir_estudiante(estudiante_espera.id, curso_id)
            return True
        return False

    def deshacer_ultima_accion(self) -> bool:
        if self._historial_cambios.esta_vacia():
            return False

        accion = self._historial_cambios.desapilar()
        est_id = accion["estudiante_id"]
        cur_id = accion["curso_id"]

        if est_id not in self._estudiantes or cur_id not in self._cursos:
            return False

        estudiante = self._estudiantes[est_id]
        curso = self._cursos[cur_id]

        if accion["tipo"] == "inscripcion":
            estudiante.remover_curso(curso)
            curso.remover_estudiante(estudiante)
        elif accion["tipo"] == "cancelacion":
            estudiante.agregar_curso(curso)
            curso.agregar_estudiante(estudiante)

        self._guardar()
        return True

    # ══════════════════════════════════════════════════════════════════
    #  Búsquedas
    # ══════════════════════════════════════════════════════════════════

    def buscar_cursos(self, tema: str, nivel: str = "Todos") -> List[Curso]:
        return self._arbol_cursos.buscar_por_tema_nivel(tema, nivel)

    def recomendar_cursos(self, curso_objetivo_id: int) -> List[Curso]:
        return self._grafo_cursos.recomendar_ruta_aprendizaje(curso_objetivo_id)

    # ══════════════════════════════════════════════════════════════════
    #  Persistencia manual
    # ══════════════════════════════════════════════════════════════════

    def guardar(self) -> None:
        datos = self._serializar_estado()
        self.__repositorio.guardar_todo(datos)
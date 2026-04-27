"""
Entidades del dominio E-Learning: Estudiante, Curso, Material.

PILARES POO IMPLEMENTADOS:
  • ABSTRACCIÓN:    Entidad (ABC) define contrato to_dict/from_dict/obtener_resumen
  • HERENCIA:       Estudiante, Curso, Material heredan de Entidad
  • POLIMORFISMO:   cada subclase implementa to_dict/from_dict/obtener_resumen diferente
  • ENCAPSULAMIENTO: atributos privados (__), acceso mediante @property y métodos
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class Entidad(ABC):
    """
    Clase abstracta base para todas las entidades del sistema.
    ABSTRACCIÓN: define el contrato que toda entidad debe cumplir.
    POLIMORFISMO: cada subclase implementa sus propios métodos abstractos.
    """

    @property
    @abstractmethod
    def id(self) -> Any:
        """Identificador único de la entidad."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serializa la entidad a diccionario para persistencia."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Entidad":
        """Deserializa la entidad desde un diccionario."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Retorna un resumen legible de la entidad."""
        pass

    def __str__(self) -> str:
        return self.obtener_resumen()


# ══════════════════════════════════════════════════════════════════════
#  Estudiante
# ══════════════════════════════════════════════════════════════════════

class Estudiante(Entidad):
    """
    Representa un estudiante con sus datos y cursos inscritos.
    HERENCIA: extiende Entidad.
    ENCAPSULAMIENTO: atributos privados, acceso mediante properties.
    POLIMORFISMO: implementación propia de to_dict/from_dict/obtener_resumen.
    """

    def __init__(self, id: int, nombre: str, email: str) -> None:
        self.__id = id
        self.__nombre = nombre
        self.__email = email
        self.__cursos: List[Any] = []  # Lista de Curso

    # ── Properties (Encapsulamiento: lectura controlada) ─────────────
    @property
    def id(self) -> int:
        return self.__id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str) -> None:
        self.__email = valor.strip() if valor else ""

    @property
    def cursos(self) -> List[Any]:
        """Retorna referencia directa para iteración (solo lectura externa)."""
        return self.__cursos

    # ── Métodos de modificación (Encapsulamiento: escritura controlada) ─
    def agregar_curso(self, curso: Any) -> None:
        if curso not in self.__cursos:
            self.__cursos.append(curso)

    def remover_curso(self, curso: Any) -> None:
        if curso in self.__cursos:
            self.__cursos.remove(curso)

    def obtener_ids_cursos(self) -> List[int]:
        return [c.id for c in self.__cursos]

    def limpiar_cursos(self) -> None:
        self.__cursos.clear()

    # ── Polimorfismo: implementación específica ──────────────────────
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "email": self.__email,
            "cursos": self.obtener_ids_cursos(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Estudiante":
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            email=data.get("email", ""),
        )

    def obtener_resumen(self) -> str:
        return f"Estudiante: {self.__nombre} ({self.__email})"


# ══════════════════════════════════════════════════════════════════════
#  Material
# ══════════════════════════════════════════════════════════════════════

class Material(Entidad):
    """
    Representa un material educativo asociado a un curso.
    HERENCIA: extiende Entidad.
    ENCAPSULAMIENTO: atributos privados con properties.
    POLIMORFISMO: implementación propia de to_dict/from_dict/obtener_resumen.
    """

    def __init__(self, id: int, nombre: str, tipo: str, url: str) -> None:
        self.__id = id
        self.__nombre = nombre
        self.__tipo = tipo
        self.__url = url

    @property
    def id(self) -> int:
        return self.__id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = valor

    @property
    def tipo(self) -> str:
        return self.__tipo

    @tipo.setter
    def tipo(self, valor: str) -> None:
        self.__tipo = valor

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, valor: str) -> None:
        self.__url = valor

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "tipo": self.__tipo,
            "url": self.__url,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Material":
        return cls(
            id=data["id"],
            nombre=data["nombre"],
            tipo=data.get("tipo", ""),
            url=data.get("url", ""),
        )

    def obtener_resumen(self) -> str:
        return f"Material: {self.__nombre} ({self.__tipo})"


# ══════════════════════════════════════════════════════════════════════
#  Curso
# ══════════════════════════════════════════════════════════════════════

class Curso(Entidad):
    """
    Representa un curso con sus atributos, materiales y prerequisitos.
    HERENCIA: extiende Entidad.
    ENCAPSULAMIENTO: atributos privados, modificaciones mediante métodos.
    POLIMORFISMO: implementación propia de to_dict/from_dict/obtener_resumen.
    """

    def __init__(self, id: int, nombre: str, descripcion: str, nivel: str) -> None:
        self.__id = id
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__nivel = nivel
        self.__materiales: List[Material] = []
        self.__estudiantes: List[Estudiante] = []
        self.__prerequisitos: List[int] = []

    # ── Properties (Encapsulamiento) ─────────────────────────────────
    @property
    def id(self) -> int:
        return self.__id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = valor

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self.__descripcion = valor

    @property
    def nivel(self) -> str:
        return self.__nivel

    @nivel.setter
    def nivel(self, valor: str) -> None:
        self.__nivel = valor

    @property
    def materiales(self) -> List[Material]:
        return self.__materiales

    @property
    def estudiantes(self) -> List[Estudiante]:
        return self.__estudiantes

    @property
    def prerequisitos(self) -> List[int]:
        return self.__prerequisitos

    # ── Métodos de modificación (Encapsulamiento: escritura controlada) ─
    def agregar_material(self, material: Material) -> None:
        self.__materiales.append(material)

    def remover_material(self, material: Material) -> None:
        if material in self.__materiales:
            self.__materiales.remove(material)

    def agregar_estudiante(self, estudiante: Estudiante) -> None:
        if estudiante not in self.__estudiantes:
            self.__estudiantes.append(estudiante)

    def remover_estudiante(self, estudiante: Estudiante) -> None:
        if estudiante in self.__estudiantes:
            self.__estudiantes.remove(estudiante)

    def agregar_prerequisito(self, prerequisito_id: int) -> None:
        if prerequisito_id not in self.__prerequisitos:
            self.__prerequisitos.append(prerequisito_id)

    def remover_prerequisito(self, prerequisito_id: int) -> None:
        if prerequisito_id in self.__prerequisitos:
            self.__prerequisitos.remove(prerequisito_id)

    def obtener_ids_estudiantes(self) -> List[int]:
        return [e.id for e in self.__estudiantes]

    # ── Polimorfismo: implementación específica ──────────────────────
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "descripcion": self.__descripcion,
            "nivel": self.__nivel,
            "materiales": [m.to_dict() for m in self.__materiales],
            "estudiantes": self.obtener_ids_estudiantes(),
            "prerequisitos": list(self.__prerequisitos),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Curso":
        curso = cls(
            id=data["id"],
            nombre=data["nombre"],
            descripcion=data.get("descripcion", ""),
            nivel=data.get("nivel", ""),
        )
        for m_data in data.get("materiales", []):
            curso.agregar_material(Material.from_dict(m_data))
        for pre_id in data.get("prerequisitos", []):
            curso.agregar_prerequisito(pre_id)
        return curso

    def obtener_resumen(self) -> str:
        return f"Curso: {self.__nombre} (Nivel: {self.__nivel})"
    
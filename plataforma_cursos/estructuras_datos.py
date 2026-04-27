"""
Estructuras de datos personalizadas para el sistema E-Learning.

PILARES POO IMPLEMENTADOS:
  • ABSTRACCIÓN:   EstructuraLineal, EstructuraBusqueda, EstructuraRelacion (ABC)
  • HERENCIA:      Pila/Cola heredan de EstructuraLineal; ArbolBusqueda de EstructuraBusqueda;
                   Grafo de EstructuraRelacion
  • POLIMORFISMO:  agregar(), extraer(), ver_proximo() se comportan distinto en Pila vs Cola;
                   insertar()/buscar() específicos por estructura
  • ENCAPSULAMIENTO: atributos protegidos/privados, acceso mediante properties y métodos
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic

T = TypeVar("T")


# ══════════════════════════════════════════════════════════════════════
#  ABSTRACCIÓN → Clase abstracta base para estructuras lineales
#  HERENCIA   → Pila y Cola heredan de EstructuraLineal
#  POLIMORFISMO→ agregar/extraer/ver_proximo varían según la subclase
# ══════════════════════════════════════════════════════════════════════

class EstructuraLineal(ABC, Generic[T]):
    """
    Clase abstracta que define el contrato para estructuras de datos lineales.
    ABSTRACCIÓN: oculta detalles de implementación, expone solo la interfaz.
    ENCAPSULAMIENTO: _items es protegido, se accede mediante property.
    """

    def __init__(self) -> None:
        self._items: List[T] = []

    # ── Encapsulamiento: acceso de solo lectura ──────────────────────
    @property
    def items(self) -> List[T]:
        """Retorna copia para proteger la estructura interna."""
        return self._items.copy()

    # ── Polimorfismo: cada subclase implementa su propia lógica ──────
    @abstractmethod
    def agregar(self, item: T) -> None:
        """Agrega un elemento (LIFO en Pila, FIFO en Cola)."""
        pass

    @abstractmethod
    def extraer(self) -> Optional[T]:
        """Extrae y retorna el elemento correspondiente."""
        pass

    @abstractmethod
    def ver_proximo(self) -> Optional[T]:
        """Retorna el próximo elemento a extraer sin removerlo."""
        pass

    # ── Métodos concretos heredados por todas las subclases ──────────
    def esta_vacia(self) -> bool:
        return len(self._items) == 0

    def tamaño(self) -> int:
        return len(self._items)

    def limpiar(self) -> None:
        self._items.clear()


class Pila(EstructuraLineal[T]):
    """
    Estructura LIFO (Last In, First Out).
    HERENCIA: extiende EstructuraLineal.
    POLIMORFISMO: agregar/extraer/ver_proximo con semántica LIFO.
    """

    def agregar(self, item: T) -> None:
        self.apilar(item)

    def extraer(self) -> Optional[T]:
        return self.desapilar()

    def ver_proximo(self) -> Optional[T]:
        return self.ver_tope()

    # ── Métodos específicos de Pila ──────────────────────────────────
    def apilar(self, item: T) -> None:
        self._items.append(item)

    def desapilar(self) -> Optional[T]:
        if not self.esta_vacia():
            return self._items.pop()
        return None

    def ver_tope(self) -> Optional[T]:
        if not self.esta_vacia():
            return self._items[-1]
        return None


class Cola(EstructuraLineal[T]):
    """
    Estructura FIFO (First In, First Out).
    HERENCIA: extiende EstructuraLineal.
    POLIMORFISMO: agregar/extraer/ver_proximo con semántica FIFO.
    """

    def agregar(self, item: T) -> None:
        self.encolar(item)

    def extraer(self) -> Optional[T]:
        return self.desencolar()

    def ver_proximo(self) -> Optional[T]:
        return self.ver_frente()

    # ── Métodos específicos de Cola ──────────────────────────────────
    def encolar(self, item: T) -> None:
        self._items.insert(0, item)

    def desencolar(self) -> Optional[T]:
        if not self.esta_vacia():
            return self._items.pop()
        return None

    def ver_frente(self) -> Optional[T]:
        if not self.esta_vacia():
            return self._items[-1]
        return None


# ══════════════════════════════════════════════════════════════════════
#  Nodo y Árbol Binario de Búsqueda
# ══════════════════════════════════════════════════════════════════════

class NodoArbol:
    """
    Nodo para árbol binario de búsqueda.
    ENCAPSULAMIENTO: atributos protegidos con properties de acceso.
    """

    def __init__(self, clave: str, valor: Any) -> None:
        self._clave = clave
        self._valor = valor
        self._izquierdo: Optional["NodoArbol"] = None
        self._derecho: Optional["NodoArbol"] = None

    @property
    def clave(self) -> str:
        return self._clave

    @property
    def valor(self) -> Any:
        return self._valor

    @property
    def izquierdo(self) -> Optional["NodoArbol"]:
        return self._izquierdo

    @izquierdo.setter
    def izquierdo(self, nodo: Optional["NodoArbol"]) -> None:
        self._izquierdo = nodo

    @property
    def derecho(self) -> Optional["NodoArbol"]:
        return self._derecho

    @derecho.setter
    def derecho(self, nodo: Optional["NodoArbol"]) -> None:
        self._derecho = nodo


class EstructuraBusqueda(ABC):
    """
    ABSTRACCIÓN: interfaz para estructuras de búsqueda.
    POLIMORFISMO: cada subclase define su propia lógica de insertar/buscar.
    """

    @abstractmethod
    def insertar(self, clave: str, valor: Any) -> None:
        pass

    @abstractmethod
    def buscar(self, criterio: Any) -> List[Any]:
        pass


class ArbolBusqueda(EstructuraBusqueda):
    """
    Árbol binario de búsqueda para cursos.
    HERENCIA: extiende EstructuraBusqueda.
    POLIMORFISMO: implementa insertar/buscar de forma específica.
    ENCAPSULAMIENTO: raiz privada, acceso por property.
    """

    def __init__(self) -> None:
        self.__raiz: Optional[NodoArbol] = None

    @property
    def raiz(self) -> Optional[NodoArbol]:
        return self.__raiz

    def insertar(self, clave: str, valor: Any) -> None:
        if not self.__raiz:
            self.__raiz = NodoArbol(clave, valor)
        else:
            self._insertar_recursivo(self.__raiz, clave, valor)

    def _insertar_recursivo(self, nodo: NodoArbol, clave: str, valor: Any) -> None:
        if clave < nodo.clave:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoArbol(clave, valor)
            else:
                self._insertar_recursivo(nodo.izquierdo, clave, valor)
        else:
            if nodo.derecho is None:
                nodo.derecho = NodoArbol(clave, valor)
            else:
                self._insertar_recursivo(nodo.derecho, clave, valor)

    def buscar(self, criterio: Any) -> List[Any]:
        """
        POLIMORFISMO: acepta dict con tema/nivel o string simple.
        """
        if isinstance(criterio, dict):
            tema = criterio.get("tema", "")
            nivel = criterio.get("nivel", "Todos")
            return self.buscar_por_tema_nivel(tema, nivel)
        return []

    def buscar_por_tema_nivel(self, tema: str, nivel: str) -> List[Any]:
        resultados: List[Any] = []
        self._buscar_tema_nivel_recursivo(self.__raiz, tema, nivel, resultados)
        return resultados

    def _buscar_tema_nivel_recursivo(
        self, nodo: Optional[NodoArbol], tema: str, nivel: str, resultados: List[Any]
    ) -> None:
        if nodo is None:
            return
        curso = nodo.valor
        if tema.lower() in curso.nombre.lower() and (
            nivel == "Todos" or curso.nivel == nivel
        ):
            resultados.append(curso)
        self._buscar_tema_nivel_recursivo(nodo.izquierdo, tema, nivel, resultados)
        self._buscar_tema_nivel_recursivo(nodo.derecho, tema, nivel, resultados)


# ══════════════════════════════════════════════════════════════════════
#  Grafo Dirigido para Prerequisitos
# ══════════════════════════════════════════════════════════════════════

class EstructuraRelacion(ABC):
    """
    ABSTRACCIÓN: interfaz para estructuras que modelan relaciones entre entidades.
    POLIMORFISMO: cada subclase define su lógica de vértices/aristas.
    """

    @abstractmethod
    def agregar_vertice(self, id_vertice: Any, valor: Any = None) -> None:
        pass

    @abstractmethod
    def agregar_arista(self, origen: Any, destino: Any) -> None:
        pass


class Grafo(EstructuraRelacion):
    """
    Grafo dirigido para modelar prerequisitos entre cursos.
    HERENCIA: extiende EstructuraRelacion.
    ENCAPSULAMIENTO: vertices y aristas protegidos con properties de solo lectura.
    """

    def __init__(self) -> None:
        self._vertices: Dict[Any, Any] = {}
        self._aristas: Dict[Any, List[Any]] = {}

    @property
    def vertices(self) -> Dict[Any, Any]:
        return self._vertices.copy()

    @property
    def aristas(self) -> Dict[Any, List[Any]]:
        return {k: v.copy() for k, v in self._aristas.items()}

    def agregar_vertice(self, id_vertice: Any, valor: Any = None) -> None:
        self._vertices[id_vertice] = valor
        if id_vertice not in self._aristas:
            self._aristas[id_vertice] = []

    def agregar_arista(self, origen: Any, destino: Any) -> None:
        if origen in self._aristas and destino in self._vertices:
            if destino not in self._aristas[origen]:
                self._aristas[origen].append(destino)

    def eliminar_vertice(self, id_vertice: Any) -> None:
        if id_vertice in self._vertices:
            del self._vertices[id_vertice]
        if id_vertice in self._aristas:
            del self._aristas[id_vertice]
        for key in list(self._aristas.keys()):
            if id_vertice in self._aristas[key]:
                self._aristas[key].remove(id_vertice)

    def eliminar_arista(self, origen: Any, destino: Any) -> None:
        if origen in self._aristas and destino in self._aristas[origen]:
            self._aristas[origen].remove(destino)

    def obtener_aristas_vertice(self, id_vertice: Any) -> List[Any]:
        return self._aristas.get(id_vertice, []).copy()

    def tiene_vertice(self, id_vertice: Any) -> bool:
        return id_vertice in self._vertices

    def verificar_cumple_prerequisitos(
        self, cursos_completados_ids: set, curso_id: Any
    ) -> bool:
        prerequisitos_necesarios = self._aristas.get(curso_id, [])
        for prereq_id in prerequisitos_necesarios:
            if prereq_id not in cursos_completados_ids:
                return False
        return True

    def recomendar_ruta_aprendizaje(self, curso_objetivo_id: Any) -> List[Any]:
        if curso_objetivo_id not in self._vertices:
            return []

        def obtener_ruta(curso_id, visitados=None, ruta_actual=None):
            if visitados is None:
                visitados = set()
            if ruta_actual is None:
                ruta_actual = []

            if curso_id in visitados:
                return []

            visitados.add(curso_id)
            prerequisitos = self._aristas.get(curso_id, [])

            for prereq_id in prerequisitos:
                if prereq_id not in [c.id for c in ruta_actual]:
                    ruta_prereq = obtener_ruta(
                        prereq_id, visitados.copy(), ruta_actual.copy()
                    )
                    for curso in ruta_prereq:
                        if curso.id not in [c.id for c in ruta_actual]:
                            ruta_actual.append(curso)

            if curso_id not in [c.id for c in ruta_actual]:
                ruta_actual.append(self._vertices[curso_id])

            return ruta_actual

        return obtener_ruta(curso_objetivo_id)
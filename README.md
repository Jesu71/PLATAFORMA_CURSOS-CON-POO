# PLATAFORMA_CURSOS-CON-POO
App E-Learning con pilares poo, estructura de datos y patrones de software, desarrollada en python.

🎓 Sistema de Gestión E-Learning
Una aplicación de escritorio completa para gestionar cursos, estudiantes y materiales didácticos. Desarrollada en Python aplicando rigurosamente los 4 pilares de la Programación Orientada a Objetos (POO), implementando estructuras de datos personalizadas y contando con persistencia híbrida (Local + Supabase en la nube) con sincronización offline/online inteligente.

✨ Características Principales
🧑‍🎓 Gestión de Estudiantes: Registro, eliminación y visualización de cursos inscritos.
📚 Gestión de Cursos: Creación, eliminación, restauración y asignación de materiales.
🔗 Sistema de Prerequisitos: Configuración de dependencias entre cursos usando un Grafo dirigido.
📝 Inscripciones: Control de cupos, lista de espera automática (FIFO) y validación de prerequisitos.
🔍 Búsquedas Optimizadas: Búsqueda por tema y nivel utilizando un Árbol Binario de Búsqueda (ABB).
🛡️ Datos de Ejemplo Persistentes: Los datos base de demostración se regeneran automáticamente si se eliminan.
☁️ Sincronización Offline/Online: Arquitectura Local-First. La app funciona sin internet y sincroniza los cambios a Supabase automáticamente cuando se recupera la conexión.
↩️ Deshacer Acciones: Historial de inscripciones/cancelaciones usando una Pila (LIFO).
🏗️ Arquitectura y Pilares POO
El sistema está diseñado bajo estrictos principios de ingeniería de software:

Encapsulamiento: Atributos privados (__id, __nombre) en las entidades y acceso mediante @property. La lógica interna de las estructuras de datos y la conexión a BD están ocultas.
Abstracción: Clases abstractas como Entidad, EstructuraLineal y RepositorioDatos definen contratos claros, ocultando la complejidad interna al resto del sistema.
Herencia: Estudiante, Curso, Material heredan de Entidad; Pila y Cola heredan de EstructuraLineal; RepositorioJSON, RepositorioSupabase heredan de RepositorioDatos.
Polimorfismo: Métodos como to_dict(), obtener_resumen(), agregar() y guardar_todo() se comportan de manera distinta dependiendo de la instancia concreta que los invoque.
🧮 Estructuras de Datos Personalizadas
Pila (LIFO): Historial de acciones (Deshacer).
Cola (FIFO): Lista de espera de cursos.
Árbol Binario de Búsqueda: Búsquedas eficientes por tema/nivel.
Grafo Dirigido: Modelado de prerequisitos y rutas de aprendizaje.
🛠️ Tech Stack
Lenguaje: Python 3.10+
GUI: Tkinter / ttk
Base de Datos (Nube): Supabase (PostgreSQL)
Persistencia (Local): JSON
Empaquetado: PyInstaller
🚀 Instalación y Puesta en Marcha
Sigue estos pasos para ejecutar el proyecto en tu máquina local:

1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.gitcd TU_REPOSITORIO
2. Crear entorno virtual (Recomendado)
bash

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
3. Instalar dependencias
bash

pip install -r requirements.txt

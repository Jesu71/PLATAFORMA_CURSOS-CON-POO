"""
Interfaz gráfica del sistema E-Learning con Tkinter.
Mantiene la misma interfaz y funcionalidad del código original.
"""

import tkinter as tk
from tkinter import messagebox, ttk

from entidades import Material
from sistema import SistemaELearning


class SistemaELearningGUI:
    """Interfaz gráfica principal del sistema E-Learning."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Sistema de Gestión E-Learning")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.sistema = SistemaELearning()

        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#ccc", font=("Arial", 10))
        self.style.map("TButton", background=[("active", "#aaa")])

        self.menu_principal()
        self.root.protocol("WM_DELETE_WINDOW", self._salir)

    # ══════════════════════════════════════════════════════════════════
    #  Utilidades GUI
    # ══════════════════════════════════════════════════════════════════

    def _limpiar_ventana(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

    def _salir(self) -> None:
        self.sistema.guardar()
        self.root.destroy()

    # ══════════════════════════════════════════════════════════════════
    #  Menús de navegación
    # ══════════════════════════════════════════════════════════════════

    def menu_principal(self) -> None:
        self._limpiar_ventana()
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=20)

        tk.Label(frame, text="===== SISTEMA DE GESTIÓN E-LEARNING =====",
                 font=("Arial", 16), bg="#f0f0f0").pack(pady=10)

        ttk.Button(frame, text="Gestión de Estudiantes", command=self.menu_estudiantes, width=30).pack(pady=5)
        ttk.Button(frame, text="Gestión de Cursos", command=self.menu_cursos, width=30).pack(pady=5)
        ttk.Button(frame, text="Inscripciones", command=self.menu_inscripciones, width=30).pack(pady=5)
        ttk.Button(frame, text="Búsquedas", command=self.menu_busquedas, width=30).pack(pady=5)
        ttk.Button(frame, text="Salir", command=self._salir, width=30).pack(pady=5)

    def menu_estudiantes(self) -> None:
        self._limpiar_ventana()
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=20)

        tk.Label(frame, text="===== GESTIÓN DE ESTUDIANTES =====", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)

        ttk.Button(frame, text="Registrar nuevo estudiante", command=self.registrar_estudiante, width=30).pack(pady=5)
        ttk.Button(frame, text="Ver lista de estudiantes", command=self.ver_estudiantes, width=30).pack(pady=5)
        ttk.Button(frame, text="Eliminar estudiante", command=self.eliminar_estudiante, width=30).pack(pady=5)
        ttk.Button(frame, text="Ver cursos de un estudiante", command=self.ver_cursos_estudiante, width=30).pack(pady=5)
        ttk.Button(frame, text="Volver al menú principal", command=self.menu_principal, width=30).pack(pady=5)

    def menu_cursos(self) -> None:
        self._limpiar_ventana()
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=20)

        tk.Label(frame, text="===== GESTIÓN DE CURSOS =====", font=("Arial", 16), bg="#f0f0f0").pack(pady=5)

        ttk.Button(frame, text="Crear nuevo curso", command=self.crear_curso, width=30).pack(pady=3)
        ttk.Button(frame, text="Ver lista de cursos", command=self.ver_cursos, width=30).pack(pady=3)
        ttk.Button(frame, text="Agregar material a curso", command=self.agregar_material, width=30).pack(pady=3)
        ttk.Button(frame, text="Eliminar material de curso", command=self.eliminar_material, width=30).pack(pady=3)
        ttk.Button(frame, text="Establecer prerequisito", command=self.establecer_prerequisito, width=30).pack(pady=3)
        ttk.Button(frame, text="Eliminar prerequisito", command=self.eliminar_prerequisito, width=30).pack(pady=3)
        ttk.Button(frame, text="Eliminar curso", command=self.eliminar_curso, width=30).pack(pady=3)
        ttk.Button(frame, text="Restaurar curso eliminado", command=self.restaurar_curso, width=30).pack(pady=3)
        ttk.Button(frame, text="Ver materiales de curso", command=self.ver_materiales, width=30).pack(pady=5)
        ttk.Button(frame, text="Volver al menú principal", command=self.menu_principal, width=30).pack(pady=5)

    def menu_inscripciones(self) -> None:
        self._limpiar_ventana()
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=20)

        tk.Label(frame, text="===== INSCRIPCIONES =====", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)

        ttk.Button(frame, text="Inscribir estudiante en curso", command=self.inscribir_estudiante, width=30).pack(pady=5)
        ttk.Button(frame, text="Cancelar inscripción", command=self.cancelar_inscripcion, width=30).pack(pady=5)
        ttk.Button(frame, text="Deshacer última acción", command=self.deshacer_ultima_accion, width=30).pack(pady=5)
        ttk.Button(frame, text="Volver al menú principal", command=self.menu_principal, width=30).pack(pady=5)

    def menu_busquedas(self) -> None:
        self._limpiar_ventana()
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=20)

        tk.Label(frame, text="===== BÚSQUEDAS =====", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)

        ttk.Button(frame, text="Buscar cursos por tema", command=self.buscar_cursos_tema, width=30).pack(pady=5)
        ttk.Button(frame, text="Buscar cursos por tema y nivel", command=self.buscar_cursos_tema_nivel, width=30).pack(pady=5)
        ttk.Button(frame, text="Recomendar ruta de aprendizaje", command=self.recomendar_ruta, width=30).pack(pady=5)
        ttk.Button(frame, text="Volver al menú principal", command=self.menu_principal, width=30).pack(pady=5)

    # ══════════════════════════════════════════════════════════════════
    #  Gestión de Estudiantes
    # ══════════════════════════════════════════════════════════════════

    def registrar_estudiante(self) -> None:
        def guardar():
            try:
                id = int(entry_id.get())
                nombre = entry_nombre.get()
                email = entry_email.get()
                if not all([id, nombre]):
                    raise ValueError("El ID y el nombre son obligatorios.")
                est = self.sistema.registrar_estudiante(id, nombre, email)
                if est:
                    messagebox.showinfo("Éxito", f"Estudiante {nombre} registrado correctamente!")
                else:
                    messagebox.showerror("Error", "Ya existe un estudiante con ese ID.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        win = tk.Toplevel(self.root)
        win.title("Registrar Estudiante")
        win.configure(bg="#f0f0f0")

        tk.Label(win, text="ID:", bg="#f0f0f0").pack(pady=5)
        entry_id = tk.Entry(win); entry_id.pack(pady=5)

        tk.Label(win, text="Nombre:", bg="#f0f0f0").pack(pady=5)
        entry_nombre = tk.Entry(win); entry_nombre.pack(pady=5)

        tk.Label(win, text="Email:", bg="#f0f0f0").pack(pady=5)
        entry_email = tk.Entry(win); entry_email.pack(pady=5)

        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)
        win.bind('<Return>', lambda e: guardar())

    def ver_estudiantes(self) -> None:
        win = tk.Toplevel(self.root)
        win.title("Lista de Estudiantes")
        win.configure(bg="#f0f0f0")

        if not self.sistema.estudiantes:
            tk.Label(win, text="No hay estudiantes registrados.", bg="#f0f0f0").pack(pady=10)
            return

        tk.Label(win, text="LISTA DE ESTUDIANTES:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        frame = tk.Frame(win); frame.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(frame, bg="#f0f0f0")
        sb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg="#f0f0f0")

        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)

        for id, est in self.sistema.estudiantes.items():
            tk.Label(sf, text=f"ID: {id} | Nombre: {est.nombre} | Email: {est.email}", bg="#f0f0f0").pack(pady=5)

        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    def eliminar_estudiante(self) -> None:
        def confirmar():
            try:
                id = int(entry_id.get())
                if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este estudiante?"):
                    if self.sistema.eliminar_estudiante(id):
                        messagebox.showinfo("Éxito", "Estudiante eliminado correctamente!")
                    else:
                        messagebox.showerror("Error", "Error al eliminar. Verifique el ID.")
            except ValueError:
                messagebox.showerror("Error", "ID inválido.")

        win = tk.Toplevel(self.root); win.title("Eliminar Estudiante"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="ID del estudiante:", bg="#f0f0f0").pack(pady=5)
        entry_id = tk.Entry(win); entry_id.pack(pady=5)
        ttk.Button(win, text="Eliminar", command=confirmar).pack(pady=10)

    def ver_cursos_estudiante(self) -> None:
        def buscar():
            try:
                id = int(entry_id.get())
                if id in self.sistema.estudiantes:
                    est = self.sistema.estudiantes[id]
                    win2 = tk.Toplevel(win); win2.title(f"Cursos de {est.nombre}"); win2.configure(bg="#f0f0f0")
                    if not est.cursos:
                        tk.Label(win2, text="No está inscrito en ningún curso.", bg="#f0f0f0").pack(pady=10)
                    else:
                        tk.Label(win2, text=f"Cursos de {est.nombre}:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
                        for c in est.cursos:
                            tk.Label(win2, text=f"- {c.nombre} (Nivel: {c.nivel})", bg="#f0f0f0").pack(pady=5)
                else:
                    messagebox.showerror("Error", "Estudiante no encontrado.")
            except ValueError:
                messagebox.showerror("Error", "ID inválido.")

        win = tk.Toplevel(self.root); win.title("Ver Cursos de Estudiante"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="ID del estudiante:", bg="#f0f0f0").pack(pady=5)
        entry_id = tk.Entry(win); entry_id.pack(pady=5)
        ttk.Button(win, text="Buscar", command=buscar).pack(pady=10)

    # ══════════════════════════════════════════════════════════════════
    #  Gestión de Cursos
    # ══════════════════════════════════════════════════════════════════

    def crear_curso(self) -> None:
        def guardar():
            try:
                id = int(entry_id.get())
                nombre = entry_nombre.get()
                desc = entry_desc.get()
                nivel = entry_nivel.get()
                if not all([id, nombre, desc, nivel]):
                    raise ValueError("Todos los campos son obligatorios.")
                c = self.sistema.crear_curso(id, nombre, desc, nivel)
                if c:
                    messagebox.showinfo("Éxito", f"Curso '{nombre}' creado correctamente!")
                else:
                    messagebox.showerror("Error", "Ya existe un curso con ese ID.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        win = tk.Toplevel(self.root); win.title("Crear Curso"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="ID:", bg="#f0f0f0").pack(pady=5); entry_id = tk.Entry(win); entry_id.pack(pady=5)
        tk.Label(win, text="Nombre:", bg="#f0f0f0").pack(pady=5); entry_nombre = tk.Entry(win); entry_nombre.pack(pady=5)
        tk.Label(win, text="Descripción:", bg="#f0f0f0").pack(pady=5); entry_desc = tk.Entry(win); entry_desc.pack(pady=5)
        tk.Label(win, text="Nivel:", bg="#f0f0f0").pack(pady=5); entry_nivel = tk.Entry(win); entry_nivel.pack(pady=5)
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def ver_cursos(self) -> None:
        win = tk.Toplevel(self.root); win.title("Lista de Cursos"); win.configure(bg="#f0f0f0")
        if not self.sistema.cursos:
            tk.Label(win, text="No hay cursos registrados.", bg="#f0f0f0").pack(pady=10)
            return

        tk.Label(win, text="LISTA DE CURSOS:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        frame = tk.Frame(win); frame.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(frame, bg="#f0f0f0"); sb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg="#f0f0f0")
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw"); canvas.configure(yscrollcommand=sb.set)

        for id, c in self.sistema.cursos.items():
            tk.Label(sf, text=f"ID: {id} | Nombre: {c.nombre} | Nivel: {c.nivel}", bg="#f0f0f0").pack(pady=5)
            tk.Label(sf, text=f"  Descripción: {c.descripcion}", bg="#f0f0f0").pack(pady=2)
            tk.Label(sf, text=f"  Estudiantes: {len(c.estudiantes)} | Materiales: {len(c.materiales)}", bg="#f0f0f0").pack(pady=2)
            if c.prerequisitos:
                pre_nombres = ", ".join(self.sistema.cursos[pre_id].nombre for pre_id in c.prerequisitos if pre_id in self.sistema.cursos)
                tk.Label(sf, text=f"  Prerequisitos: {pre_nombres}", bg="#f0f0f0").pack(pady=2)
            tk.Label(sf, text="", bg="#f0f0f0").pack(pady=5)

        canvas.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")

    def agregar_material(self) -> None:
        def guardar():
            try:
                c_id = int(entry_c_id.get()); m_id = int(entry_m_id.get())
                nombre = entry_nombre.get(); tipo = entry_tipo.get(); url = entry_url.get()
                if not all([c_id, m_id, nombre, tipo, url]):
                    raise ValueError("Todos los campos son obligatorios.")
                if c_id in self.sistema.cursos:
                    mat = Material(m_id, nombre, tipo, url)
                    if self.sistema.agregar_material(c_id, mat):
                        messagebox.showinfo("Éxito", f"Material agregado al curso {self.sistema.cursos[c_id].nombre}!")
                else:
                    messagebox.showerror("Error", "Curso no encontrado.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        win = tk.Toplevel(self.root); win.title("Agregar Material"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="ID del curso:", bg="#f0f0f0").pack(pady=5); entry_c_id = tk.Entry(win); entry_c_id.pack(pady=5)
        tk.Label(win, text="ID del material:", bg="#f0f0f0").pack(pady=5); entry_m_id = tk.Entry(win); entry_m_id.pack(pady=5)
        tk.Label(win, text="Nombre:", bg="#f0f0f0").pack(pady=5); entry_nombre = tk.Entry(win); entry_nombre.pack(pady=5)
        tk.Label(win, text="Tipo (PDF, Video, etc.):", bg="#f0f0f0").pack(pady=5); entry_tipo = tk.Entry(win); entry_tipo.pack(pady=5)
        tk.Label(win, text="URL o ruta:", bg="#f0f0f0").pack(pady=5); entry_url = tk.Entry(win); entry_url.pack(pady=5)
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def eliminar_material(self) -> None:
        def guardar():
            try:
                c_id = int(entry_c_id.get()); m_id = int(entry_m_id.get())
                if self.sistema.eliminar_material(c_id, m_id):
                    messagebox.showinfo("Éxito", "Material eliminado correctamente!")
                else:
                    messagebox.showerror("Error", "Error al eliminar material. Verifique los IDs.")
            except ValueError:
                messagebox.showerror("Error", "IDs inválidos.")

        win = tk.Toplevel(self.root); win.title("Eliminar Material"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="ID del curso:", bg="#f0f0f0").pack(pady=5); entry_c_id = tk.Entry(win); entry_c_id.pack(pady=5)
        tk.Label(win, text="ID del material:", bg="#f0f0f0").pack(pady=5); entry_m_id = tk.Entry(win); entry_m_id.pack(pady=5)
        ttk.Button(win, text="Eliminar", command=guardar).pack(pady=10)

    def establecer_prerequisito(self) -> None:
        def guardar():
            try:
                c_id = int(entry_c_id.get()); p_id = int(entry_p_id.get())
                if c_id == p_id:
                    messagebox.showerror("Error", "Un curso no puede ser prerequisito de sí mismo.")
                elif self.sistema.establecer_prerequisito(c_id, p_id):
                    messagebox.showinfo("Éxito", "Prerequisito establecido correctamente!")
                else:
                    messagebox.showerror("Error", "Error al establecer prerequisito. Verifique los IDs.")
            except ValueError:
                messagebox.showerror("Error", "IDs inválidos.")

        win = tk.Toplevel(self.root); win.title("Establecer Prerequisito"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="ID del curso principal:", bg="#f0f0f0").pack(pady=5); entry_c_id = tk.Entry(win); entry_c_id.pack(pady=5)
        tk.Label(win, text="ID del curso prerequisito:", bg="#f0f0f0").pack(pady=5); entry_p_id = tk.Entry(win); entry_p_id.pack(pady=5)
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def eliminar_prerequisito(self) -> None:
        def guardar():
            try:
                c_id = int(entry_c_id.get()); p_id = int(entry_p_id.get())
                if self.sistema.eliminar_prerequisito(c_id, p_id):
                    messagebox.showinfo("Éxito", "Prerequisito eliminado correctamente!")
                else:
                    messagebox.showerror("Error", "Error al eliminar prerequisito. Verifique los IDs.")
            except ValueError:
                messagebox.showerror("Error", "IDs inválidos.")

        win = tk.Toplevel(self.root); win.title("Eliminar Prerequisito"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="ID del curso principal:", bg="#f0f0f0").pack(pady=5); entry_c_id = tk.Entry(win); entry_c_id.pack(pady=5)
        tk.Label(win, text="ID del curso prerequisito:", bg="#f0f0f0").pack(pady=5); entry_p_id = tk.Entry(win); entry_p_id.pack(pady=5)
        ttk.Button(win, text="Eliminar", command=guardar).pack(pady=10)

    def eliminar_curso(self) -> None:
        def confirmar():
            try:
                c_id = int(entry_c_id.get())
                if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este curso?"):
                    if self.sistema.eliminar_curso(c_id):
                        messagebox.showinfo("Éxito", "Curso eliminado correctamente!")
                    else:
                        messagebox.showerror("Error", "Error al eliminar curso. Verifique el ID.")
            except ValueError:
                messagebox.showerror("Error", "ID inválido.")

        win = tk.Toplevel(self.root); win.title("Eliminar Curso"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="ID del curso:", bg="#f0f0f0").pack(pady=5); entry_c_id = tk.Entry(win); entry_c_id.pack(pady=5)
        ttk.Button(win, text="Eliminar", command=confirmar).pack(pady=10)

    def restaurar_curso(self) -> None:
        def confirmar():
            try:
                c_id = int(entry_c_id.get())
                if self.sistema.restaurar_curso(c_id):
                    messagebox.showinfo("Éxito", "Curso restaurado correctamente!")
                else:
                    messagebox.showerror("Error", "Error al restaurar curso. Verifique el ID.")
            except ValueError:
                messagebox.showerror("Error", "ID inválido.")

        win = tk.Toplevel(self.root); win.title("Restaurar Curso"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="ID del curso eliminado:", bg="#f0f0f0").pack(pady=5); entry_c_id = tk.Entry(win); entry_c_id.pack(pady=5)
        ttk.Button(win, text="Restaurar", command=confirmar).pack(pady=10)

    def ver_materiales(self) -> None:
        win = tk.Toplevel(self.root); win.title("Materiales de Cursos"); win.configure(bg="#f0f0f0")
        if not self.sistema.cursos:
            tk.Label(win, text="No hay cursos registrados.", bg="#f0f0f0").pack(pady=10)
            return

        tk.Label(win, text="LISTA DE MATERIALES:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        frame = tk.Frame(win); frame.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(frame, bg="#f0f0f0"); sb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg="#f0f0f0")
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw"); canvas.configure(yscrollcommand=sb.set)

        for c in self.sistema.cursos.values():
            for m in c.materiales:
                tk.Label(sf, text=f"ID: {m.id} | Nombre: {m.nombre} | Tipo: {m.tipo}", bg="#f0f0f0").pack(pady=5)
                tk.Label(sf, text=f"  URL: {m.url}", bg="#f0f0f0").pack(pady=2)
                tk.Label(sf, text=f"  Curso: {c.nombre}", bg="#f0f0f0").pack(pady=2)

        canvas.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")

    # ══════════════════════════════════════════════════════════════════
    #  Inscripciones
    # ══════════════════════════════════════════════════════════════════

    def inscribir_estudiante(self) -> None:
        def guardar():
            try:
                e_id = int(entry_e_id.get()); c_id = int(entry_c_id.get())
                res = self.sistema.inscribir_estudiante(e_id, c_id)
                if res == True:
                    messagebox.showinfo("Éxito", "Estudiante inscrito correctamente!")
                elif res == "ya_inscrito":
                    messagebox.showwarning("Aviso", "El estudiante ya está inscrito en este curso.")
                elif res == "prerequisitos_faltantes":
                    messagebox.showerror("Error", "El estudiante no cumple con los prerequisitos.")
                elif res == "lista_espera":
                    messagebox.showinfo("Lista de espera", "El curso está lleno. Estudiante añadido a lista de espera.")
                else:
                    messagebox.showerror("Error", "Estudiante o curso no encontrados.")
            except ValueError:
                messagebox.showerror("Error", "IDs inválidos.")

        win = tk.Toplevel(self.root); win.title("Inscribir Estudiante"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="ID del estudiante:", bg="#f0f0f0").pack(pady=5); entry_e_id = tk.Entry(win); entry_e_id.pack(pady=5)
        tk.Label(win, text="ID del curso:", bg="#f0f0f0").pack(pady=5); entry_c_id = tk.Entry(win); entry_c_id.pack(pady=5)
        ttk.Button(win, text="Inscribir", command=guardar).pack(pady=10)

    def cancelar_inscripcion(self) -> None:
        def guardar():
            try:
                e_id = int(entry_e_id.get()); c_id = int(entry_c_id.get())
                if self.sistema.cancelar_inscripcion(e_id, c_id):
                    messagebox.showinfo("Éxito", "Inscripción cancelada correctamente!")
                else:
                    messagebox.showerror("Error", "No se pudo cancelar. Verifique IDs o si estaba inscrito.")
            except ValueError:
                messagebox.showerror("Error", "IDs inválidos.")

        win = tk.Toplevel(self.root); win.title("Cancelar Inscripción"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="ID del estudiante:", bg="#f0f0f0").pack(pady=5); entry_e_id = tk.Entry(win); entry_e_id.pack(pady=5)
        tk.Label(win, text="ID del curso:", bg="#f0f0f0").pack(pady=5); entry_c_id = tk.Entry(win); entry_c_id.pack(pady=5)
        ttk.Button(win, text="Cancelar", command=guardar).pack(pady=10)

    def deshacer_ultima_accion(self) -> None:
        if self.sistema.deshacer_ultima_accion():
            messagebox.showinfo("Éxito", "Última acción deshecha correctamente!")
        else:
            messagebox.showerror("Error", "No hay acciones para deshacer.")

    # ══════════════════════════════════════════════════════════════════
    #  Búsquedas
    # ══════════════════════════════════════════════════════════════════

    def buscar_cursos_tema(self) -> None:
        def buscar():
            tema = entry_tema.get()
            resultados = self.sistema.buscar_cursos(tema)
            self._mostrar_resultados_busqueda(resultados, f"Búsqueda: '{tema}'")

        win = tk.Toplevel(self.root); win.title("Buscar por Tema"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="Tema (nombre del curso):", bg="#f0f0f0").pack(pady=5)
        entry_tema = tk.Entry(win); entry_tema.pack(pady=5)
        ttk.Button(win, text="Buscar", command=buscar).pack(pady=10)

    def buscar_cursos_tema_nivel(self) -> None:
        def buscar():
            tema = entry_tema.get(); nivel = entry_nivel.get()
            resultados = self.sistema.buscar_cursos(tema, nivel)
            self._mostrar_resultados_busqueda(resultados, f"Búsqueda: '{tema}' - Nivel: {nivel}")

        win = tk.Toplevel(self.root); win.title("Buscar por Tema y Nivel"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="Tema:", bg="#f0f0f0").pack(pady=5); entry_tema = tk.Entry(win); entry_tema.pack(pady=5)
        tk.Label(win, text="Nivel:", bg="#f0f0f0").pack(pady=5); entry_nivel = tk.Entry(win); entry_nivel.pack(pady=5)
        ttk.Button(win, text="Buscar", command=buscar).pack(pady=10)

    def recomendar_ruta(self) -> None:
        def buscar():
            try:
                c_id = int(entry_c_id.get())
                ruta = self.sistema.recomendar_cursos(c_id)
                win2 = tk.Toplevel(win); win2.title("Ruta de Aprendizaje"); win2.configure(bg="#f0f0f0")
                if not ruta:
                    tk.Label(win2, text="No se encontró ruta o el curso no existe.", bg="#f0f0f0").pack(pady=10)
                else:
                    tk.Label(win2, text="Ruta recomendada:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
                    for i, c in enumerate(ruta, 1):
                        tk.Label(win2, text=f"{i}. {c.nombre} (Nivel: {c.nivel})", bg="#f0f0f0").pack(pady=3)
            except ValueError:
                messagebox.showerror("Error", "ID inválido.")

        win = tk.Toplevel(self.root); win.title("Ruta de Aprendizaje"); win.configure(bg="#f0f0f0")
        tk.Label(win, text="ID del curso objetivo:", bg="#f0f0f0").pack(pady=5); entry_c_id = tk.Entry(win); entry_c_id.pack(pady=5)
        ttk.Button(win, text="Recomendar", command=buscar).pack(pady=10)

    def _mostrar_resultados_busqueda(self, resultados, titulo) -> None:
        win = tk.Toplevel(self.root); win.title(titulo); win.configure(bg="#f0f0f0")
        if not resultados:
            tk.Label(win, text="No se encontraron cursos.", bg="#f0f0f0").pack(pady=10)
        else:
            for c in resultados:
                tk.Label(win, text=f"- {c.nombre} (Nivel: {c.nivel}) | {c.descripcion}", bg="#f0f0f0").pack(pady=5)
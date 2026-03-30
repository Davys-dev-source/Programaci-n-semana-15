import tkinter as tk
from tkinter import ttk

# =========================
# MODELO (modelos/tarea.py)
# =========================
class Tarea:
    _id_counter = 1

    def __init__(self, descripcion):
        self.id = Tarea._id_counter
        Tarea._id_counter += 1
        self.descripcion = descripcion
        self.completada = False


# =========================
# SERVICIO (servicios/tarea_servicio.py)
# =========================
class TareaServicio:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, descripcion):
        if descripcion.strip():
            tarea = Tarea(descripcion)
            self.tareas.append(tarea)
            return tarea
        return None

    def completar_tarea(self, tarea_id):
        for tarea in self.tareas:
            if tarea.id == tarea_id:
                tarea.completada = True
                return tarea
        return None

    def eliminar_tarea(self, tarea_id):
        self.tareas = [t for t in self.tareas if t.id != tarea_id]

    def listar_tareas(self):
        return self.tareas


# =========================
# UI (ui/app_tkinter.py)
# =========================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")

        self.servicio = TareaServicio()

        # Entrada
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=10)

        # Evento Enter
        self.entry.bind("<Return>", self.agregar_tarea_evento)

        # Botones
        frame_botones = tk.Frame(root)
        frame_botones.pack()

        tk.Button(frame_botones, text="Añadir Tarea", command=self.agregar_tarea).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Marcar Completada", command=self.completar_tarea).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Eliminar", command=self.eliminar_tarea).grid(row=0, column=2, padx=5)

        # Lista
        self.tree = ttk.Treeview(root, columns=("Estado"), show="headings")
        self.tree.heading("Estado", text="Tarea")
        self.tree.pack(pady=10)

        # Evento doble clic
        self.tree.bind("<Double-1>", self.completar_tarea_evento)

    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for tarea in self.servicio.listar_tareas():
            texto = tarea.descripcion
            if tarea.completada:
                texto = f"[Hecho] {texto}"
                self.tree.insert("", "end", iid=tarea.id, values=(texto,), tags=("completada",))
            else:
                self.tree.insert("", "end", iid=tarea.id, values=(texto,))

        self.tree.tag_configure("completada", foreground="gray")

    def agregar_tarea(self):
        descripcion = self.entry.get()
        self.servicio.agregar_tarea(descripcion)
        self.entry.delete(0, tk.END)
        self.actualizar_lista()

    def agregar_tarea_evento(self, event):
        self.agregar_tarea()

    def completar_tarea(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            tarea_id = int(seleccionado[0])
            self.servicio.completar_tarea(tarea_id)
            self.actualizar_lista()

    def completar_tarea_evento(self, event):
        self.completar_tarea()

    def eliminar_tarea(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            tarea_id = int(seleccionado[0])
            self.servicio.eliminar_tarea(tarea_id)
            self.actualizar_lista()


# =========================
# MAIN (main.py)
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
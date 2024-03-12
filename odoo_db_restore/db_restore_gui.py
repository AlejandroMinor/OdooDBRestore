import tkinter as tk
import os
from tkinter import filedialog
import OdooDBRestore
class DbRestoreGui:
    def __init__(self):
        self.file_path = None
        self.output_path = None 

    def open_gui_interface(self):
        window = tk.Tk()
        window.title("Odoo DB Restore")

        tk.Label(window, text="Archivo sql:").pack()

        self.file_path = tk.Entry(window, width=50)
        self.file_path.pack()

        btn_select_file = tk.Button(window, text="Seleccionar archivo sql", command=self.select_file)
        btn_select_file.pack()

        tk.Label(window, text="Ruta del filestore a copiar:").pack()
        self.output_path = tk.Entry(window, width=50)
        self.output_path.pack()

        btn_output_path = tk.Button(window, text="Seleccionar ruta", command=self.select_output_path)
        btn_output_path.pack()

        btn_restore = tk.Button(window, text="Restaurar", command=lambda: self.restore(self.file_path.get(), self.output_path.get()))
        btn_restore.pack()

        window.mainloop()
    def select_file(self):
        archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivos .slq", "*.sql"), ("Archivos .dump", "*.dump")])
        self.file_path.delete(0, tk.END)  
        self.file_path.insert(0, archivo)  

    def show_success_message(self, message=''):
        tk.messagebox.showinfo("Información", message)

    def show_error_message(self, message=''):
        tk.messagebox.showerror("Error", message)

    def select_output_path(self):
        path = filedialog.askdirectory()
        self.output_path.delete(0, tk.END)
        self.output_path.insert(0, path)

    def restore(self, slq_file, filestore_folder):
        if self.verify_fields(slq_file, filestore_folder) and self.confirm_action():    
            database_name = os.path.basename(filestore_folder)
            restore_obj = OdooDBRestore.OdooDBRestore(filestore_folder, database_name, slq_file)
            restore_obj.action_odoo_server("stop")
            restore_obj.copy_filestore(filestore_folder)
            restore_obj.set_filestore_permissions(database_name)
            restore_obj.create_database(database_name)
            restore_obj.restore_database(database_name, slq_file)
            restore_obj.action_odoo_server("start")
            self.show_success_message("Restauración completada")
        else:
            self.show_error_message("Restauración cancelada")

    def confirm_action(self):
        return tk.messagebox.askyesno("Confirmación", "¿Está seguro de realizar esta acción?")

    def verify_fields(self, slq_file, filestore_folder):
        if not slq_file or not filestore_folder:
            self.show_error_message("Debe seleccionar un archivo sql y una ruta para el filestore")
            return False
        return True
    


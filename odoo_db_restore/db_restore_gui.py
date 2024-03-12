import tkinter as tk
import os
from tkinter import filedialog
import odoo_db_restore.OdooDBRestore
class DbRestoreGui:
    def __init__(self):
        self.file_path = None
        self.output_path = None 

    def open_gui_interface(self):
        window = tk.Tk()
        window.title("Odoo DB Restore")
        window.geometry("500x250")
        window.resizable(width=False, height=False)

        tk.Label(window, text="Ruta del filestore a copiar:").place(x=20, y=10)
        self.output_path = tk.Entry(window, width=58)
        self.output_path.place(x=20, y=30)

        btn_output_path = tk.Button(window, text="Seleccionar ruta", command=self.select_output_path)
        btn_output_path.place(x=20, y=55)

        tk.Label(window, text="Archivo SQL:").place(x=20, y=110)
        self.file_path = tk.Entry(window, width=58)
        self.file_path.place(x=20, y=130)

        btn_select_file = tk.Button(window, text="Seleccionar archivo SQL", command=self.select_file)
        btn_select_file.place(x=20, y=155)

        btn_restore = tk.Button(window, text="Restaurar", command=lambda: self.restore(self.file_path.get(), self.output_path.get()))
        btn_restore.place(x=200, y=200)

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
    

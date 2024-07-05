import os
import subprocess
import tkinter as tk
from tkinter import filedialog


class OdooDBRestore:

    def __init__(self, filestore_folder="", database_name="", dump_file=""):
        self.filestore_folder = filestore_folder
        self.database_name = database_name
        self.dump_file = dump_file
        
    def action_odoo_server(self, action):
        print(f"Odoo server {action} \n")
        subprocess.run(["sudo", "/etc/init.d/odoo", action])
        print(f"➡ Odoo server {action}ed \n")

    def copy_filestore(self, filestore_folder):
        self.filestore_folder = filestore_folder
        self.validate_filestore(self.filestore_folder)
        print("Copiando filestore. Este proceso puede tardar varios minutos.\n")
        subprocess.run(["sudo", "cp", "-R", self.filestore_folder, "/var/lib/odoo/.local/share/Odoo/filestore/","-v"])
        print("➡ Filestore copiado.\n")

    def set_filestore_permissions(self,filestore_folder):
        print("Cambiando permisos de filestore.\n")
        self.get_filestore_permissions()
        subprocess.run(["sudo", "chown", "-R", "odoo:odoo", f"/var/lib/odoo/.local/share/Odoo/filestore/{filestore_folder}"])
        print("➡ Permisos cambiados.\n")
        self.get_filestore_permissions()

    def get_filestore_permissions(self):
        result = subprocess.run(["ls", "-l", "/var/lib/odoo/.local/share/Odoo/filestore/"], capture_output=True, text=True)
        print(result.stdout)

    def create_database(self,database_name):
        print("Creando base de datos.\n")
        subprocess.run(["psql", "-h", "localhost", "-U", "odoo", "-d", "postgres", "-W"],
                    input=f"create database \"{database_name}\";\n".encode())
        print("➡ Base de datos creada.\n")

    def restore_database(self,database_name, dump_file):
        self.dump_file = dump_file
        self.validate_dump_file(self.dump_file)
        self.database_name = database_name
        print("Restaurando base de datos. Este proceso puede tardar varios minutos.\n")
        subprocess.run(["sudo", "su", "-", "postgres", "-c",
                        f"psql -U odoo -d {self.database_name} -f {self.dump_file}"])
        print("➡ Base de datos restaurada.\n")
        

    def define_restore_paths(self):
        while True:
            filestore_folder, database_name = self.define_filestore()
            dump_file = self.define_dump_file()

            # Resumen de datos
            print(f"Resumen de datos:\n"
                    f"Ruta de la carpeta filestore: {filestore_folder}\n"
                    f"Nombre de la base de datos: {database_name}\n"
                    f"Ruta del archivo SQL de respaldo: {dump_file}\n")
            confirm = input("¿Los datos son correctos? (S/N): ")
            if confirm.lower() == "s":
                self.filestore_folder = filestore_folder
                self.database_name = database_name
                self.dump_file = dump_file
                break
            else:
                print("Por favor ingrese los datos nuevamente.\n")


    def sequence_restore(self):
        self.define_restore_paths()
        self.action_odoo_server("stop")
        self.copy_filestore(self.filestore_folder)
        self.set_filestore_permissions(self.database_name)
        self.create_database(self.database_name)
        self.restore_database(self.database_name, self.dump_file)
        self.action_odoo_server("start")

    def define_filestore(self):
        while True:
            self.filestore_folder = input("Ruta de la carpeta filestore (Ejem /home/minor/Escritorio/filestore_folder_name):")
            if self.validate_filestore(self.filestore_folder):
                self.database_name = os.path.basename(self.filestore_folder)
                print(f"Nombre de la base de datos sera {self.database_name}")
                break
        return self.filestore_folder, self.database_name
    
    def define_dump_file(self):
        while True:
            dump_file = input("Ruta del archivo SQL de respaldo (Ejem /home/minor/Escritorio/dump.sql): ")
            if not os.path.isfile(dump_file) or not dump_file.endswith(".sql"):
                print("El archivo especificado no es valido o no existe.")
            else:
                self.dump_file = dump_file
                break
        return self.dump_file

    def validate_filestore(self, filestore_folder):
        if not os.path.exists(filestore_folder):
            print(f"La ruta '{filestore_folder}' no existe")
            return False
        
        if not os.path.isdir(filestore_folder):
            print(f"La ruta '{filestore_folder}' no es una carpeta")
            return False
        
        if filestore_folder.endswith("/"):
            print(f"La ruta '{filestore_folder}' no debe terminar con '/'")
            return False
        
        else:
            return True
    
    def validate_dump_file(self, dump_file):
        if not os.path.isfile(dump_file) or not dump_file.endswith(".sql"):
            print(f"El archivo '{dump_file}' no es valido o no existe")
            self.define_dump_file()

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
        archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivos .sql", "*.sql"), ("Archivos .dump", "*.dump")])
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
            restore_obj = OdooDBRestore(filestore_folder, database_name, slq_file)
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

    

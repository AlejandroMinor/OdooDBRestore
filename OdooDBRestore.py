import os
import subprocess

def action_odoo_server(action):
    print(f"Odoo server {action} \n")
    subprocess.run(["sudo", "/etc/init.d/odoo", action])
    print(f"➡ Odoo server {action}ed \n")

def copy_filestore(filestore_folder):
    print("Copiando filestore. Este proceso puede tardar varios minutos.\n")
    subprocess.run(["sudo", "cp", "-R", filestore_folder, "/var/lib/odoo/.local/share/Odoo/filestore/"])
    print("➡ Filestore copiado.\n")
def set_filestore_permissions(filestore_folder):
    print("Cambiando permisos de filestore.\n")
    get_filestore_permissions()
    subprocess.run(["sudo", "chown", "-R", "odoo:odoo", f"/var/lib/odoo/.local/share/Odoo/filestore/{filestore_folder}"])
    print("➡ Permisos cambiados.\n")
    get_filestore_permissions()

def get_filestore_permissions():
    result = subprocess.run(["ls", "-l", "/var/lib/odoo/.local/share/Odoo/filestore/"], capture_output=True, text=True)
    print(result.stdout)


def create_database(database_name):
    print("Creando base de datos.\n")
    subprocess.run(["psql", "-h", "localhost", "-U", "odoo", "-d", "postgres", "-W"],
                   input=f"create database \"{database_name}\";\n".encode())
    print("➡ Base de datos creada.\n")
def restore_database(database_name, dump_file):
    print("Restaurando base de datos. Este proceso puede tardar varios minutos.\n")
    subprocess.run(["sudo", "su", "-", "postgres", "-c",
                    f"psql -U odoo -d {database_name} -f {dump_file}"])
    print("➡ Base de datos restaurada.\n")


# Rutas y nombres de archivos
filestore_folder = "filestore_folder_name"
database_name = "DB_NAME"
dump_file = "/path/to/dump.sql"

# Solicitar datos
filestore_folder = input("Ruta de la carpeta filestore (Ejem /home/minor/Escritorio/filestore_folder_name):")
# Verificar si la ruta existe
if not os.path.exists(filestore_folder):
    print("La ruta especificada no existe.")
    exit()
database_name = os.path.basename(filestore_folder)
print(f"Nombre de la base de datos sera {database_name}")
dump_file = input("Ruta del archivo SQL de respaldo (Ejem /home/minor/Escritorio/dump.sql): ")
#verificar si el archivo existe
if not os.path.exists(dump_file):
    print("El archivo especificado no existe.")
    exit()

# Resumen de datos
print(f"Resumen de datos:\n"
        f"Ruta de la carpeta filestore: {filestore_folder}\n"
        f"Nombre de la base de datos: {database_name}\n"
        f"Ruta del archivo SQL de respaldo: {dump_file}\n")

# Confirmación de accion a realizar
confirm = input("¿Desea continuar? (S/N): ")
if confirm.lower() != "s":
    exit()

# Proceso de restauración
action_odoo_server("stop")
copy_filestore(filestore_folder)
set_filestore_permissions(filestore_folder)
create_database(database_name)
restore_database(database_name, dump_file)
action_odoo_server("start")

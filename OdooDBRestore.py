import subprocess

def action_odoo_server(action):
    print(f"Odoo server {action} \n")
    subprocess.run(["sudo", "/etc/init.d/odoo", action])

def copy_filestore(filestore_folder):
    print("Copiando filestore. Este proceso puede tardar varios minutos.\n")
    subprocess.run(["sudo", "cp", "-R", filestore_folder, "/var/lib/odoo/.local/share/Odoo/filestore/"])
    print("Filestore copiado.\n")
def set_filestore_permissions(filestore_folder):
    print("Cambiando permisos de filestore.\n")
    subprocess.run(["sudo", "chown", "-R", "odoo:odoo", f"/var/lib/odoo/.local/share/Odoo/filestore/{filestore_folder}"])
    print("Permisos cambiados.\n")
def create_database(database_name):
    print("Creando base de datos.\n")
    subprocess.run(["psql", "-h", "localhost", "-U", "odoo", "-d", "postgres", "-W"],
                   input=f"create database \"{database_name}\";\n".encode())
    print("Base de datos creada.\n")
def restore_database(database_name, dump_file):
    print("Restaurando base de datos. Este proceso puede tardar varios minutos.\n")
    subprocess.run(["sudo", "su", "-", "postgres", "-c",
                    f"psql -U odoo -d {database_name} -f {dump_file}"])
    print("Base de datos restaurada.\n")

# Rutas y nombres de archivos
filestore_folder = "filestore_folder_name"
database_name = "DB_NAME"
dump_file = "/path/to/dump.sql"

# Solicitar datos
database_name = input("Nombre de la base de datos y filestore: ")
filestore_folder = database_name
dump_file = input("Ruta del archivo SQL de respaldo (Ejem /home/minor/Escritorio/dump.sql): ")

# Proceso de restauración
action_odoo_server("stop")
copy_filestore(filestore_folder)
set_filestore_permissions(filestore_folder)
create_database(database_name)
restore_database(database_name, dump_file)
action_odoo_server("start")

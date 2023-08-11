# OdooDBRestore | Proyecto de Restauración Manual de Base de Datos de Odoo

Este proyecto tiene como objetivo facilitar la restauración de una base de datos de Odoo junto con el correspondiente filestore. Proporciona funciones para detener y reiniciar el servidor de Odoo, copiar y establecer permisos en el filestore, crear una nueva base de datos y restaurar una base de datos existente a partir de un archivo de respaldo SQL.

## Funciones

- `action_odoo_server(action)`: Permite detener o reiniciar el servidor de Odoo.
- `copy_filestore(filestore_folder)`: Copia el filestore a la ubicación adecuada en el sistema.
- `set_filestore_permissions(filestore_folder)`: Establece los permisos adecuados en el filestore.
- `create_database(database_name)`: Crea una nueva base de datos en el servidor de PostgreSQL.
- `restore_database(database_name, dump_file)`: Restaura una base de datos existente a partir de un archivo de respaldo SQL.

## Requisitos

- Python 3.x
- PostgreSQL
- Tener su servicio de odoo configurado de manera correcta
- Acceso sudo (para ciertas operaciones que requieren permisos de administrador)

## Cómo usar
1. El nombre de la carpeta con el filestore y el nombre de la base de datos debe ser la misma
2. Abre una terminal y y ejecuta el comando:
```shell
python3 OdooDBRestore/
```
4.  Te pedira el nombre del directorio que almacena el filestore (este al estar en el mismo directorio que el archivo .py solo necesitara del nombre), este nombre tambien se usara para el nombre de la base de datos que se creara. 
5. El proceso ira corriendo de manera automatica ejecutando las tareas una tras otra, hay que ser pacientes ya que algunas demoran algunos minutos. 


## Ejemplo

```shell
➜  Escritorio python3 OdooDBRestore/ 
➜  Nombre de la base de datos y filestore: Develop_Junio_2023
➜  Ruta del archivo SQL de respaldo: home/minor/Escritorio/dump.sql
```


## Errores 

Si marca error en postgres hay que colocar los siguientes valores en el archivo de configuracion:

```shell
sudo nano /etc/postgresql/12/main/pg_hba.conf
```

El archivo debe coincidir con los siguientes valores: 

``` t
# Database administrative login by Unix domain socket
local   all             postgres                                peer

# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             odoo            trust
# "local" is for Unix domain socket connections only
local   all             all                                     md5
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            md5
host    replication     all             ::1/128                 md5

```

Despues de modificar el archivo pg_hba.conf se debe reiniciar el servicio, para que reconozca los cambios:

```shell
service postgresql restart
```

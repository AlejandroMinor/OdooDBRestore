# OdooDBRestore | Restauración Manual de Base de Datos de Odoo

Este proyecto tiene como objetivo facilitar la restauración de una base de datos de Odoo junto con el correspondiente filestore. Proporciona funciones para detener y reiniciar el servidor de Odoo, copiar y establecer permisos en el filestore, crear una nueva base de datos y restaurar una base de datos existente a partir de un archivo de respaldo SQL.

## Nota 

El nombre de la base de datos se toma por medio del nombre de la carpeta del filestore ya que este va ligado a la base, por tanto si tu filestore se llama "Respaldo_01_04_2024" el nombre de la base sera el mismo. 

## Requisitos

- Python 3.x
- PostgreSQL
- Tener su servicio de odoo configurado de manera correcta
- Acceso sudo (para ciertas operaciones que requieren permisos de administrador)

## Cómo usar

1. Abre una terminal en la ruta del proyecto y ejecuta el comando:
```shell
python3 OdooDBRestore/odoo_db_restore
```
2. Selecciona una de las opciones para restaurar la base ya sea via terminal o por medio de interfaz grafica
3. Te pedira el nombre del directorio que almacena el filestore , este nombre tambien se usara para el nombre de la base de datos que se creara. 
4. Deberas colocar la ruta del archivo sql o dump
5. El proceso ira corriendo de manera automatica ejecutando las tareas una tras otra, hay que ser pacientes ya que algunas demoran algunos minutos.
6. Durante el proceso pedira algunas contraseñas como lo son las de usuario o de postgres


## Ejemplo

```shell
➜  python3 OdooDBRestore/odoo_db_restore
➜  Ruta de la carpeta filestore: home/minor/Escritorio/Develop_Junio_2023
➜  Ruta del archivo SQL de respaldo: home/minor/Escritorio/dump.sql
```


## Errores 
### Errores en filestore
Es importante verificar que se este copiando el filestore correcto de tu proyecto y no rutas más arriba en la jerarquía

### Duplicidad de nombres
Si ya tienes una base o filestore con el mismo nombre solo se van a sobre escribir por tanto no se veran mayores cambios

### Error de postgres
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

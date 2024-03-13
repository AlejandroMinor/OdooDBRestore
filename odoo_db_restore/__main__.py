import db_restore_tools

if __name__ == "__main__":

    options = {
        '1': db_restore_tools.OdooDBRestore().sequence_restore,
        '2': db_restore_tools.DbRestoreGui().open_gui_interface
    }

    while True:
        print("1. Restaurar secuencia de base de datos")
        print("2. Abrir interfaz gráfica de restauración de base de datos")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion in options:
            options[opcion]()
        elif opcion == "0":
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")


import OdooDBRestore
import db_restore_gui

if __name__ == "__main__":  
    # OdooDBRestore.OdooDBRestore().sequence_restore()
    db_restore_gui.DbRestoreGui().open_gui_interface()
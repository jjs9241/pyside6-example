from PySide6 import QtCore, QtWidgets

from typing import Callable

class MainApplication(QtWidgets.QApplication):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            cls._init = True
            super().__init__()

class MainWindow(QtWidgets.QMainWindow):
    
    _instance = None

    def __new__(cls):
        MainApplication()
        
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            super().__init__()
            cls._init = True
            self.setWindowTitle('Pyside6 Example')
            self.close_callback_map = {}
            
    def get_main_window(self):
        return self
    
    def set_main_view(self, main_view):
        self.main_view = main_view
        self.setCentralWidget(self.main_view.get_widget())
        self.show()

    def add_close_callback(self, key, callback_func: Callable):
        self.close_callback_map[key] = callback_func

    def closeEvent(self, event):
        for key, callback in self.close_callback_map.items():
            try:
                callback()
            except Exception as e:
                pass
        
        

class MainViewIdManager:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            cls._init = True

            self._id_top = -1
            self._garbage_pool = set()

    def new_id(self):
        result_id = self._id_top + 1
        if len(self._garbage_pool) > 0:
            result_id = self._garbage_pool.pop()
        else:
            self._id_top += 1
        return result_id
    
    def delete_id(self, target):
        self._garbage_pool.add(target)

    def get_object_name(self, main_view_id):
        return f'MAINVIEW_{main_view_id}'

class MainView(QtCore.QObject):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._main_view_id = MainViewIdManager().new_id()
        self.setObjectName(MainViewIdManager().get_object_name(self.get_main_view_id()))
    
    def get_widget(self):
        return self.widget
    
    def set_widget(self, widget):
        self.widget = widget

    def get_main_view_id(self):
        return self._main_view_id
    


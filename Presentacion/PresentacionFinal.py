import sys
import sqlite3
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QAction
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Inscripciones - Evento Académico")
        self.setMinimumSize(1200, 750)
        
        # Base de datos
        self.init_db()
        self.cargar_datos_ejemplo()
        
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Panel lateral (menú)
        self.create_side_panel(main_layout)
        
        # Área de contenido
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area, 1)
        
        # Páginas
        self.create_registration_page()
        self.create_search_page()
        self.create_list_page()
        self.create_reports_page()
        
        # Barra de menú
        self.create_menu_bar()

    def init_db(self):
        """Inicializa la base de datos SQLite"""
        self.conn = sqlite3.connect('inscripciones.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inscriptos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                dni TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                telefono TEXT,
                fecha_inscripcion DATE,
                institucion TEXT
            )
        ''')
        self.conn.commit()

    def cargar_datos_ejemplo(self):
        """Carga datos de ejemplo si la tabla está vacía"""
        self.cursor.execute("SELECT COUNT(*) FROM inscriptos")
        count = self.cursor.fetchone()[0]
        
        if count == 0:
            participantes_ejemplo = [
                ('María', 'Gómez', '30123456', 'maria.gomez@email.com', '1156789012', '2024-01-15', 'Universidad Nacional'),
                ('Carlos', 'López', '32234567', 'carlos.lopez@email.com', '1167890123', '2024-01-16', 'Universidad Tecnológica'),
                ('Ana', 'Martínez', '34345678', 'ana.martinez@email.com', '1178901234', '2024-01-17', 'Instituto Superior'),
                ('Pedro', 'Rodríguez', '36456789', 'pedro.rodriguez@email.com', '1189012345', '2024-01-18', 'Universidad Privada'),
                ('Laura', 'Fernández', '38567890', 'laura.fernandez@email.com', '1190123456', '2024-01-19', 'Colegio Profesional')
            ]
            
            try:
                self.cursor.executemany('''
                    INSERT INTO inscriptos 
                    (nombre, apellido, dni, email, telefono, fecha_inscripcion, institucion)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', participantes_ejemplo)
                self.conn.commit()
                print("Datos de ejemplo cargados correctamente")
            except sqlite3.IntegrityError as e:
                print(f"Error al cargar datos de ejemplo: {e}")

    def create_side_panel(self, main_layout):
        """Crea el panel lateral de navegación"""
        side_panel = QFrame()
        side_panel.setFixedWidth(280)
        side_panel.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border: none;
            }
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                text-align: center;
                font-size: 14px;
                border-radius: 8px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)
        
        layout = QVBoxLayout(side_panel)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 25, 15, 25)
        
        # Título del panel
        title = QLabel("MENÚ PRINCIPAL")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 20px;
                margin-bottom: 15px;
                background-color: #34495e;
                border-radius: 8px;
            }
        """)
        layout.addWidget(title)
        
        # Botones del menú - TEXTO CORREGIDO Y COMPLETO
        menu_items = [
            ("📝 Registrar Participante", 0),
            ("🔍 Buscar Inscriptos", 1),
            ("📋 Lista de Inscriptos", 2),
            ("📊 Generar Reportes", 3)
        ]
        
        self.menu_buttons = []
        for text, index in menu_items:
            btn = QPushButton(text)
            btn.setFixedSize(240, 70)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx=index: self.content_area.setCurrentIndex(idx))
            
            # Estilo específico para botones del menú
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 8px;
                    padding: 15px;
                }
                QPushButton:hover {
                    background-color: #219a52;
                }
            """)
            
            layout.addWidget(btn)
            self.menu_buttons.append(btn)
        
        # Espacio flexible
        layout.addStretch()
        
        # Información de ejemplo cargada
        info_label = QLabel("✓ 5 participantes de ejemplo cargados automáticamente")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
            QLabel {
                color: #bdc3c7;
                font-size: 12px;
                padding: 12px;
                margin-top: 20px;
                background-color: #34495e;
                border-radius: 6px;
            }
        """)
        layout.addWidget(info_label)
        
        main_layout.addWidget(side_panel)

    def create_menu_bar(self):
        """Crea la barra de menú superior"""
        menubar = self.menuBar()
        
        # Menú Archivo
        file_menu = menubar.addMenu('Archivo')
        
        export_action = QAction('Exportar datos', self)
        exit_action = QAction('Salir', self)
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(export_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

    def create_registration_page(self):
        """Crea la página de registro de participantes"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignTop)
        
        # Título
        title = QLabel("Registro de Participantes")
        title.setStyleSheet("""
            font-size: 26px; 
            font-weight: bold; 
            margin: 25px;
            color: #2c3e50;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Contenedor del formulario
        form_container = QWidget()
        form_layout = QFormLayout(form_container)
        form_layout.setContentsMargins(120, 40, 120, 40)
        form_layout.setSpacing(25)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        # Crear campos de entrada
        self.nombre_input = QLineEdit()
        self.apellido_input = QLineEdit()
        self.dni_input = QLineEdit()
        self.email_input = QLineEdit()
        self.telefono_input = QLineEdit()
        self.institucion_input = QLineEdit()
        
        # Estilo para campos de entrada
        input_style = """
            QLineEdit {
                padding: 15px;
                font-size: 15px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                min-height: 25px;
                min-width: 350px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """
        
        for input_field in [self.nombre_input, self.apellido_input, self.dni_input, 
                           self.email_input, self.telefono_input, self.institucion_input]:
            input_field.setStyleSheet(input_style)
        
        # Placeholders para guiar al usuario
        self.dni_input.setPlaceholderText("Solo números")
        self.email_input.setPlaceholderText("Debe contener @")
        self.telefono_input.setPlaceholderText("Solo números")
        
        # Crear etiquetas con asterisco para campos obligatorios
        labels = [
            ("Nombre*", self.nombre_input),
            ("Apellido*", self.apellido_input),
            ("DNI*", self.dni_input),
            ("Email*", self.email_input),
            ("Teléfono", self.telefono_input),
            ("Institución", self.institucion_input)
        ]
        
        for label_text, input_field in labels:
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 15px; font-weight: bold; color: #2c3e50;")
            form_layout.addRow(label, input_field)
        
        layout.addWidget(form_container)
        
        # Botón de registro
        btn_registrar = QPushButton("Registrar Participante")
        btn_registrar.clicked.connect(self.registrar_participante)
        btn_registrar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 18px 35px;
                font-size: 17px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)
        btn_registrar.setCursor(Qt.PointingHandCursor)
        btn_registrar.setFixedSize(280, 60)
        
        # Contenedor para centrar el botón
        button_container = QHBoxLayout()
        button_container.addStretch()
        button_container.addWidget(btn_registrar)
        button_container.addStretch()
        
        layout.addLayout(button_container)
        
        # Nota sobre campos obligatorios
        nota = QLabel("* Campos obligatorios - DNI y Teléfono deben ser numéricos - Email debe contener @")
        nota.setStyleSheet("""
            color: #7f8c8d; 
            font-size: 14px; 
            margin: 25px;
            font-style: italic;
        """)
        nota.setAlignment(Qt.AlignCenter)
        nota.setWordWrap(True)
        layout.addWidget(nota)
        
        self.content_area.addWidget(page)

    def create_search_page(self):
        """Crea la página de búsqueda"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Título
        title = QLabel("Búsqueda de Inscriptos")
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin: 25px; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(80, 25, 80, 25)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre, apellido, DNI o email...")
        self.search_input.setStyleSheet("padding: 15px; font-size: 15px; border: 2px solid #bdc3c7; border-radius: 8px;")
        self.search_input.setMinimumHeight(50)
        
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_inscriptos)
        btn_buscar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 15px 30px;
                font-size: 15px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)
        btn_buscar.setCursor(Qt.PointingHandCursor)
        btn_buscar.setFixedSize(140, 50)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(btn_buscar)
        
        # Tabla de resultados
        self.search_table = QTableWidget()
        self.configurar_tabla(self.search_table)
        
        layout.addLayout(search_layout)
        layout.addWidget(self.search_table)

        self.content_area.addWidget(page)

    def create_list_page(self):
        """Crea la página de listado de inscriptos"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Título
        title = QLabel("Lista de Inscriptos")
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin: 25px; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Controles de ordenamiento
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(80, 15, 80, 15)
        
        btn_ordenar_nombre = QPushButton("Ordenar por Nombre")
        btn_ordenar_apellido = QPushButton("Ordenar por Apellido")
        btn_ordenar_fecha = QPushButton("Ordenar por Fecha")
        
        # Estilo para botones de ordenamiento
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px 18px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        
        for btn in [btn_ordenar_nombre, btn_ordenar_apellido, btn_ordenar_fecha]:
            btn.setStyleSheet(button_style)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(45)
        
        btn_ordenar_nombre.clicked.connect(lambda: self.ordenar_inscriptos('nombre'))
        btn_ordenar_apellido.clicked.connect(lambda: self.ordenar_inscriptos('apellido'))
        btn_ordenar_fecha.clicked.connect(lambda: self.ordenar_inscriptos('fecha_inscripcion'))
        
        control_layout.addWidget(btn_ordenar_nombre)
        control_layout.addWidget(btn_ordenar_apellido)
        control_layout.addWidget(btn_ordenar_fecha)
        control_layout.addStretch()
        
        # Tabla de inscriptos
        self.list_table = QTableWidget()
        self.configurar_tabla(self.list_table)
        
        layout.addLayout(control_layout)
        layout.addWidget(self.list_table)
        
        self.actualizar_lista_inscriptos()
        self.content_area.addWidget(page)

    def configurar_tabla(self, tabla):
        """Configura una tabla para mostrar información completa"""
        tabla.setColumnCount(7)
        tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Apellido", "DNI", "Email", "Teléfono", "Institución"
        ])
        
        # Ajustar el comportamiento de las columnas
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Nombre
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Apellido
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # DNI
        header.setSectionResizeMode(4, QHeaderView.Stretch)           # Email (se expande)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Teléfono
        header.setSectionResizeMode(6, QHeaderView.Stretch)           # Institución (se expande)
        
        # Permitir que el texto se envuelva en las celdas
        tabla.setWordWrap(True)
        tabla.setAlternatingRowColors(True)
        
        # Ajustar altura de las filas para mostrar contenido completo
        tabla.resizeRowsToContents()

    def create_reports_page(self):
        """Crea la página de reportes"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Título
        title = QLabel("Generar Reportes")
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin: 25px; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Contenedor para centrar los botones
        buttons_container = QVBoxLayout()
        buttons_container.setAlignment(Qt.AlignCenter)
        buttons_container.setContentsMargins(150, 100, 150, 100)
        buttons_container.setSpacing(40)
        
        # Botones de reportes
        btn_reporte_total = QPushButton("Generar Reporte Total")
        btn_reporte_instituciones = QPushButton("Reporte por Instituciones")
        
        # Estilo para botones de reportes
        report_button_style = """
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 25px;
                font-size: 17px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """
        
        for btn in [btn_reporte_total, btn_reporte_instituciones]:
            btn.setStyleSheet(report_button_style)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(320, 80)
            buttons_container.addWidget(btn, alignment=Qt.AlignCenter)
        
        btn_reporte_total.clicked.connect(self.generar_reporte_total)
        btn_reporte_instituciones.clicked.connect(self.generar_reporte_instituciones)
        
        layout.addLayout(buttons_container)
        layout.addStretch()
        
        self.content_area.addWidget(page)

    def validar_email(self, email):
        """Valida que el email contenga @"""
        return '@' in email

    def validar_numerico(self, texto):
        """Valida que el texto contenga solo números"""
        return texto.isdigit() if texto else True

    def registrar_participante(self):
        """Registra un nuevo participante en la base de datos con validaciones"""
        nombre = self.nombre_input.text().strip()
        apellido = self.apellido_input.text().strip()
        dni = self.dni_input.text().strip()
        email = self.email_input.text().strip()
        telefono = self.telefono_input.text().strip()
        institucion = self.institucion_input.text().strip()
        
        # Validaciones básicas
        if not all([nombre, apellido, dni, email]):
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos obligatorios")
            return
        
        # Validar email
        if not self.validar_email(email):
            QMessageBox.warning(self, "Error", "El email debe contener el símbolo @")
            self.email_input.setFocus()
            return
        
        # Validar DNI (solo números)
        if not self.validar_numerico(dni):
            QMessageBox.warning(self, "Error", "El DNI debe contener solo números")
            self.dni_input.setFocus()
            return
        
        # Validar teléfono (solo números, si se ingresó)
        if telefono and not self.validar_numerico(telefono):
            QMessageBox.warning(self, "Error", "El teléfono debe contener solo números")
            self.telefono_input.setFocus()
            return
        
        datos = (
            nombre,
            apellido,
            dni,
            email,
            telefono,
            QDate.currentDate().toString("yyyy-MM-dd"),
            institucion
        )
        
        try:
            self.cursor.execute('''
                INSERT INTO inscriptos 
                (nombre, apellido, dni, email, telefono, fecha_inscripcion, institucion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', datos)
            self.conn.commit()
            
            QMessageBox.information(self, "Éxito", "Participante registrado correctamente")
            self.limpiar_formulario()
            self.actualizar_lista_inscriptos()
            
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "El DNI ya está registrado")

    def limpiar_formulario(self):
        """Limpia el formulario de registro"""
        self.nombre_input.clear()
        self.apellido_input.clear()
        self.dni_input.clear()
        self.email_input.clear()
        self.telefono_input.clear()
        self.institucion_input.clear()

    def actualizar_lista_inscriptos(self):
        """Actualiza la tabla de listado de inscriptos"""
        self.cursor.execute('''
            SELECT id, nombre, apellido, dni, email, telefono, institucion 
            FROM inscriptos
        ''')
        datos = self.cursor.fetchall()
        
        self.list_table.setRowCount(len(datos))
        for row, record in enumerate(datos):
            for col, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                # CORRECCIÓN: Eliminar la línea problemática
                self.list_table.setItem(row, col, item)
        
        # Ajustar las filas al contenido
        self.list_table.resizeRowsToContents()

    def buscar_inscriptos(self):
        """Busca inscriptos según el criterio de búsqueda"""
        criterio = f"%{self.search_input.text()}%"
        self.cursor.execute('''
            SELECT id, nombre, apellido, dni, email, telefono, institucion 
            FROM inscriptos 
            WHERE nombre LIKE ? OR apellido LIKE ? OR dni LIKE ? OR email LIKE ?
        ''', (criterio, criterio, criterio, criterio))
        
        resultados = self.cursor.fetchall()
        
        self.search_table.setRowCount(len(resultados))
        for row, record in enumerate(resultados):
            for col, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                # CORRECCIÓN: Eliminar la línea problemática
                self.search_table.setItem(row, col, item)
        
        # Ajustar las filas al contenido
        self.search_table.resizeRowsToContents()

    def ordenar_inscriptos(self, criterio):
        """Ordena la lista de inscriptos según el criterio especificado"""
        self.cursor.execute(f'''
            SELECT id, nombre, apellido, dni, email, telefono, institucion 
            FROM inscriptos 
            ORDER BY {criterio}
        ''')
        datos = self.cursor.fetchall()
        
        self.list_table.setRowCount(len(datos))
        for row, record in enumerate(datos):
            for col, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                # CORRECCIÓN: Eliminar la línea problemática
                self.list_table.setItem(row, col, item)
        
        # Ajustar las filas al contenido
        self.list_table.resizeRowsToContents()

    def generar_reporte_total(self):
        """Genera un reporte general de inscriptos"""
        self.cursor.execute("SELECT COUNT(*) FROM inscriptos")
        total = self.cursor.fetchone()[0]
        
        QMessageBox.information(self, "Reporte Total", 
                               f"Total de inscriptos: {total}")

    def generar_reporte_instituciones(self):
        """Genera un reporte agrupado por instituciones"""
        self.cursor.execute('''
            SELECT institucion, COUNT(*) 
            FROM inscriptos 
            GROUP BY institucion
        ''')
        datos = self.cursor.fetchall()
        
        reporte = "Inscriptos por institución:\n\n"
        for institucion, cantidad in datos:
            reporte += f"{institucion or 'Sin institución'}: {cantidad}\n"
        
        QMessageBox.information(self, "Reporte por Instituciones", reporte)

    def closeEvent(self, event):
        """Cierra la conexión a la base de datos al salir"""
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Estilo moderno
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f8f9fa;
        }
        QTableWidget {
            border: 1px solid #bdc3c7;
            border-radius: 8px;
            background-color: white;
            gridline-color: #bdc3c7;
        }
        QHeaderView::section {
            background-color: #34495e;
            color: white;
            padding: 12px;
            border: none;
            font-size: 13px;
            font-weight: bold;
        }
        QTableWidget::item {
            padding: 10px;
        }
        QTableWidget::item:alternate {
            background-color: #f2f2f2;
        }
    """)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
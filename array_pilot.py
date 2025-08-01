import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QSpinBox, QSlider, QCheckBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
)
from PyQt5.QtGui import QPalette, QColor, QBrush
from PyQt5.QtCore import Qt


def create_hexagonal_array(radius, randomize=False, empty_fraction=0.1, passive=False):
    """
    Creates a hexagonal array with a given radius.

    Parameters:
    radius (int): The radius of the hexagonal array (number of rings around the center).
    randomize (bool): If set to True, inserts random empty cells within the hexagon.
    empty_fraction (float): Fraction of hexagonal cells to leave empty (only if randomize is True).

    Returns:
    np.ndarray: 2D numpy array representing the hexagonal array,
                with empty cells (np.nan) for air and '1' for active cells.
    """
    # Calculate the dimensions of the square that contains the hexagon
    size = 2 * radius + 1
    hex_array = np.full((size, size),np.nan)  # Initialize the array with empty cells (np.nan)

    # Calculate the center position
    center = radius
    cell_positions = []  # List to save the positions of the hexagonal cells

    # Build the hexagon with initial fill
    for i in range(size):
        start = max(0, radius - i)
        end = size - max(0, i - radius)
        hex_array[i, start:end] = 1
        # Add hexagonal cell positions
        cell_positions.extend([(i, j) for j in range(start, end)])

    # If randomize is True, remove random hexagonal cells to create air cells
    if randomize:
        # Determine the number of cells to leave empty
        num_empty_cells = int(len(cell_positions) * empty_fraction)
        empty_positions = np.random.choice(len(cell_positions), num_empty_cells, replace=False)

        # Set selected cells to np.nan
        for idx in empty_positions:
            i, j = cell_positions[idx]
            hex_array[i, j] = 0 if passive else np.nan

    return hex_array



def create_rectangular_array(rows, columns, randomize=False, empty_fraction=0.1, passive=False):
    """
    Creates a rectangular array with specified rows and columns.

    Parameters:
    rows (int): Number of rows in the array.
    columns (int): Number of columns in the array.
    randomize (bool): If set to True, inserts random empty cells within the rectangle.
    empty_fraction (float): Fraction of rectangular cells to leave empty (only if randomize is True).

    Returns:
    np.ndarray: 2D numpy array representing the rectangular array,
                with empty cells (np.nan) for air and '1' for active cells.
    """
    # Initialize the array with active cells (1)
    rect_array = np.ones((rows, columns))

    # If randomize is True, remove random rectangular cells to create air cells
    if randomize:
        # Calculate the total number of cells to leave empty
        num_cells = rows * columns
        num_empty_cells = int(num_cells * empty_fraction)

        # Randomly select positions to set as empty
        empty_positions = np.random.choice(num_cells, num_empty_cells, replace=False)

        # Set selected cells to np.nan
        for pos in empty_positions:
            i, j = divmod(pos, columns)  # Convert 1D position to 2D coordinates
            rect_array[i, j] = 0 if passive else np.nan

    return rect_array

def create_sunflower_array(n_points, radius, grid_size, randomize=False, empty_fraction=0.1, passive=False):
    """
    Creates a 2D sunflower array on a square grid using a Fermat's spiral pattern.

    Parameters:
        n_points (int): Number of points (cells) in the sunflower array.
        radius (float): Radius of the sunflower array.
        grid_size (int): Size of the square grid (grid_size x grid_size).
        randomize (bool): If True, randomly place air gaps within the array.
        empty_fraction (float): Probability of an air gap for each cell if `randomize` is True.

    Returns:
        np.ndarray: A 2D numpy array with cells set to `1` where sunflower pattern points are located,
                    and `None` where empty cells (air gaps) are present.
    """
    # Initialize a 2D array for the grid with `None` values (empty cells)
    grid = np.full((grid_size, grid_size), np.nan)

    # Golden angle in radians for the sunflower pattern
    golden_angle = np.pi * (3 - np.sqrt(5))  # ~137.5 degrees

    # Center of the grid
    center = grid_size // 2

    # Generate each point in the sunflower pattern
    for i in range(n_points):
        # Radius grows with the square root of the index to create the spiral
        r = radius * np.sqrt(i / n_points)
        # Angle increases by the golden angle for each point
        theta = i * golden_angle

        # Convert polar coordinates to Cartesian coordinates
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        # Translate to grid coordinates
        row = int(round(center + y))
        col = int(round(center + x))

        # Check if coordinates are within the grid boundaries
        if 0 <= row < grid_size and 0 <= col < grid_size:
            grid[row, col] = 0 if randomize and np.random.rand() < empty_fraction and passive else 1

        return grid


def create_circular_array(grid_size, radius, randomize=False, empty_fraction=0.1, passive=False):
    """
    Generates a 2D numpy array with a circular pattern, setting cells within the circle to 1
    and empty cells outside to None. If randomize=True, some cells within the circle are
    left empty based on the empty_fraction to simulate air gaps.

    Parameters:
    - grid_size (int): Size of the output square grid (grid_size x grid_size).
    - radius (float): Radius of the circle within the grid.
    - randomize (bool): If True, introduces empty cells randomly within the circle to simulate air gaps.
    - empty_fraction (float): Proportion of cells within the circle to randomly leave empty if randomize=True.

    Returns:
    - numpy.ndarray: A 2D array where cells inside the circle are set to 1,
                     and cells outside are NaN. Random gaps may be added if randomize=True.
    """
    # Initialize grid with None (empty cells)
    grid = np.full((grid_size, grid_size), np.nan)
    center = grid_size // 2  # Define the center of the circular pattern

    for i in range(grid_size):
        for j in range(grid_size):
            # Calculate distance from the center for each cell
            distance = np.sqrt((i - center) ** 2 + (j - center) ** 2)

            # Check if the cell is within the specified radius
            if distance <= radius:
                # Set cell to 1 if within the radius
                if randomize and np.random.rand() < empty_fraction:
                    grid[i, j] = 0 if passive else np.nan  # Leave cell empty for air gaps
                else:
                    grid[i, j] = 1  # Set cell to 1

    return grid


def create_octagonal_array(grid_size, side_length, randomize=False, empty_fraction=0.1, passive=False):
    """
    Generates a 2D numpy array with an octagonal pattern, setting cells within the octagon to 1
    and empty cells outside to None. If randomize=True, some cells within the octagon are
    left empty based on the empty_fraction to simulate air gaps.

    Parameters:
    - grid_size (int): Size of the output square grid (grid_size x grid_size).
    - side_length (float): Length of the side of the octagon (half the width across the flat sides).
    - randomize (bool): If True, introduces empty cells randomly within the octagon to simulate air gaps.
    - empty_fraction (float): Proportion of cells within the octagon to randomly leave empty if randomize=True.

    Returns:
    - numpy.ndarray: A 2D array where cells inside the octagon are set to 1,
                     and cells outside are None. Random gaps may be added if randomize=True.
    """
    # Initialize grid with None (empty cells)
    grid = np.full((grid_size, grid_size), np.nan)
    center = grid_size // 2  # Define the center of the octagonal pattern

    # Define distance thresholds for octagon vertices based on side_length
    max_dist_from_center = side_length * (1 + np.sqrt(2) / 2)

    for i in range(grid_size):
        for j in range(grid_size):
            # Calculate x and y distances from the center
            x_dist = abs(i - center)
            y_dist = abs(j - center)

            # Check if the point is within the octagon bounds
            if x_dist + y_dist <= max_dist_from_center and \
                    max(x_dist, y_dist) <= side_length * np.sqrt(2):

                # Set cell to 1 if within the octagon
                if randomize and np.random.rand() < empty_fraction:
                    grid[i, j] = 0 if passive else np.nan  # Leave cell empty for air gaps
                else:
                    grid[i, j] = 1  # Set cell to 1

    return grid


class ArrayGeneratorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ArrayPilot")
        self.setGeometry(100, 100, 800, 500)

        # Colori della UI
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(47, 47, 47))  
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        # Layout principale
        layout = QHBoxLayout()

        # Sezione di configurazione a sinistra
        config_layout = QVBoxLayout()

        # Array attribute
        self.array = []

        # Dropdown per il tipo di array
        self.array_type_label = QLabel("Select array type:")
        self.array_type_label.setStyleSheet("color: white;")
        self.array_type_combo = QComboBox()
        self.array_type_combo.addItems(["Rectangular", "Circular", "Octagonal", "Hexagonal", "Sunflower"])
        self.array_type_combo.currentIndexChanged.connect(self.update_inputs)

        # Checkbox per `Randomize`
        self.randomize_check = QCheckBox("Randomize")
        self.randomize_check.setStyleSheet("color: white;")
        self.randomize_check.stateChanged.connect(self.toggle_empty_fraction)

        ############################################################
        # Radio button per `Passive Cell` ##########
        self.passive_cell_radio = QCheckBox("Passive Cell")
        self.passive_cell_radio.setStyleSheet("color: white;")
        self.passive_cell_radio.setEnabled(False)  # Disabilitato inizialmente

        #config_layout.addWidget(self.randomize_check)
        #config_layout.addWidget(self.passive_cell_radio)

        ############################################################

        # Label e slider per `empty_fraction` (percentuale)
        self.empty_fraction_label = QLabel("Empty Fraction: 0%")
        self.empty_fraction_label.setStyleSheet("color: white;")  # font-size: 16px;")
        self.empty_fraction_slider = QSlider(Qt.Horizontal)
        self.empty_fraction_slider.setRange(0, 100)
        self.empty_fraction_slider.setValue(0)
        self.empty_fraction_slider.valueChanged.connect(self.update_empty_fraction_label)

        # Nascondi `empty_fraction` inizialmente
        self.empty_fraction_label.hide()
        self.empty_fraction_slider.hide()

        # Campo per selezionare il file `3D Component`
        self.component_label = QLabel("3D Component File:")
        self.component_label.setStyleSheet("color: white;")
        self.component_button = QPushButton("Select File")
        self.component_button.clicked.connect(self.select_3d_component_file)
        self.component_file_path = None

        # Campo per la versione AEDT
        self.version_label = QLabel("AEDT Version:")
        self.version_label.setStyleSheet("color: white;")
        self.version_combo = QComboBox()
        self.version_combo.addItems(["2024.1", "2024.2", "2025.1"])

        # Checkbox per `Non-Graphical Mode`
        self.non_graphical_mode_check = QCheckBox("Non-Graphical Mode")
        self.non_graphical_mode_check.setStyleSheet("color: white;")

        # Form per i parametri specifici dell'array
        self.form_layout = QFormLayout()

        # Bottone di anteprima e bottone di generazione
        self.preview_button = QPushButton("Preview")
        self.preview_button.clicked.connect(self.preview_array)

        self.generate_button = QPushButton("Generate Array")
        self.generate_button.clicked.connect(self.generate_array)

        # Aggiungi elementi al layout di configurazione
        config_layout.addWidget(self.component_label)
        config_layout.addWidget(self.component_button)
        config_layout.addWidget(self.version_label)
        config_layout.addWidget(self.version_combo)
        config_layout.addWidget(self.non_graphical_mode_check)

        config_layout.addWidget(self.array_type_label)
        config_layout.addWidget(self.array_type_combo)
        config_layout.addWidget(self.randomize_check)
        config_layout.addWidget(self.passive_cell_radio)
        config_layout.addWidget(self.empty_fraction_label)
        config_layout.addWidget(self.empty_fraction_slider)

        config_layout.addLayout(self.form_layout)
        config_layout.addWidget(self.preview_button)
        config_layout.addWidget(self.generate_button)

        # Aggiorna i campi di input per il tipo di array iniziale
        self.update_inputs()

        # Vista grafica per l'anteprima dell'array
        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.graphics_scene)

        # Aggiungi layout al layout principale
        layout.addLayout(config_layout)
        layout.addWidget(self.graphics_view)

        # Set main layout
        self.setLayout(layout)

    def toggle_empty_fraction(self):
        # Mostra o nascondi `empty_fraction_label` e `empty_fraction_slider` a seconda dello stato di `randomize_check`
        if self.randomize_check.isChecked():
            self.empty_fraction_label.show()
            self.empty_fraction_slider.show()
            self.passive_cell_radio.setEnabled(True)  # Abilita il radio button
        else:
            self.empty_fraction_label.hide()
            self.empty_fraction_slider.hide()
            self.passive_cell_radio.setEnabled(False)  # Disabilita il radio button
            self.passive_cell_radio.setChecked(False)  # Deseleziona se disabilitato

    def update_empty_fraction_label(self, value):
        # Aggiorna la label per mostrare il valore attuale del `empty_fraction` in percentuale
        self.empty_fraction_label.setText(f"Empty Fraction: {value}%")

    def select_3d_component_file(self):
        # Apri un file dialog per selezionare un file .a3dcomp
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Seleziona un file 3D Component", "",
                                                   "3D Component Files (*.a3dcomp)")

        if file_path:
            self.component_file_path = file_path
            self.component_button.setText(f"Selezionato: {file_path.split('/')[-1]}")

    def update_inputs(self):
        # Rimuovi vecchi campi
        for i in reversed(range(self.form_layout.count())):
            self.form_layout.itemAt(i).widget().deleteLater()

        # Crea nuovamente i widget ogni volta che aggiorniamo gli input
        array_type = self.array_type_combo.currentText()

        # Empty the array attribute
        self.array = []

        if array_type == "Hexagonal":
            self.radius_spin = QSpinBox()
            self.radius_spin.setRange(1, 500)
            self.form_layout.addRow("Radius:", self.radius_spin)

        elif array_type == "Rectangular":
            self.rows_spin = QSpinBox()
            self.rows_spin.setRange(1, 500)
            self.columns_spin = QSpinBox()
            self.columns_spin.setRange(1, 500)
            self.form_layout.addRow("Rows:", self.rows_spin)
            self.form_layout.addRow("Columns:", self.columns_spin)

        elif array_type == "Sunflower":
            self.n_points_spin = QSpinBox()
            self.n_points_spin.setRange(1, 500)
            self.radius_spin = QSpinBox()
            self.radius_spin.setRange(1, 500)
            self.grid_size_spin = QSpinBox()
            self.grid_size_spin.setRange(1, 500)
            self.form_layout.addRow("Number of Points:", self.n_points_spin)
            self.form_layout.addRow("Radius:", self.radius_spin)
            self.form_layout.addRow("Grid Size:", self.grid_size_spin)

        elif array_type == "Circular":
            self.radius_spin = QSpinBox()
            self.radius_spin.setRange(1, 500)
            self.grid_size_spin = QSpinBox()
            self.grid_size_spin.setRange(1, 500)
            self.form_layout.addRow("Radius:", self.radius_spin)
            self.form_layout.addRow("Grid Size:", self.grid_size_spin)

        elif array_type == "Octagonal":
            self.side_length_spin = QSpinBox()
            self.side_length_spin.setRange(1, 500)
            self.grid_size_spin = QSpinBox()
            self.grid_size_spin.setRange(1, 500)
            self.form_layout.addRow("Side Length:", self.side_length_spin)
            self.form_layout.addRow("Grid Size:", self.grid_size_spin)

    def generate_array(self):

        array_type = self.array_type_combo.currentText()
        randomize = self.randomize_check.isChecked()
        empty_fraction = self.empty_fraction_slider.value() / 100  # Decimal conversion
        passive_cell = self.passive_cell_radio.isChecked()

        if len(self.array) == 0:
            # Parametri specifici dell'array
            if array_type == "Hexagonal":
                radius = self.radius_spin.value()
                self.array = create_hexagonal_array(radius, randomize=randomize, empty_fraction=empty_fraction, passive=passive_cell)

            elif array_type == "Rectangular":
                rows = self.rows_spin.value()
                columns = self.columns_spin.value()
                self.array = create_rectangular_array(rows, columns, randomize=randomize, empty_fraction=empty_fraction, passive=passive_cell)

            elif array_type == "Sunflower":
                n_points = self.n_points_spin.value()
                radius = self.radius_spin.value()
                grid_size = self.grid_size_spin.value()
                self.array = create_sunflower_array(n_points, radius, grid_size, randomize=randomize,
                                               air_gap_prob=empty_fraction, passive=passive_cell)
            elif array_type == "Circular":
                radius = self.radius_spin.value()
                grid_size = self.grid_size_spin.value()
                self.array = create_circular_array(grid_size, radius, randomize=randomize,
                                                   empty_fraction=empty_fraction, passive=passive_cell)
            elif array_type == "Octagonal":
                grid_size = self.grid_size_spin.value()
                side_length = self.side_length_spin.value()
                self.array = create_octagonal_array(grid_size, side_length, randomize=randomize,
                                                    empty_fraction=empty_fraction, passive=passive_cell)

        # Parametri AEDT
        aedt_version = self.version_combo.currentText()
        non_graphical_mode = self.non_graphical_mode_check.isChecked()
        #cmp_file = self.component_file_path.currentText()
        cmp_file = self.component_file_path

        # Stampa l'array e le impostazioni AEDT per visualizzare l'output; qui puoi aggiungere il codice per salvare il CSV.
        print(f"3D Component File: {self.component_file_path}")
        print(f"AEDT Version: {aedt_version}, Non-Graphical Mode: {non_graphical_mode}")
        print(self.array)

    def preview_array(self):
        self.graphics_scene.clear()
        array_type = self.array_type_combo.currentText()
        randomize = self.randomize_check.isChecked()
        empty_fraction = self.empty_fraction_slider.value() / 100
        passive_cell = self.passive_cell_radio.isChecked()

        if array_type == "Hexagonal":
            radius = self.radius_spin.value()
            self.array = create_hexagonal_array(radius, randomize=randomize, empty_fraction=empty_fraction, passive=passive_cell)

        elif array_type == "Rectangular":
            rows = self.rows_spin.value()
            columns = self.columns_spin.value()
            self.array = create_rectangular_array(rows, columns, randomize=randomize, empty_fraction=empty_fraction, passive=passive_cell)

        elif array_type == "Sunflower":
            n_points = self.n_points_spin.value()
            radius = self.radius_spin.value()
            grid_size = self.grid_size_spin.value()
            self.array = create_sunflower_array(n_points, radius, grid_size, randomize=randomize,
                                           empty_fraction=empty_fraction, passive=passive_cell)
        elif array_type == "Circular":
            radius = self.radius_spin.value()
            grid_size = self.grid_size_spin.value()
            self.array = create_circular_array(grid_size, radius, randomize=randomize, empty_fraction=empty_fraction, passive=passive_cell)

        elif array_type == "Octagonal":
            grid_size = self.grid_size_spin.value()
            side_length = self.side_length_spin.value()
            self.array = create_octagonal_array(grid_size, side_length, randomize=randomize, empty_fraction=empty_fraction, passive=passive_cell)

        # Disegna anteprima
        for i in range(self.array.shape[0]):
            for j in range(self.array.shape[1]):
                if not np.isnan(self.array[i, j]):
                    if self.array[i, j] == 1:  # Celle attive
                        circle = QGraphicsEllipseItem(j * 10, i * 10, 8, 8)
                        circle.setBrush(QBrush(Qt.red))
                    elif self.array[i, j] == 0:  # Celle passive
                        circle = QGraphicsEllipseItem(j * 10, i * 10, 8, 8)
                        circle.setBrush(QBrush(Qt.blue))
                    self.graphics_scene.addItem(circle)



# Avvio dell'applicazione
app = QApplication(sys.argv)
window = ArrayGeneratorUI()
window.show()
sys.exit(app.exec_())
📡 **ArrayPilot: Interactive Antenna Array Generator for HFSS**

ArrayPilot is an interactive Python tool for generating 2D antenna array geometries of various shapes — rectangular, circular, hexagonal, octagonal, and sunflower — with optional randomization and passive cell definition. It's designed for rapid prototyping and automation of array structures to be imported into ANSYS HFSS.

Built with PyQt5, the tool provides an intuitive GUI for previewing and exporting parametric array definitions.

______________________________________________________________________________________________________________


🚀 **Features**

✅ GUI-based configuration using PyQt5

🔲 Generate arrays in:

  - Rectangular

  - Circular

  - Hexagonal

  - Octagonal

  - Sunflower (Fermat’s spiral)

🎯 Optional random air gaps or passive cells

🔧 AEDT version and non-graphical mode selection

📁 Selection of .a3dcomp 3D Component files

🔎 Live preview of the generated array

🧠 Built-in logic to support passive elements and sparse arrays

______________________________________________________________________________________________________________


🖼️ **Preview**

![ArrayPilot_UI](https://github.com/user-attachments/assets/e854a99e-f414-4add-9749-7ab50c95a12e)

______________________________________________________________________________________________________________


🛠️ **Installation**

1) Clone the repository:

  - git clone https://github.com/NickL88-lab/array-pilot.git

  - cd array-pilot

2) Install dependencies:

  - pip install PyQt5 numpy

______________________________________________________________________________________________________________

▶️ **Usage**

- Run the script
  
- Choose the array type

- Set dimensions and parameters

- Toggle randomization and passive elements if needed

- Select your .a3dcomp file

- Preview the geometry

- Click "Generate Array" to export settings or integrate with HFSS scripting

______________________________________________________________________________________________________________

📂 **Output**

Console output includes:

  - Numpy matrix of the generated array

  - AEDT version and non-graphical mode flags

  - Selected 3D Component path

You can easily extend the generate_array() method to:

  - Save arrays as .csv or .txt

  - Trigger HFSS scripting via pyAEDT or custom macros

______________________________________________________________________________________________________________

⚙️ **Array Encoding Convention**

| Value | Meaning                      |
| ----- | ---------------------------- |
| `1`   | Active antenna cell          |
| `0`   | Passive (non-driven) element |
| `NaN` | Empty (air) region           |

______________________________________________________________________________________________________________

🧠 **Future Work**

  - 💾 Export array to CSV/JSON

  - 🌐 Web version (PySide + Qt for WebAssembly)

  - 💡 Advanced spacing and phase control (for beamforming)

______________________________________________________________________________________________________________

📄 **License**

MIT License — free to use, modify, and share.

______________________________________________________________________________________________________________




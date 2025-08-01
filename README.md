# **ArrayPilot: Interactive Antenna Array Generator for HFSS**

## Overview

ArrayPilot is an interactive Python tool for generating 2D antenna array geometries of various shapes — rectangular, circular, hexagonal, octagonal, and sunflower — with optional randomization and passive cell definition. It's designed for rapid prototyping and automation of array structures to be imported into ANSYS HFSS.

Built with PyQt5, the tool provides an intuitive GUI for previewing and exporting parametric array definitions.


![sparse_array](https://github.com/user-attachments/assets/2d2607cc-f5d9-4350-a23a-b59d5375d1aa)

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/NickL88-lab/array-pilot.git

cd array-pilot

pip install PyQt5 numpy
```

---

## Usage

- Run the script

- Select your .a3dcomp source file 
  
- Choose the array type: supported types are Rectangular, Circular, Hexagonal, Octagonal and Sunflower (Fermat's Spiral)

- Set dimensions and parameters

- Toggle randomization and passive elements if needed. Built-in logic to support passive elements (useful to test elements failures) and sparse arrays

- Live preview of the genrerated array

- Click "Generate Array" to export settings or integrate with HFSS scripting

Console output includes:

  - Numpy matrix of the generated array

  - AEDT version and non-graphical mode flags

  - Selected 3D Component path

You can easily extend the generate_array() method to:

  - Save arrays as .csv or .txt

  - Trigger HFSS scripting via pyAEDT or custom macros

---

## Array Encoding Convention

| Value | Meaning                      |
| ----- | ---------------------------- |
| `1`   | Active antenna cell          |
| `0`   | Passive (non-driven) element |
| `NaN` | Empty (air) region           |

---

## License

MIT License — free to use, modify, and share.

---



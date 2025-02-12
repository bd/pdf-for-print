# Booklet Reorder

Booklet Reorder is a command-line Python tool that rearranges PDF pages for booklet (signature) printing. It reorders pages into signatures according to a predetermined imposition scheme so that when printed double-sided and folded, the pages appear in the correct order for binding.

For example, for an 8-page signature the mapping is as follows:

| **Output (I<n>)** | **Imposition Label** | **Source Page** |
|-------------------|----------------------|-----------------|
| I1                | S1FL                 | Source P8       |
| I2                | S1FR                 | Source P1       |
| I3                | S1BR                 | Source P7       |
| I4                | S1BL                 | Source P2       |
| I5                | S2FL                 | Source P6       |
| I6                | S2FR                 | Source P3       |
| I7                | S2BR                 | Source P5       |
| I8                | S2BL                 | Source P4       |

This ordering is generalized for a signature of _N_ pages (where _N_ is a multiple of 4). In each sheet (0-indexed, with sheet label S{i+1}), the pages are arranged as:  
- **Front Left (FL)** = `sig_pages[N – 1 – 2*i]`  
- **Front Right (FR)** = `sig_pages[2*i]`  
- **Back Right (BR)** = `sig_pages[N – 2 – 2*i]`  
- **Back Left (BL)** = `sig_pages[2*i + 1]`  

The output order per sheet is `[FL, FR, BR, BL]`.

By default, the tool rotates the back pages (BR and BL) 180° so that their orientation is correct for double-sided printing. An optional overlay can be applied that labels each imposed page with its signature and output page number.

---

## Features

- **Customizable Signatures:**  
  Specify the number of pages per signature (default is 20, must be a multiple of 4).

- **Rotation Control:**  
  By default, back pages are rotated 180° to correct orientation. This can be disabled.

- **Optional Imposition Overlay:**  
  Optionally overlay each page with its imposition label and global output page number.

- **Simple Command-Line Interface:**  
  Reorder your PDF with a single command.

---

## Dependencies

- Python 3.x  
- [PyPDF2 3.0.1](https://pypi.org/project/PyPDF2/)  
- [reportlab 4.3.0](https://pypi.org/project/reportlab/)

---

## Installation

1. **Clone the Repository:**

       git clone https://github.com/yourusername/booklet-reorder.git
       cd booklet-reorder

2. **(Optional) Create and Activate a Virtual Environment:**

       python3 -m venv venv
       source venv/bin/activate

3. **Install the Dependencies:**

       pip install PyPDF2==3.0.1 reportlab==4.3.0

---

## Usage

Run the script from the command line:

       python booklet_builder.py input.pdf output.pdf [options]

### Options

- **--pages-per-signature**  
  Number of pages per signature (must be a multiple of 4). Default is 20.

- **--no-rotate-back**  
  Do not rotate back pages (default rotates back pages).

- **--overlay**  
  Enable imposition overlay (labels each imposed page with its signature label and output page number).

### Example

To process `input.pdf` with the default settings:

       python booklet_builder.py input.pdf output.pdf

To enable overlays and use 20 pages per signature:

       python booklet_builder.py input.pdf output.pdf --pages-per-signature 20 --overlay

To disable rotation of back pages:

       python booklet_builder.py input.pdf output.pdf --no-rotate-back

---

## Imposition Scheme

For an 8-page signature, the mapping is as follows:

- **Front Side:**
  - **S1FR (I2):** Source P1
  - **S1BL (I3):** Source P2

- **Back Side:**
  - **S1BR (I4):** Source P7
  - **S1FL (I1):** Source P8

- **Second Sheet (if applicable):**
  - **S2FR (I6):** Source P3
  - **S2BL (I7):** Source P4
  - **S2BR (I8):** Source P5
  - **S2FL (I5):** Source P6

The tool generalizes this ordering for signatures with any number of pages (multiple of 4).

---

## Limitations

- This version of the script applies the same transformation (the front–left transformation) to every imposed page. In a future revision, you may implement different transformations for the FR, BR, and BL positions.
- The script assumes that the input and output page counts are the same.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your improvements.

---

## Contact

For questions or feedback, please contact [Your Name](mailto:your.email@example.com).

Enjoy your booklet printing!
# Quick and Dirty PDF Bookbinding Signature Creation

`booklet_builder.py` is a command-line Python tool that rearranges PDF pages for book printing. It reorders pages into signatures according to a predetermined imposition scheme so that when printed double-sided and folded, the pages appear in the correct order for binding. This is designed to work with a Brother home laser printer, so it's nothing too sophisticated. The reordered PDF will print into foldable signatures correctly if the print settings are 2-up double sided per sheet. It _should_ scale to any paper size, but has only been tested on 8.5x11. Likewise it should work for signatures with pages in any multiple of four, but has only been tested on signatures of 8, 16, and 20 pages (2, 4, and 5 printed sheets, respectively). 

## Terminology and Workflow

### Terms:
- Source: the PDF you want to print
- Output: the PDF you have reordered for printing
- Page: a single source page in the PDF. Not to be confused with a "Sheet". There will be 4 pages per Sheet, and N Sheets per Signature
- Signature: bookbinding term for the collection of Sheets which will be folded and bound into a book. There will typically be multiple signatures per book. Otherwise it's just a booklet
- Imposition: the new ordering of Pages
- Sheet: a single printed page. It will contain 4 pages and be folded in half along with _N - 1_ other sheets to produce a signature. Not to be confused with a Page. 
  
### Workflow: 
1. Run the script on your PDF. Setting the signature size too high will make folding unwieldy, while setting it too low will make binding a bit more work. 
2. Print a test: print 1 Signature from the Output. In my printer, this means printing pages from 1 to N where N is the number of pages per signature.
  a. Settings should be 2-up Double Sided, meaning you will have 4 Pages per Sheet.
  b. The flow should be Left-to-right, top-to-bottom, with Auto-rotate on. Other flows will not work right. I guess I could support them, but there's not much
reason for that now.
  c. fold the signature and confirm the page ordering and orientation.
4. Print the full Output.  
5. Count out the sheets into Signatures, i.e. number of Pages per signature divided by 4. Maintain the order as you do!
6. Fold each Signature in half, maintaining order.
7. Stack and bind Signatures. For my purposes, it's usually enough to use binder clips. Much beyond that and we should start using real typsetting technology.


## Features

- **Customizable Signatures:**  
  Specify the number of pages per signature (default is 20, must be a multiple of 4). So, for example, 20 pages per signature means 5 sheets per signature (20/4 == 5). 

- **Rotation Control:**  
  By default, back pages are rotated 180° to correct orientation. This can be disabled. My setup requires this with the Auto-rotate print setting. It hasn't been tested _without_ that setting. 

- **Optional Imposition Overlay:**  
  Optionally overlay each page with its imposition label and global output page number for debugging and sorting.

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

       pip install -r requirements.txt

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

## License

None. No Warranty. Use at your own risk.

---

## Contributing

Contributions are welcome, I suppose. Open an issue or submit a pull request with your improvements. I would be shocked if you did...


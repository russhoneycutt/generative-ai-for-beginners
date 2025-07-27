# Invoice Extraction Example

This folder contains a minimal example for building an invoice extraction
service. It demonstrates how a Python web app can accept uploaded PDFs or
scanned images and attempt to convert them into a comma separated format
that matches the fields required for QuickBooks import.

The example relies on open-source tools such as **Flask**, **pdf2image** and
**pytesseract** for processing files. A simple JSON based template system is
used to recognise invoice formats. When a new invoice layout is uploaded a
corresponding template can be added, allowing the parser to learn from
previous examples.

## Files

- `app.py` – minimal Flask application exposing endpoints for uploading
  invoices and exporting the parsed data.
- `parser.py` – helper functions for extracting text from PDF or image files
  and parsing invoice fields using regular expressions.
- `templates.json` – storage for template patterns that the parser uses to
  recognise invoices. New templates can be added to extend support for new
  layouts.

## Usage

Install the required Python packages (Flask, pdf2image, Pillow,
pytesseract, pandas). The `tesseract` OCR engine must also be installed on
your system.

```bash
pip install flask pdf2image pytesseract Pillow pandas
```

Run the server:

```bash
python app.py
```

Open a browser to `http://localhost:5000` to upload an invoice. Parsed data
will be displayed on the page and can be exported as CSV.

This example is intentionally simplified. Real world invoice processing may
require more advanced machine learning models and data validation.

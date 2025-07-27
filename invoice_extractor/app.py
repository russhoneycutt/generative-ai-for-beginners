from pathlib import Path
from flask import Flask, request, render_template_string, send_file
import pandas as pd

from parser import load_templates, extract_text, parse_invoice, invoice_to_dataframe

app = Flask(__name__)

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

HTML = """
<!doctype html>
<title>Invoice Uploader</title>
<h1>Upload Invoice</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=invoice>
  <input type=submit value=Upload>
</form>
{% if table %}
<h2>Parsed Data</h2>
{{ table | safe }}
<a href="/download/{{ csv_name }}">Download CSV</a>
{% endif %}
"""


@app.route("/", methods=["GET", "POST"])
def upload_invoice():
    table_html = None
    csv_name = None
    if request.method == "POST":
        file = request.files["invoice"]
        path = UPLOAD_FOLDER / file.filename
        file.save(path)

        templates = load_templates()
        template = templates.get("default", {})
        text = extract_text(path)
        info = parse_invoice(text, template)
        df = invoice_to_dataframe(info, file.filename)
        csv_name = file.filename + ".csv"
        csv_path = UPLOAD_FOLDER / csv_name
        df.to_csv(csv_path, index=False)
        table_html = df.to_html(index=False)
    return render_template_string(HTML, table=table_html, csv_name=csv_name)


@app.route("/download/<name>")
def download_csv(name: str):
    csv_path = UPLOAD_FOLDER / name
    if csv_path.exists():
        return send_file(csv_path, as_attachment=True)
    return "File not found", 404


if __name__ == "__main__":
    app.run(debug=True)

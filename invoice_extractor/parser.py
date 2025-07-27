import json
import re
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

import pandas as pd

try:
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependencies
    convert_from_path = None
    pytesseract = None
    Image = None

TEMPLATE_FILE = Path(__file__).with_name("templates.json")


def load_templates() -> Dict[str, Dict[str, str]]:
    if TEMPLATE_FILE.exists():
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_templates(data: Dict[str, Dict[str, str]]) -> None:
    with open(TEMPLATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def extract_text(filepath: Path) -> str:
    """Extract text from a PDF or image file using tesseract."""
    if filepath.suffix.lower() == ".pdf" and convert_from_path:
        images = convert_from_path(str(filepath))
        text = "\n".join(pytesseract.image_to_string(img) for img in images)
        return text
    else:
        img = Image.open(filepath)
        return pytesseract.image_to_string(img)


def parse_invoice(text: str, template: Dict[str, str]) -> Dict[str, Any]:
    data = {}
    for field, pattern in template.items():
        match = re.search(pattern, text, re.IGNORECASE)
        data[field] = match.group(1).strip() if match else ""
    return data


def invoice_to_dataframe(info: Dict[str, Any], filename: str) -> pd.DataFrame:
    fields = [
        "original_filename", "invoice_amount", "invoice_number", "seller_name",
        "currency", "po_number", "invoice_date", "total_tax", "net_d", "subtotal",
        "payment_due_date", "payto_name", "total_due_amount", "Quantity",
        "Description", "Product_Code", "Line_Amount", "Price"
    ]
    row = {k: "" for k in fields}
    row.update(info)
    row["original_filename"] = filename
    return pd.DataFrame([row])


def train_template(name: str, patterns: Dict[str, str]) -> None:
    templates = load_templates()
    templates[name] = patterns
    save_templates(templates)

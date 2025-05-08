from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
from PyPDF2 import PdfMerger
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_invoice(data, filepath):
    c = canvas.Canvas(filepath, pagesize=A4)
    c.drawString(100, 800, f"Name: {data.get('name')}")
    c.drawString(100, 780, f"Email: {data.get('email')}")
    c.drawString(100, 760, f"Payment Type: {data.get('paymentType')}")
    c.drawString(100, 740, f"Description: {data.get('description')}")
    c.drawString(100, 720, f"Quantity: {data.get('quantity')}")
    c.drawString(100, 700, f"Amount: {data.get('amount')}")
    c.drawString(100, 680, "Supporting Document Attached Below")
    c.save()

def merge_pdfs(invoice_path, support_path, output_path):
    merger = PdfMerger()
    merger.append(invoice_path)
    merger.append(support_path)
    merger.write(output_path)
    merger.close()

@app.route('/handle-form', methods=['POST'])
def handle_form():
    data = request.form
    file = request.files.get('supportingDoc')

    invoice_path = os.path.join(UPLOAD_FOLDER, "invoice.pdf")
    support_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    merged_path = os.path.join(UPLOAD_FOLDER, "merged.pdf")

    file.save(support_path)
    generate_invoice(data, invoice_path)
    merge_pdfs(invoice_path, support_path, merged_path)

    return send_file(merged_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

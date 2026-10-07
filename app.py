from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
CORS(app)  # Allows GitHub Pages frontend to communicate with API

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.json or {}
    
    team_name = data.get('teamName', 'N/A')
    team_leader = data.get('teamLeader', 'N/A')

    # Create PDF directly in memory buffer (Zero disk/drive storage)
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    # PDF Content Drawing
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(100, 750, "Operating Systems Project Proposal")
    
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 710, f"Team Name: {team_name}")
    pdf.drawString(100, 690, f"Team Leader: {team_leader}")
    
    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"Team_{team_name}.pdf",
        mimetype='application/pdf'
    )

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
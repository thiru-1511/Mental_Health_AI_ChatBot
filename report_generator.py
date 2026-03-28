from fpdf import FPDF
import datetime

class ReportGenerator:
    def generate_medical_report(self, appointment, user, output_path):
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", 'B', 20)
        pdf.set_text_color(40, 44, 52)
        pdf.cell(0, 15, "Medical Consultation Report", ln=True, align='C')
        pdf.ln(5)
        
        # Header Line
        pdf.set_draw_color(0, 123, 255)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(10)
        
        # Patient Info
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "Patient Information", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(40, 8, f"Name: {user.get('full_name', 'N/A')}")
        pdf.cell(40, 8, f"Age: {user.get('age', 'N/A')}")
        pdf.cell(0, 8, f"Gender: {user.get('gender', 'N/A')}", ln=True)
        pdf.cell(0, 8, f"Patient ID: {user.get('id', 'N/A')}", ln=True)
        pdf.ln(5)
        
        # Doctor Info
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Consultation Details", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 8, f"Doctor: {appointment.get('doctor_name', 'N/A')}", ln=True)
        pdf.cell(0, 8, f"Specialization: {appointment.get('specialization', 'N/A')}", ln=True)
        pdf.cell(0, 8, f"Date: {appointment.get('date', 'N/A')}", ln=True)
        pdf.cell(0, 8, f"Time: {appointment.get('time', 'N/A')}", ln=True)
        pdf.cell(0, 8, f"Consultation Type: {appointment.get('type', 'Online')}", ln=True)
        pdf.ln(5)
        
        # Diagnosis/Notes
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Consultation Notes", ln=True)
        pdf.set_font("Arial", '', 12)
        notes = appointment.get('notes', 'No notes provided.')
        pdf.multi_cell(0, 8, notes)
        pdf.ln(5)
        
        # Prescription
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Prescriptions", ln=True)
        pdf.set_font("Arial", 'I', 12)
        prescription = appointment.get('prescription', 'No prescription provided.')
        pdf.multi_cell(0, 8, prescription)
        pdf.ln(15)
        
        # Footer
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 10, f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align='C')
        
        pdf.output(output_path)
        return output_path

report_generator = ReportGenerator()

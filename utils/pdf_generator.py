from fpdf import FPDF
import os
from datetime import datetime


class CropSensePDF(FPDF):
    def header(self):
        self.set_fill_color(10, 22, 40)
        self.rect(0, 0, 210, 30, 'F')
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(76, 175, 80)
        self.set_xy(10, 8)
        self.cell(0, 10, 'FarmOS Analytics Report', ln=True)
        self.set_font('Helvetica', '', 9)
        self.set_text_color(168, 213, 162)
        self.set_x(10)
        self.cell(0, 6, f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", ln=True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 150, 100)
        self.cell(0, 10, f'FarmOS v4.0 | Page {self.page_no()}', align='C')

    def section_title(self, title):
        self.set_fill_color(15, 33, 55)
        self.set_text_color(76, 175, 80)
        self.set_font('Helvetica', 'B', 13)
        self.cell(0, 10, title, ln=True, fill=True)
        self.ln(2)

    def stat_row(self, label, value):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(50, 50, 50)
        self.cell(70, 8, f"{label}:", border=0)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(27, 94, 32)
        self.cell(0, 8, str(value), ln=True)


def _pdf_safe(text):
    """
    fpdf2's built-in Helvetica font only supports Latin-1 characters.
    Replace common Unicode punctuation with ASCII equivalents, then drop
    anything else that's still unsupported, so PDF generation never breaks
    on text that displays fine on the (Unicode-safe) web page.
    """
    if text is None:
        return ""
    text = str(text)
    replacements = {
        "—": "-", "–": "-", "’": "'", "‘": "'", "“": '"', "”": '"',
        "…": "...", "₹": "Rs.", "°": " deg",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "ignore").decode("latin-1")


def generate_fertilizer_report(crop, plan):
    """
    Generates a printable PDF fertilizer plan for one crop + area.
    plan: the dict returned by utils.fertilizer_data.get_fertilizer_plan()
    """
    pdf = CropSensePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.section_title(_pdf_safe(f'Fertilizer Plan - {crop}'))
    pdf.stat_row('Crop', _pdf_safe(crop))
    pdf.stat_row('Area', f"{plan['area_acres']} Acres ({plan['area_ha']} Hectares)")
    pdf.stat_row('Season(s)', _pdf_safe(plan.get('seasons', '-')))
    pdf.stat_row('Seed Required', f"{plan['seed_total']} kg")
    pdf.stat_row('Row Spacing', _pdf_safe(plan.get('spacing', '-')))
    pdf.ln(4)

    pdf.section_title('Total NPK Required')
    npk = plan['npk_total']
    pdf.stat_row('Nitrogen (N)', f"{npk['N']} kg")
    pdf.stat_row('Phosphorus (P)', f"{npk['P']} kg")
    pdf.stat_row('Potassium (K)', f"{npk['K']} kg")
    pdf.ln(4)

    pdf.section_title('Fertilizer Application Plan')
    headers = ['Fertilizer', 'Per Hectare', 'Total Qty', 'Bags (50kg)', 'Timing']
    widths  = [35, 30, 30, 30, 65]
    pdf.set_fill_color(76, 175, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 9)
    for h, w in zip(headers, widths):
        pdf.cell(w, 8, h, border=1, fill=True)
    pdf.ln()

    pdf.set_text_color(30, 30, 30)
    pdf.set_font('Helvetica', '', 9)
    for i, f in enumerate(plan['fertilizers']):
        fill = i % 2 == 0
        pdf.set_fill_color(240, 255, 240) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(35, 7, _pdf_safe(f['name']), border=1, fill=fill)
        pdf.cell(30, 7, f"{f['per_ha']} kg/ha", border=1, fill=fill)
        pdf.cell(30, 7, f"{f['total_kg']} kg", border=1, fill=fill)
        pdf.cell(30, 7, f"~{f['bags_50kg']}", border=1, fill=fill)
        pdf.cell(65, 7, _pdf_safe(f['timing'])[:38], border=1, fill=fill)
        pdf.ln()

    if plan.get('tips'):
        pdf.ln(4)
        pdf.section_title('Expert Tip')
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 7, _pdf_safe(plan['tips']))

    pdf.ln(4)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(0, 6, "Source: ICAR (Indian Council of Agricultural Research) recommendations. "
                          "Local soil test ke baad quantities adjust karein.")

    output_dir = os.path.join('static', 'charts')
    os.makedirs(output_dir, exist_ok=True)
    safe_crop = "".join(c for c in crop if c.isalnum()) or "crop"
    output_path = os.path.join(output_dir, f'fertilizer_{safe_crop}.pdf')
    pdf.output(output_path)
    return output_path


def generate_farmer_report(user_id, user_name, stats, recent_crops, predictions, charts_dir=None):
    pdf = CropSensePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.section_title('Farmer Overview')
    pdf.stat_row('Farmer Name', user_name)
    pdf.stat_row('Total Records', stats.get('total_records', 0))
    pdf.stat_row('Avg Yield (t/ha)', stats.get('avg_yield', 'N/A'))
    pdf.stat_row('Total Predictions', stats.get('total_predictions', 0))
    pdf.ln(5)

    if recent_crops:
        pdf.section_title('Recent Crop Data')
        headers = ['Crop', 'Season', 'Year', 'Area (ha)', 'Yield (t/ha)']
        widths  = [40, 35, 25, 35, 35]
        pdf.set_fill_color(76, 175, 80)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Helvetica', 'B', 9)
        for h, w in zip(headers, widths):
            pdf.cell(w, 8, h, border=1, fill=True)
        pdf.ln()

        pdf.set_text_color(30, 30, 30)
        pdf.set_font('Helvetica', '', 9)
        for i, row in enumerate(recent_crops[:15]):
            fill = i % 2 == 0
            pdf.set_fill_color(240, 255, 240) if fill else pdf.set_fill_color(255, 255, 255)
            pdf.cell(40, 7, str(getattr(row, 'crop', '')), border=1, fill=fill)
            pdf.cell(35, 7, str(getattr(row, 'season', '')), border=1, fill=fill)
            pdf.cell(25, 7, str(getattr(row, 'crop_year', '')), border=1, fill=fill)
            pdf.cell(35, 7, str(round(getattr(row, 'area', 0) or 0, 2)), border=1, fill=fill)
            pdf.cell(35, 7, str(round(getattr(row, 'yield_per_hectare', 0) or 0, 2)), border=1, fill=fill)
            pdf.ln()

    if predictions:
        pdf.ln(4)
        pdf.section_title('Recent Predictions')
        ph = ['Crop', 'Season', 'Predicted Yield (t/ha)', 'Confidence']
        pw = [45, 35, 60, 40]
        pdf.set_fill_color(76, 175, 80)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Helvetica', 'B', 9)
        for h, w in zip(ph, pw):
            pdf.cell(w, 8, h, border=1, fill=True)
        pdf.ln()

        pdf.set_text_color(30, 30, 30)
        pdf.set_font('Helvetica', '', 9)
        for i, p in enumerate(predictions[:10]):
            fill = i % 2 == 0
            pdf.set_fill_color(240, 255, 240) if fill else pdf.set_fill_color(255, 255, 255)
            pdf.cell(45, 7, str(getattr(p, 'crop', '')), border=1, fill=fill)
            pdf.cell(35, 7, str(getattr(p, 'season', '')), border=1, fill=fill)
            pdf.cell(60, 7, str(round(getattr(p, 'predicted_yield', 0) or 0, 2)), border=1, fill=fill)
            conf = getattr(p, 'confidence', 0) or 0
            pdf.cell(40, 7, f"{int(conf * 100)}%", border=1, fill=fill)
            pdf.ln()

    if charts_dir and os.path.exists(charts_dir):
        chart_files = [f for f in os.listdir(charts_dir) if f.endswith('.png')]
        if chart_files:
            pdf.add_page()
            pdf.section_title('Analytics Charts')
            x_pos = [10, 110]
            y_start = pdf.get_y()
            for i, cf in enumerate(chart_files[:4]):
                path = os.path.join(charts_dir, cf)
                x = x_pos[i % 2]
                y = y_start if i < 2 else y_start + 75
                try:
                    pdf.image(path, x=x, y=y, w=90)
                except Exception:
                    pass

    # FIX: save to static/charts/ relative to cwd (not relative to this file's dir)
    output_dir = os.path.join('static', 'charts')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'report_{user_id}.pdf')
    pdf.output(output_path)
    return f"charts/report_{user_id}.pdf"

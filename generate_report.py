from PIL import Image, ImageDraw, ImageFont
import os

# Create a blank white image
img = Image.new('RGB', (800, 1000), color=(255, 255, 255))
d = ImageDraw.Draw(img)

# Try to load a font, otherwise use default
try:
    font_title = ImageFont.truetype("arial.ttf", 24)
    font_header = ImageFont.truetype("arial.ttf", 16)
    font_body = ImageFont.truetype("arial.ttf", 14)
    font_bold = ImageFont.truetype("arialbd.ttf", 14)
except IOError:
    font_title = ImageFont.load_default()
    font_header = ImageFont.load_default()
    font_body = ImageFont.load_default()
    font_bold = ImageFont.load_default()

# Header
d.text((50, 50), "PATHOLOGY AND LABORATORY REPORT", fill=(0, 0, 0), font=font_title)
d.text((50, 90), "Patient Name: Jane Doe", fill=(0, 0, 0), font=font_header)
d.text((50, 110), "DOB: 05/12/1980   |   MRN: 987654321", fill=(0, 0, 0), font=font_header)
d.text((50, 130), "Date Collected: 03/08/2026", fill=(0, 0, 0), font=font_header)

d.line([(50, 160), (750, 160)], fill=(0, 0, 0), width=2)

# Content - Section 1
d.text((50, 180), "COMPLETE BLOOD COUNT (CBC)", fill=(0, 0, 0), font=font_bold)
d.text((50, 210), "Test", fill=(100, 100, 100), font=font_bold)
d.text((300, 210), "Result", fill=(100, 100, 100), font=font_bold)
d.text((450, 210), "Units", fill=(100, 100, 100), font=font_bold)
d.text((600, 210), "Reference Range", fill=(100, 100, 100), font=font_bold)

d.line([(50, 230), (750, 230)], fill=(200, 200, 200), width=1)

d.text((50, 240), "White Blood Cell (WBC)", fill=(0, 0, 0), font=font_body)
d.text((300, 240), "6.8", fill=(0, 0, 0), font=font_body)
d.text((450, 240), "x10^3/uL", fill=(0, 0, 0), font=font_body)
d.text((600, 240), "3.8 - 10.8", fill=(0, 0, 0), font=font_body)

d.text((50, 270), "Red Blood Cell (RBC)", fill=(0, 0, 0), font=font_body)
d.text((300, 270), "4.10", fill=(0, 0, 0), font=font_body)
d.text((450, 270), "x10^6/uL", fill=(0, 0, 0), font=font_body)
d.text((600, 270), "3.80 - 5.10", fill=(0, 0, 0), font=font_body)

d.text((50, 300), "Hemoglobin", fill=(255, 0, 0), font=font_bold) # Abnormal
d.text((300, 300), "11.2 (L)", fill=(255, 0, 0), font=font_bold)
d.text((450, 300), "g/dL", fill=(0, 0, 0), font=font_body)
d.text((600, 300), "11.7 - 15.5", fill=(0, 0, 0), font=font_body)

d.text((50, 330), "Platelet Count", fill=(0, 0, 0), font=font_body)
d.text((300, 330), "245", fill=(0, 0, 0), font=font_body)
d.text((450, 330), "x10^3/uL", fill=(0, 0, 0), font=font_body)
d.text((600, 330), "140 - 400", fill=(0, 0, 0), font=font_body)


# Content - Section 2
d.text((50, 400), "COMPREHENSIVE METABOLIC PANEL (CMP)", fill=(0, 0, 0), font=font_bold)
d.text((50, 430), "Test", fill=(100, 100, 100), font=font_bold)
d.text((300, 430), "Result", fill=(100, 100, 100), font=font_bold)
d.text((450, 430), "Units", fill=(100, 100, 100), font=font_bold)
d.text((600, 430), "Reference Range", fill=(100, 100, 100), font=font_bold)

d.line([(50, 450), (750, 450)], fill=(200, 200, 200), width=1)

d.text((50, 460), "Glucose", fill=(0, 0, 0), font=font_body)
d.text((300, 460), "95", fill=(0, 0, 0), font=font_body)
d.text((450, 460), "mg/dL", fill=(0, 0, 0), font=font_body)
d.text((600, 460), "65 - 99", fill=(0, 0, 0), font=font_body)

d.text((50, 490), "AST (SGOT)", fill=(255, 0, 0), font=font_bold) # Abnormal
d.text((300, 490), "61 (H)", fill=(255, 0, 0), font=font_bold)
d.text((450, 490), "U/L", fill=(0, 0, 0), font=font_body)
d.text((600, 490), "10 - 40", fill=(0, 0, 0), font=font_body)

d.text((50, 520), "ALT (SGPT)", fill=(0, 0, 0), font=font_body)
d.text((300, 520), "52", fill=(0, 0, 0), font=font_body)
d.text((450, 520), "U/L", fill=(0, 0, 0), font=font_body)
d.text((600, 520), "7 - 56", fill=(0, 0, 0), font=font_body)


# Content - Section 3 (Tumor Markers)
d.text((50, 590), "ONCOLOGY MARKERS / SPECIAL CHEMISTRY", fill=(0, 0, 0), font=font_bold)
d.line([(50, 610), (750, 610)], fill=(200, 200, 200), width=1)

d.text((50, 620), "CA 15-3 (Breast Tumor Marker)", fill=(0, 0, 0), font=font_body)
d.text((300, 620), "28.5", fill=(0, 0, 0), font=font_body)
d.text((450, 620), "U/mL", fill=(0, 0, 0), font=font_body)
d.text((600, 620), "0.0 - 30.0", fill=(0, 0, 0), font=font_body)

d.text((50, 650), "CEA", fill=(0, 0, 0), font=font_body)
d.text((300, 650), "4.2", fill=(0, 0, 0), font=font_body)
d.text((450, 650), "ng/mL", fill=(0, 0, 0), font=font_body)
d.text((600, 650), "0.0 - 5.0", fill=(0, 0, 0), font=font_body)

d.text((50, 680), "Ki-67 Proliferation Index", fill=(255, 0, 0), font=font_bold) # Abnormal
d.text((300, 680), "22%", fill=(255, 0, 0), font=font_bold)
d.text((450, 680), "%", fill=(0, 0, 0), font=font_body)
d.text((600, 680), "< 14.0", fill=(0, 0, 0), font=font_body)


# Footer notes
d.line([(50, 850), (750, 850)], fill=(0, 0, 0), width=1)
d.text((50, 860), "* Note: (H) indicates High, (L) indicates Low compared to reference range.", fill=(100, 100, 100), font=font_body)
d.text((50, 880), "Electronically Signed by: Dr. Sarah Jenkins, MD, PhD Pathology", fill=(100, 100, 100), font=font_body)

# Save
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
filepath = os.path.join(desktop, "sample_pathology_report.png")
img.save(filepath)
print(f"Saved to {filepath}")

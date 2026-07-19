from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

OUT = Path(r"C:\Users\DELL\Documents\Codex\2026-07-19\h\outputs")
PDF = OUT / "Madan_R_Sangur_Resume.pdf"
W, H = letter
LEFT, RIGHT, TOP = 47, W - 47, H - 39
INK = HexColor("#161B22")
MUTED = HexColor("#4B5563")


def wrap(text, font, size, width):
    words, result, line = text.split(), [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if stringWidth(candidate, font, size) <= width:
            line = candidate
        else:
            result.append(line)
            line = word
    if line:
        result.append(line)
    return result


def write(c, text, x, y, font="Helvetica", size=9.1, color=INK):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, text)


def paragraph(c, text, y, size=9.1, leading=10.4):
    lines = wrap(text, "Helvetica", size, RIGHT - LEFT - 13)
    c.setFillColor(INK)
    c.setFont("Helvetica", size)
    for line in lines:
        c.circle(LEFT + 2.5, y + 2.2, 1.1, fill=1, stroke=0)
        c.drawString(LEFT + 10, y, line)
        y -= leading
    return y


def title(c, text, y):
    y -= 12
    write(c, text.upper(), LEFT, y, "Helvetica-Bold", 9.1)
    return y - 12


def project(c, name, sub, bullets, y):
    write(c, name, LEFT, y, "Helvetica-Bold", 9.6)
    x = LEFT + stringWidth(name, "Helvetica-Bold", 9.6)
    write(c, " | " + sub, x, y, "Helvetica", 8.8, MUTED)
    y -= 11.5
    for item in bullets:
        y = paragraph(c, item, y, 8.85, 10.5) - 2
    return y - 2


c = canvas.Canvas(str(PDF), pagesize=letter, pageCompression=1)
c.setTitle("Madan R. Sangur Resume")
c.setAuthor("Madan R. Sangur")
y = TOP
write(c, "Madan R. Sangur", LEFT, y, "Helvetica-Bold", 20)
y -= 17
write(c, "AI/ML Engineer | B.Tech Artificial Intelligence & Machine Learning Student", LEFT, y, "Helvetica-Bold", 9.5, MUTED)
y -= 14
contact = "Haveri, Karnataka, India | +91 93803 50086 | madansangur@gmail.com | linkedin.com/in/madan-sangur-075772275 | github.com/madan-sangur"
write(c, contact, LEFT, y, "Helvetica", 8.15, MUTED)
y -= 5

y = title(c, "Summary", y)
y = paragraph(c, "Apply Python, TensorFlow, Keras, and data tooling to build machine learning prototypes and practical AI product concepts.", y)
y = paragraph(c, "Focus on AI/ML and data-focused internship opportunities where strong fundamentals and hands-on project work can create useful outcomes.", y) - 1

y = title(c, "Projects", y)
y = project(c, "ArcLife", "AI-powered life management platform | In development", [
    "Design a unified experience for planning, habit tracking, journaling, and personal growth.",
    "Explore AI-assisted guidance and personalized workflows that support consistent routines."
], y)
y = project(c, "NeuroPlay", "Python, ML | Code Meet 2025 Hackathon", [
    "Designed and prototyped adaptive learning paths from diagnostic responses and aptitude patterns.",
    "Applied ML concepts to categorize aptitude and tailor subject matter for individual learners."
], y)
y = project(c, "Image Classification Model", "Python, TensorFlow, Keras", [
    "Developed and optimized a convolutional neural network that achieved approximately 98% validation accuracy."
], y)
y = project(c, "Student Record System", "C, file handling, data structures", [
    "Built a console-based record-management application using file handling and core data-structure concepts."
], y)

y = title(c, "Skills", y)
write(c, "Programming: ", LEFT, y, "Helvetica-Bold", 8.85)
x = LEFT + stringWidth("Programming: ", "Helvetica-Bold", 8.85)
write(c, "Python, C, Java (OOP), HTML, CSS, JavaScript", x, y, "Helvetica", 8.85)
x += stringWidth("Python, C, Java (OOP), HTML, CSS, JavaScript", "Helvetica", 8.85)
write(c, " | ML & Data: ", x, y, "Helvetica-Bold", 8.85)
x += stringWidth(" | ML & Data: ", "Helvetica-Bold", 8.85)
write(c, "TensorFlow, Keras, Pandas, NumPy, Machine Learning, Deep Learning", x, y, "Helvetica", 8.85)
y -= 10.5
write(c, "Tools: ", LEFT, y, "Helvetica-Bold", 8.85)
write(c, "Git, GitHub, MySQL (RDBMS), AWS (Basics), Data Visualization", LEFT + stringWidth("Tools: ", "Helvetica-Bold", 8.85), y, "Helvetica", 8.85)
y -= 2

y = title(c, "Education", y)
write(c, "B.Tech in Artificial Intelligence & Machine Learning", LEFT, y, "Helvetica-Bold", 9.4)
write(c, " | Srinivas University Institute of Engineering Technology, Mukka", LEFT + stringWidth("B.Tech in Artificial Intelligence & Machine Learning", "Helvetica-Bold", 9.4), y, "Helvetica", 8.75, MUTED)
y -= 10.5
write(c, "Expected 2027 | CGPA: 6.5/10 (after 4th semester) | Coursework: Algorithms & Data Structures, Linear Algebra, OOP, Cloud Computing Fundamentals", LEFT, y, "Helvetica", 8.45, MUTED)
y -= 2

y = title(c, "Certifications", y)
cert = "Data Visualization, IBM Developer Skills Network (2024) | RDBMS, IBM Developer Skills Network (2024) | Machine Learning, Ethnotech Academic Solutions (2024)"
for line in wrap(cert, "Helvetica", 8.55, RIGHT - LEFT):
    write(c, line, LEFT, y, "Helvetica", 8.55)
    y -= 10

if y < 38:
    raise RuntimeError(f"Content overflowed the page (y={y}).")
c.save()
print(PDF)

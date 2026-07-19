from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

OUT = Path(r"C:\Users\DELL\Documents\Codex\2026-07-19\h\outputs")
PDF = OUT / "Madan_R_Sangur_Resume.pdf"

W, H = letter
LEFT, RIGHT, TOP = 42, W - 42, H - 38
INK = HexColor("#172033")
BLUE = HexColor("#2E5EAA")
SLATE = HexColor("#485363")
LINE = HexColor("#D8DEE8")


def wrap(text, font, size, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        next_line = f"{line} {word}".strip()
        if stringWidth(next_line, font, size) <= width:
            line = next_line
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_lines(c, lines, x, y, font="Helvetica", size=9.1, leading=11, color=INK):
    c.setFont(font, size)
    c.setFillColor(color)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def section(c, title, y):
    y -= 11
    c.setFont("Helvetica-Bold", 8.6)
    c.setFillColor(BLUE)
    c.drawString(LEFT, y, title.upper())
    y -= 4
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.line(LEFT, y, RIGHT, y)
    return y - 10


def rich_line(c, x, y, parts, size=9.1):
    cursor = x
    for text, font, color in parts:
        c.setFont(font, size)
        c.setFillColor(color)
        c.drawString(cursor, y, text)
        cursor += stringWidth(text, font, size)


def project(c, y, title, subtitle, bullets):
    rich_line(c, LEFT, y, [(title, "Helvetica-Bold", INK), ("  |  " + subtitle, "Helvetica-Oblique", SLATE)], 9.5)
    y -= 11
    for bullet in bullets:
        lines = wrap(bullet, "Helvetica", 8.8, RIGHT - LEFT - 15)
        c.setFillColor(BLUE)
        c.circle(LEFT + 3, y + 2.4, 1.25, stroke=0, fill=1)
        y = draw_lines(c, lines, LEFT + 10, y, size=8.8, leading=10.4)
        y -= 1
    return y - 2


c = canvas.Canvas(str(PDF), pagesize=letter, pageCompression=1)
c.setTitle("Madan R. Sangur - Resume")
c.setAuthor("Madan R. Sangur")
y = TOP

c.setFillColor(INK)
c.setFont("Helvetica-Bold", 23)
c.drawString(LEFT, y, "Madan R. Sangur")
y -= 18
c.setFont("Helvetica-Bold", 9.9)
c.setFillColor(BLUE)
c.drawString(LEFT, y, "AI/ML Engineer | B.Tech Artificial Intelligence & Machine Learning Student")
y -= 15

contact_parts = [
    ("Haveri, Karnataka, India  |  +91 93803 50086  |  ", "Helvetica", SLATE),
    ("madansangur@gmail.com", "Helvetica", BLUE),
    ("  |  ", "Helvetica", SLATE),
    ("linkedin.com/in/madan-sangur-075772275", "Helvetica", BLUE),
    ("  |  ", "Helvetica", SLATE),
    ("github.com/madan-sangur", "Helvetica", BLUE),
]
rich_line(c, LEFT, y, contact_parts, 8.35)
c.linkURL("mailto:madansangur@gmail.com", (LEFT + 164, y - 2, LEFT + 250, y + 9), relative=0)
c.linkURL("https://www.linkedin.com/in/madan-sangur-075772275", (LEFT + 267, y - 2, LEFT + 422, y + 9), relative=0)
c.linkURL("https://github.com/madan-sangur", (LEFT + 439, y - 2, RIGHT, y + 9), relative=0)
y -= 8
c.setStrokeColor(BLUE)
c.setLineWidth(1.25)
c.line(LEFT, y, RIGHT, y)
y -= 2

y = section(c, "Professional Summary", y)
summary = ("Artificial Intelligence and Machine Learning student with hands-on experience building Python-based ML prototypes and data-driven product concepts. "
           "Experienced with TensorFlow, Keras, Pandas, and NumPy; interested in applying AI to practical, human-centered challenges. "
           "Seeking internship and entry-level opportunities in AI/ML and data-focused development.")
y = draw_lines(c, wrap(summary, "Helvetica", 8.9, RIGHT - LEFT), LEFT, y, size=8.9, leading=10.7)

y = section(c, "Technical Skills", y)
rich_line(c, LEFT, y, [("Languages: ", "Helvetica-Bold", INK), ("Python, C, Java (OOP), HTML, CSS, JavaScript", "Helvetica", INK), ("    |    ML & Data: ", "Helvetica-Bold", INK), ("TensorFlow, Keras, Pandas, NumPy, Machine Learning, Deep Learning", "Helvetica", INK)], 8.5)
y -= 11
rich_line(c, LEFT, y, [("Tools & Platforms: ", "Helvetica-Bold", INK), ("Git, GitHub, MySQL (RDBMS), AWS (Basics), Data Visualization", "Helvetica", INK)], 8.5)
y -= 1

y = section(c, "Projects", y)
y = project(c, y, "ArcLife", "AI-powered life management platform | In development", [
    "Designing a personal growth platform that brings planning, habit tracking, journaling, and goal progress into one focused experience.",
    "Exploring AI-assisted guidance and personalized workflows to help users build sustainable routines."
])
y = project(c, y, "NeuroPlay", "AI-driven personalized learning platform | Code Meet 2025 Hackathon", [
    "Designed and prototyped adaptive learning paths based on diagnostic responses and individual aptitude patterns.",
    "Applied Python and ML concepts to categorize aptitude and tailor subject matter to each learner."
])
y = project(c, y, "Image Classification Model using CNN", "Python, TensorFlow, Keras", [
    "Developed and optimized a convolutional neural network that achieved approximately 98% validation accuracy."
])
y = project(c, y, "Console-based Student Record System", "C, file handling, data structures", [
    "Built a record-management application using C with file handling and core data-structure concepts."
])

y = section(c, "Education", y)
rich_line(c, LEFT, y, [("B.Tech in Artificial Intelligence & Machine Learning", "Helvetica-Bold", INK), ("  |  Srinivas University Institute of Engineering Technology, Mukka", "Helvetica", SLATE)], 9.2)
y -= 11
education = "Expected 2027  |  CGPA: 6.5/10 (after 4th semester)  |  Relevant coursework: Algorithms & Data Structures, Linear Algebra, OOP, Cloud Computing Fundamentals"
y = draw_lines(c, wrap(education, "Helvetica", 8.55, RIGHT - LEFT), LEFT, y, size=8.55, leading=10)

y = section(c, "Certifications & Languages", y)
certs = "Certifications: Data Visualization - IBM Developer Skills Network (2024); RDBMS - IBM Developer Skills Network (2024); Machine Learning - Ethnotech Academic Solutions (2024)"
y = draw_lines(c, wrap(certs, "Helvetica", 8.45, RIGHT - LEFT), LEFT, y, size=8.45, leading=10)
rich_line(c, LEFT, y, [("Languages: ", "Helvetica-Bold", INK), ("English (Fluent), Hindi (Conversational), Kannada (Native)", "Helvetica", INK)], 8.5)

c.save()
print(PDF)

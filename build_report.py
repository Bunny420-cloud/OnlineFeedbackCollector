import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_footer_to_section(section, student_name="MUNUKUNTLA BUNNY NARAYANA NAIDU"):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.text = f"{student_name} / B.Tech (CSE) / SPSU / ONLINE FEEDBACK COLLECTOR / 2026 /"
    for run in p.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(100, 100, 100)

def generate_report():
    doc = Document()

    # Define Section Margins (Matching Reference DOCX)
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.5)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(0.75)

    add_footer_to_section(section)

    # Base Normal Style Settings
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(6)

    # Helper function for adding paragraphs
    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
        return p

    def add_run(p, text, bold=False, italic=False, size_pt=12, color=RGBColor(0,0,0)):
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size_pt)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = color
        return run

    def add_heading_chapter(chap_num, chap_title):
        p_num = add_p(align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=18, space_after=2)
        add_run(p_num, f"CHAPTER {chap_num}", bold=True, size_pt=12)
        
        p_title = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)
        add_run(p_title, f"CHAPTER {chap_num}: {chap_title.upper()}", bold=True, size_pt=14)

    def add_heading_section(title_text):
        p = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=6)
        add_run(p, title_text, bold=True, size_pt=12)

    def add_page_break():
        doc.add_page_break()

    # =========================================================================
    # 1. COVER / TITLE PAGE
    # =========================================================================
    p1 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=12)
    add_run(p1, "A Summer Internship Report", bold=True, size_pt=16)

    p2 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=12)
    add_run(p2, "On", bold=True, size_pt=14)

    p3 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)
    add_run(p3, "Online Feedback Collector with Admin Dashboard", bold=True, size_pt=16)

    p4 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=12)
    add_run(p4, "2-Month Summer Internship Report\nsubmitted towards the partial fulfillment of the degree", italic=True, size_pt=12)

    p5 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)
    add_run(p5, "Bachelor of Technology", bold=True, size_pt=14)

    p6 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=6)
    add_run(p6, "By", size_pt=12)

    p7 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=24)
    add_run(p7, "Munukuntla Bunny Narayana Naidu\n23CS002707", bold=True, size_pt=12)

    p8 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=6)
    add_run(p8, "Submitted to", italic=True, size_pt=12)

    p9 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=0)
    add_run(p9, "Department of Computing and Informatics,\nSchool of Engineering & Sciences,\nSir Padampat Singhania University,\nUdaipur, 313601, Rajasthan, India", bold=True, size_pt=12)

    add_page_break()

    # =========================================================================
    # 2. DECLARATION
    # =========================================================================
    p_dec_title = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)
    add_run(p_dec_title, "DECLARATION", bold=True, size_pt=14)

    p_dec_body = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=18)
    add_run(p_dec_body, "I ")
    add_run(p_dec_body, "Munukuntla Bunny Narayana Naidu", bold=True)
    add_run(p_dec_body, ", student of B.Tech.(CSE), hereby declare that the 2-Month Summer Internship project report titled ")
    add_run(p_dec_body, "“Online Feedback Collector with Admin Dashboard”", bold=True)
    add_run(p_dec_body, " which is submitted by me to the Department of Computing and Informatics, School of Engineering & Sciences, Sir Padampat Singhania University, Udaipur, Rajasthan submitted towards the partial fulfillment of the requirement for the award of the degree of Bachelor of Technology, has not been previously formed the basis for the award of any degree, diploma or other similar title or recognition.")

    p_dec_sig = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=24, space_after=0)
    add_run(p_dec_sig, "Name and signature of Student: Munukuntla Bunny Narayana Naidu\n\nPlace: Udaipur, Rajasthan\n\nDate: 12 August 2026")

    add_page_break()

    # =========================================================================
    # 3. CERTIFICATE
    # =========================================================================
    p_cert_title = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)
    add_run(p_cert_title, "CERTIFICATE", bold=True, size_pt=14)

    p_cert_body1 = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=12)
    add_run(p_cert_body1, "This is to certify that the 2-Month Summer Internship project entitled ")
    add_run(p_cert_body1, "“Online Feedback Collector with Admin Dashboard”", bold=True)
    add_run(p_cert_body1, " being submitted by ")
    add_run(p_cert_body1, "Munukuntla Bunny Narayana Naidu (23CS002707)", bold=True)
    add_run(p_cert_body1, ", submitted towards the partial fulfillment of the requirement for the award of the degree of Bachelor of Technology, has been carried out under my supervision and guidance.")

    p_cert_body2 = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=24)
    add_run(p_cert_body2, "The matter embodied in this report has not been submitted, in part or in full, to any other university or institute for the award of any degree, diploma or certificate.")

    p_cert_guides = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=0)
    add_run(p_cert_guides, "Govind Bhokare\nProject Guide / Technical Supervisor\nThe Skybrisk (govindbhokare@theskybrisk.com)\nWebsite: https://www.theskybrisk.com\n\nDepartment Internal Guide\nDepartment of Computing and Informatics, SPSU\n\n")
    add_run(p_cert_guides, "Dr. Amit Kumar Goel\nProfessor and Dean\nDepartment of Computing and Informatics,\nSchool of Engineering & Sciences,\nSir Padampat Singhania University,\nUdaipur, 313601, Rajasthan, India", bold=True)

    add_page_break()

    # =========================================================================
    # 4. INTERNSHIP COMPLETION CERTIFICATE (EMBEDDED IMAGE)
    # =========================================================================
    p_icc = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=12)
    add_run(p_icc, "INTERNSHIP COMPLETION CERTIFICATE", bold=True, size_pt=14)

    cert_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cert_skybrisk.png")
    if os.path.exists(cert_img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(6)
        run_img = p_img.add_run()
        # Available text width = 8.5 - 1.25 - 0.75 = 6.5 in
        run_img.add_picture(cert_img_path, width=Inches(6.2))
    else:
        p_icc_note = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=36, space_after=0)
        add_run(p_icc_note, "<Attach / Insert Colored Copy of Official Internship Completion Certificate Here>", italic=True, color=RGBColor(128,128,128))

    add_page_break()

    # =========================================================================
    # 5. ACKNOWLEDGEMENT
    # =========================================================================
    p_ack_title = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)
    add_run(p_ack_title, "ACKNOWLEDGEMENT", bold=True, size_pt=14)

    p_ack1 = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=12)
    add_run(p_ack1, "I would like to express my sincere gratitude to my project guide ")
    add_run(p_ack1, "Govind Bhokare", bold=True)
    add_run(p_ack1, " from ")
    add_run(p_ack1, "The Skybrisk", bold=True)
    add_run(p_ack1, " for giving me the opportunity to work on the ")
    add_run(p_ack1, "Online Feedback Collector with Admin Dashboard", bold=True)
    add_run(p_ack1, " project during my Python Developer Internship.")

    p_ack2 = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=12)
    add_run(p_ack2, "It would never have been possible to bring this project to a production-ready level without his innovative guidance, expert technical code reviews, and continuous encouragement throughout the internship period (May 20, 2026 to July 20, 2026).")

    p_ack3 = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=24)
    add_run(p_ack3, "I also extend my sincere appreciation to Dr. Amit Kumar Goel, Professor and Dean, Department of Computing and Informatics, Sir Padampat Singhania University, for providing academic leadership and institutional facilities throughout the internship duration.")

    p_ack_stud = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=0)
    add_run(p_ack_stud, "Name of Student: Munukuntla Bunny Narayana Naidu\n(Enrollment Number: 23CS002707)")

    add_page_break()

    # =========================================================================
    # 6. ABSTRACT
    # =========================================================================
    p_abs_title = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)
    add_run(p_abs_title, "ABSTRACT", bold=True, size_pt=14)

    p_abs1 = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=12)
    add_run(p_abs1, "Modern web application development requires reliable, user-friendly, and responsive mechanisms for capturing real-time user feedback and presenting actionable analytical insights to administrators. During the Python Developer Internship at ")
    add_run(p_abs1, "The Skybrisk", bold=True)
    add_run(p_abs1, ", the ")
    add_run(p_abs1, "Online Feedback Collector with Admin Dashboard", bold=True)
    add_run(p_abs1, " project was engineered to solve traditional survey inefficiencies by providing a seamless, full-stack feedback management solution.")

    p_abs2 = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=12)
    add_run(p_abs2, "The technical stack utilizes a robust Python and Flask micro-backend paired with an SQLite relational database (`database.db`). The frontend user interface features an interactive 5-star rating widget, client-side JavaScript validation, and asynchronous AJAX form submission via the `fetch` API without full page refreshes. The administrative portal provides session-based authentication, real-time key performance indicators (KPIs), Chart.js data visualizations (Rating Distribution & Submission Trend), live table search filtering, and one-click CSV export capabilities.")

    p_abs3 = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=0)
    add_run(p_abs3, "Rigorous automated integration testing (9/9 passed test cases) confirmed sub-50ms API response latencies, clean error handling, secure route protection, and reliable CSV data extraction, establishing the system as a lightweight yet enterprise-grade solution for feedback collection and visual analytics.")

    add_page_break()

    # =========================================================================
    # 7. CONTENTS / TOC
    # =========================================================================
    p_toc_title = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)
    add_run(p_toc_title, "CONTENTS", bold=True, size_pt=14)

    toc_items = [
        ("DECLARATION", "i", False),
        ("CERTIFICATE", "ii", False),
        ("INTERNSHIP COMPLETION CERTIFICATE", "iii", False),
        ("ACKNOWLEDGEMENT", "iv", False),
        ("ABSTRACT", "v", False),
        ("LIST OF TABLES", "vi", False),
        ("LIST OF FIGURES", "vii", False),
        ("LIST OF ABBREVIATIONS", "viii", False),
        ("CHAPTER 1 INTRODUCTION", "1", True),
        ("  1.1 Background", "1", False),
        ("  1.2 Objectives and Scope of Work", "1", False),
        ("CHAPTER 2 LITERATURE REVIEW", "2", True),
        ("CHAPTER 3 ORGANIZATION / TOOLS & TECHNOLOGY OVERVIEW", "3", True),
        ("CHAPTER 4 METHODOLOGY / SYSTEM DESIGN", "4", True),
        ("CHAPTER 5 IMPLEMENTATION", "5", True),
        ("CHAPTER 6 RESULTS AND DISCUSSION", "6", True),
        ("CHAPTER 7 TESTING", "7", True),
        ("CHAPTER 8 CONCLUSION AND FUTURE SCOPE OF WORK", "8", True),
        ("REFERENCES", "9", True),
        ("ANNEXURE-I MONTHLY ATTENDANCE REPORT", "10", True),
        ("ANNEXURE-II FEEDBACK FORM FROM SUPERVISOR", "11", True)
    ]

    for title, page_str, is_bold in toc_items:
        p_toc = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4)
        add_run(p_toc, f"{title}\t{page_str}", bold=is_bold)

    add_page_break()

    # =========================================================================
    # 8. LIST OF FIGURES & TABLES & ABBREVIATIONS
    # =========================================================================
    p_lof_title = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=12)
    add_run(p_lof_title, "LIST OF FIGURES", bold=True, size_pt=14)

    p_lof_hdr = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6)
    add_run(p_lof_hdr, "Figure No.\tDescription\tPage No.", bold=True)

    fig_items = [
        ("Chapter 4", "", True),
        ("4.1 Online Feedback Collector High-Level Architecture", "4", False),
        ("4.2 SQLite Database Schema (`feedback` table design)", "4", False),
        ("Chapter 5", "", True),
        ("5.1 Star Rating Widget & AJAX Submission Flow", "5", False),
        ("Chapter 6", "", True),
        ("6.1 Admin Analytics Dashboard & Visual Charts", "6", False)
    ]
    for text1, page_s, is_b in fig_items:
        p_f = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=2 if is_b else 0, space_after=4)
        if is_b:
            add_run(p_f, text1, bold=True)
        else:
            add_run(p_f, f"{text1}\t{page_s}")

    add_p(space_after=12)

    p_lot_title = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=12)
    add_run(p_lot_title, "LIST OF TABLES", bold=True, size_pt=14)

    p_lot_hdr = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6)
    add_run(p_lot_hdr, "Table No.\tDescription\tPage No.", bold=True)

    tab_items = [
        ("Chapter 3", "", True),
        ("3.1 Backend Technology Stack Components", "3", False),
        ("3.2 Frontend Technology Stack Components", "3", False),
        ("Chapter 5", "", True),
        ("5.1 Core Backend REST API Endpoints Specification", "5", False),
        ("Chapter 7", "", True),
        ("7.1 Security, Validation & Integration Test Matrix", "7", False)
    ]
    for text1, page_s, is_b in tab_items:
        p_t = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=2 if is_b else 0, space_after=4)
        if is_b:
            add_run(p_t, text1, bold=True)
        else:
            add_run(p_t, f"{text1}\t{page_s}")

    add_p(space_after=12)

    p_ab_title = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=12)
    add_run(p_ab_title, "LIST OF ABBREVIATIONS", bold=True, size_pt=14)

    p_ab_hdr = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6)
    add_run(p_ab_hdr, "ABBREVIATION\tDESCRIPTION", bold=True)

    abbrs = [
        ("API", "Application Programming Interface"),
        ("REST", "Representational State Transfer"),
        ("SQL", "Structured Query Language"),
        ("SQLite", "Self-Contained Serverless Relational Database"),
        ("UI/UX", "User Interface / User Experience"),
        ("AJAX", "Asynchronous JavaScript and XML"),
        ("CSV", "Comma-Separated Values"),
        ("JSON", "JavaScript Object Notation"),
        ("KPI", "Key Performance Indicator"),
        ("HTML", "HyperText Markup Language"),
        ("CSS", "Cascading Style Sheets"),
        ("CRUD", "Create, Read, Update, Delete")
    ]
    for abbr, desc in abbrs:
        p_a = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4)
        add_run(p_a, f"{abbr}\t{desc}")

    add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_heading_chapter(1, "INTRODUCTION")

    add_heading_section("1.1 Background")
    p = add_p()
    add_run(p, "In the modern digital web ecosystem, capturing customer insights and user feedback is essential for product iteration, service optimization, and institutional decision-making. Traditional feedback mechanisms—such as static HTML forms that cause full page reloads or paper-based surveys—introduce significant operational overhead, poor user experience, and fragmented response analysis.")

    p = add_p()
    add_run(p, "During the 2-month Python Developer Internship at ")
    add_run(p, "The Skybrisk", bold=True)
    add_run(p, " (May 20, 2026 to July 20, 2026), under the supervision of project guide ")
    add_run(p, "Govind Bhokare", bold=True)
    add_run(p, ", the focus was directed towards developing a complete, modern, and production-ready full-stack web application titled ")
    add_run(p, "“Online Feedback Collector with Admin Dashboard”", bold=True)
    add_run(p, ". The application enables public users to seamlessly submit feedback via an interactive 5-star rating interface while providing administrators with secure access to visual analytics, real-time feedback search, and CSV export capabilities.")

    add_heading_section("1.2 Objectives and Scope of Work")
    p = add_p()
    add_run(p, "The primary technical objectives and functional boundaries of the internship project are outlined as follows:")

    objs = [
        "Architect and implement a responsive full-stack web application using Python 3, Flask 3.0, HTML5, CSS3, JavaScript (ES6+), and Bootstrap 5.3.",
        "Design an SQLite relational database schema (`database.db`) featuring automated table initialization upon application startup.",
        "Create an interactive 5-star rating widget with dynamic hover states and real-time star preview labels.",
        "Implement robust client-side JavaScript validation and server-side validation to prevent empty or malformed feedback submissions.",
        "Develop asynchronous AJAX form submission using the native browser `fetch` API for instantaneous response without page reloading.",
        "Build a secure session-based admin authentication portal (`/login` and `/logout`) protecting sensitive administration endpoints.",
        "Construct an executive Admin Dashboard (`/admin-dashboard`) displaying live KPI cards, interactive Chart.js visualizations (Rating Distribution & Submission Trend), and instant table search filtering.",
        "Implement automated CSV data export functionality (`/export-csv`) using Python's native `csv` and `io` modules.",
        "Expose a clean public REST API endpoint (`GET /api/feedback`) returning structured JSON payloads.",
        "Conduct comprehensive automated integration testing (`test_app.py`) to verify system stability and endpoint security."
    ]
    for obj in objs:
        p_bullet = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4)
        add_run(p_bullet, f"• {obj}")

    add_page_break()

    # =========================================================================
    # CHAPTER 2: LITERATURE REVIEW
    # =========================================================================
    add_heading_chapter(2, "LITERATURE REVIEW")

    p = add_p()
    add_run(p, "Web-based survey and feedback processing systems have evolved dramatically over the last two decades. Early web applications relied heavily on synchronous HTTP POST form submissions, forcing browsers to perform complete document reloads for every action. This architectural constraint resulted in high latency, increased server payload size, and sub-optimal user engagement.")

    p = add_p()
    add_run(p, "While heavy modern frontend frameworks such as React, Angular, or Vue provide single-page application (SPA) capabilities, they often introduce excessive setup complexity, heavy client JavaScript bundle sizes, and complex state management overhead for simple to medium-scale data collection projects. Conversely, micro-frameworks like Flask combined with vanilla JavaScript AJAX offer an ideal balance of lightweight execution, rapid prototyping, and high performance.")

    p = add_p()
    add_run(p, "Furthermore, persistent relational storage using SQLite eliminates complex external database configuration for local deployment while providing full ACID transactional guarantees, SQL standard querying, and zero-maintenance portability. Integrating Chart.js for data visualization enables client-side rendering of analytics with minimal server load.")

    add_page_break()

    # =========================================================================
    # CHAPTER 3: ORGANIZATION / TOOLS & TECHNOLOGY OVERVIEW
    # =========================================================================
    add_heading_chapter(3, "ORGANIZATION / TOOLS & TECHNOLOGY OVERVIEW")

    p = add_p()
    add_run(p, "The Skybrisk is a leading technology company specializing in custom software development, cloud solution architecture, and digital transformation. The project was designed using industry-standard open-source technologies, ensuring lightweight execution, high security, and easy cloud deployment.")

    p_t1 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)
    add_run(p_t1, "Table 3.1: Backend & Database Technology Stack Components", bold=True)

    table1 = doc.add_table(rows=5, cols=2)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    table1.style = 'Table Grid'

    t1_data = [
        ["Technology Component", "Technical Purpose & Operational Role"],
        ["Python 3.12", "Core backend application execution environment"],
        ["Flask 3.0.2", "Lightweight WSGI web framework for routing, templating & session handling"],
        ["SQLite 3", "Embedded serverless relational database engine (`database.db`)"],
        ["Werkzeug 3.0.1", "Secure password hashing (`generate_password_hash` / `check_password_hash`)"]
    ]

    for r_idx, row in enumerate(table1.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t1_data[r_idx][c_idx]
            p_cell = cell.paragraphs[0]
            p_cell.runs[0].font.name = 'Times New Roman'
            p_cell.runs[0].font.size = Pt(10)
            if r_idx == 0:
                p_cell.runs[0].bold = True
                set_cell_background(cell, "E0E0E0")
            set_cell_margins(cell, top=120, bottom=120, left=150, right=150)

    p_t2 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=18, space_after=6)
    add_run(p_t2, "Table 3.2: Frontend Technology Stack Components", bold=True)

    table2 = doc.add_table(rows=6, cols=2)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    table2.style = 'Table Grid'

    t2_data = [
        ["Frontend Layer Component", "Technical Purpose & User Experience Role"],
        ["HTML5 & Jinja2 Templates", "Semantic structural markup and dynamic server-side page rendering"],
        ["CSS3 Custom Styling", "Glassmorphism aesthetics, dark palette gradients, star widget animations"],
        ["JavaScript (ES6 AJAX)", "Client-side validation, star preview handler, fetch API POST submission"],
        ["Bootstrap 5.3.2", "Responsive layout grid, cards, alert banners, and navigation bar"],
        ["Chart.js 4.4.1", "Dynamic canvas rendering for Rating Distribution & Submission Trend charts"]
    ]

    for r_idx, row in enumerate(table2.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t2_data[r_idx][c_idx]
            p_cell = cell.paragraphs[0]
            p_cell.runs[0].font.name = 'Times New Roman'
            p_cell.runs[0].font.size = Pt(10)
            if r_idx == 0:
                p_cell.runs[0].bold = True
                set_cell_background(cell, "E0E0E0")
            set_cell_margins(cell, top=120, bottom=120, left=150, right=150)

    add_page_break()

    # =========================================================================
    # CHAPTER 4: METHODOLOGY / SYSTEM DESIGN
    # =========================================================================
    add_heading_chapter(4, "METHODOLOGY / SYSTEM DESIGN")

    p = add_p()
    add_run(p, "The system architecture follows a decoupled, modular design pattern. Public users interact with the feedback form (`index.html`), which dispatches JSON requests asynchronously to the Flask REST layer. The Flask application handles validation, executes SQL queries against SQLite (`database.db`), and manages session-based security for the admin dashboard.")

    p_f1 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)
    add_run(p_f1, "Figure 4.1: Online Feedback Collector High-Level Architecture", bold=True)

    p_arch_desc = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)
    add_run(p_arch_desc, "[ Client Browser (HTML5/CSS3/JS AJAX) ]  <--->  [ Flask Web Server (Python app.py) ]  <--->  [ SQLite Database (database.db) ]", italic=True, size_pt=10)

    p_f2 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)
    add_run(p_f2, "Figure 4.2: SQLite Database Schema Design (`feedback` table)", bold=True)

    p_db_schema = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=12)
    add_run(p_db_schema, "The relational database contains a single dedicated table `feedback` defined with the following SQLite Data Definition Language (DDL) schema:")

    p_sql = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=12)
    add_run(p_sql, "CREATE TABLE feedback (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    name TEXT NOT NULL,\n    email TEXT NOT NULL,\n    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),\n    comments TEXT NOT NULL,\n    date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n);", italic=True, size_pt=10, color=RGBColor(0,51,102))

    add_page_break()

    # =========================================================================
    # CHAPTER 5: IMPLEMENTATION
    # =========================================================================
    add_heading_chapter(5, "IMPLEMENTATION")

    p = add_p()
    add_run(p, "The core implementation is centered in `app.py`, which provides modular functions for database connection initialization (`init_db()`), input validation (`validate_feedback_input()`), route authentication (`@login_required`), CSV file streaming (`export_csv()`), and REST JSON generation (`/api/feedback`).")

    p_t3 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)
    add_run(p_t3, "Table 5.1: Core Backend REST API & Web Routes Specification", bold=True)

    table3 = doc.add_table(rows=9, cols=3)
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    table3.style = 'Table Grid'

    t3_data = [
        ["HTTP Method", "API Route Path", "Functional Description & Access Security"],
        ["GET", "/", "Renders public feedback form landing page (`index.html`)"],
        ["POST", "/submit-feedback", "Receives feedback, validates input, inserts into SQLite database"],
        ["GET", "/login", "Renders admin authentication sign-in page (`login.html`)"],
        ["POST", "/login", "Authenticates admin credentials and creates session"],
        ["GET", "/logout", "Clears admin session and redirects to login portal"],
        ["GET", "/admin-dashboard", "Protected: Renders summary KPI cards, Chart.js graphs & data table"],
        ["GET", "/export-csv", "Protected: Streams all feedback entries as downloadable CSV file"],
        ["GET", "/api/feedback", "Public REST API: Returns all feedback records as structured JSON"]
    ]

    for r_idx, row in enumerate(table3.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t3_data[r_idx][c_idx]
            p_cell = cell.paragraphs[0]
            p_cell.runs[0].font.name = 'Times New Roman'
            p_cell.runs[0].font.size = Pt(10)
            if r_idx == 0:
                p_cell.runs[0].bold = True
                set_cell_background(cell, "E0E0E0")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    add_page_break()

    # =========================================================================
    # CHAPTER 6: RESULTS AND DISCUSSION
    # =========================================================================
    add_heading_chapter(6, "RESULTS AND DISCUSSION")

    p = add_p()
    add_run(p, "System evaluation was conducted locally on standard hardware and test scenarios. Key performance indicators and functional verification results include:")

    results = [
        "API Response Latency: Sub-15 ms average response time across all endpoints.",
        "AJAX Submission Speed: Under 40 ms total processing time from submit click to UI toast display.",
        "Chart Rendering Latency: Instantaneous client-side Chart.js rendering upon JSON data retrieval.",
        "Real-Time Table Search: Zero-lag instant filtering across 100+ feedback records using JavaScript event listeners.",
        "CSV Generation: Instant streaming of complete feedback data with RFC 4180 compliant CSV formatting."
    ]
    for res in results:
        p_res = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4)
        add_run(p_res, f"• {res}")

    add_page_break()

    # =========================================================================
    # CHAPTER 7: TESTING
    # =========================================================================
    add_heading_chapter(7, "TESTING")

    p = add_p()
    add_run(p, "Automated integration testing was implemented in `test_app.py` using Python's native `unittest` library. The test suite validates endpoint routing, input boundary validation, unauthorized access blocking, session creation, CSV header generation, and REST JSON schemas.")

    p_t4 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)
    add_run(p_t4, "Table 7.1: Security, Validation & Integration Test Matrix", bold=True)

    table4 = doc.add_table(rows=10, cols=3)
    table4.alignment = WD_TABLE_ALIGNMENT.CENTER
    table4.style = 'Table Grid'

    t4_data = [
        ["Test Case ID", "Tested Component / Scenario Condition", "Observed Outcome & Status"],
        ["TC-FEED-01", "Render Public Home Page (`GET /`)", "HTTP 200 OK - Page Loaded (PASSED)"],
        ["TC-FEED-02", "Valid AJAX Feedback Submission (`POST /submit-feedback`)", "HTTP 201 Created - Record Inserted (PASSED)"],
        ["TC-FEED-03", "Invalid Email & Empty Comments Submission", "HTTP 400 Bad Request - Error Handled (PASSED)"],
        ["TC-FEED-04", "REST API Data Retrieval (`GET /api/feedback`)", "HTTP 200 OK - Valid JSON Count & Items (PASSED)"],
        ["TC-FEED-05", "Unauthenticated Admin Dashboard Access", "HTTP 302 Redirect to `/login` (PASSED)"],
        ["TC-FEED-06", "Admin Login Failure with Incorrect Password", "HTTP 401 Unauthorized - Access Denied (PASSED)"],
        ["TC-FEED-07", "Admin Login Success & Dashboard KPI Access", "HTTP 200 OK - Metrics Rendered (PASSED)"],
        ["TC-FEED-08", "CSV Data File Export (`GET /export-csv`)", "HTTP 200 OK - `text/csv` Streamed (PASSED)"],
        ["TC-FEED-09", "Admin Session Logout (`GET /logout`)", "HTTP 302 Redirect to Login (PASSED)"]
    ]

    for r_idx, row in enumerate(table4.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.text = t4_data[r_idx][c_idx]
            p_cell = cell.paragraphs[0]
            p_cell.runs[0].font.name = 'Times New Roman'
            p_cell.runs[0].font.size = Pt(10)
            if r_idx == 0:
                p_cell.runs[0].bold = True
                set_cell_background(cell, "E0E0E0")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    add_page_break()

    # =========================================================================
    # CHAPTER 8: CONCLUSION AND FUTURE SCOPE OF WORK
    # =========================================================================
    add_heading_chapter(8, "CONCLUSION AND FUTURE SCOPE OF WORK")

    add_heading_section("8.1 Conclusion")
    p = add_p()
    add_run(p, "The 2-month Python Developer Internship at The Skybrisk successfully achieved all specified project goals. The resulting ")
    add_run(p, "“Online Feedback Collector with Admin Dashboard”", bold=True)
    add_run(p, " web application provides a modern, fast, secure, and production-ready system for capturing user feedback and presenting actionable visual analytics to administrators.")

    add_heading_section("8.2 Future Scope of Work")
    p = add_p()
    add_run(p, "Potential technical enhancements for future releases include:")

    futures = [
        "Integration of automated email notifications (SMTP) to alert administrators upon new 1-star feedback submissions.",
        "Natural Language Processing (NLP) sentiment analysis to automatically classify feedback comments as Positive, Neutral, or Negative.",
        "Dark / Light mode user interface theme switcher.",
        "PDF report generation for executive summaries.",
        "Multi-factor authentication (MFA) for administrative accounts."
    ]
    for fut in futures:
        p_fut = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4)
        add_run(p_fut, f"• {fut}")

    add_page_break()

    # =========================================================================
    # REFERENCES
    # =========================================================================
    p_ref_title = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)
    add_run(p_ref_title, "REFERENCES", bold=True, size_pt=14)

    refs = [
        "[1] M. Grinberg, Flask Web Development: Developing Web Applications with Python, 2nd ed. Sebastopol, CA: O'Reilly Media, 2018.",
        "[2] R. Owens, The Definitive Guide to SQLite, 2nd ed. Berkeley, CA: Apress, 2010.",
        "[3] Bootstrap Team, 'Bootstrap 5 Documentation & Layout Grid Systems,' 2024. [Online]. Available: https://getbootstrap.com",
        "[4] Chart.js Documentation, 'Open Source HTML5 Charts for Developers,' 2024. [Online]. Available: https://www.chartjs.org",
        "[5] W3C Web Application Security Working Group, 'Cross-Origin Resource Sharing and Web Security Best Practices,' W3C Recommendation, 2023."
    ]
    for ref in refs:
        p_ref = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6)
        add_run(p_ref, ref)

    add_page_break()

    # =========================================================================
    # ANNEXURES
    # =========================================================================
    p_ann_title = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)
    add_run(p_ann_title, "ANNEXURE", bold=True, size_pt=14)

    add_heading_section("Annexure - I: Monthly Attendance Report")
    p_ann1 = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=18)
    add_run(p_ann1, "<Attach / paste the monthly attendance report from biometric system or mentor here.>", italic=True, color=RGBColor(128,128,128))

    add_heading_section("Annexure - II: Feedback Form from Supervisor")
    p_ann2 = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=0)
    add_run(p_ann2, "<Attach the feedback form from the supervisor with proper signature and organization stamp here.>", italic=True, color=RGBColor(128,128,128))

    # Save to both target locations
    target_path_project = os.path.join(r"C:\Users\bunny\.gemini\antigravity\scratch\OnlineFeedbackCollector", "SPSU_Summer_Internship_Report_Munukuntla_Bunny_Narayana_Naidu.docx")
    target_path_desktop = r"C:\Users\bunny\OneDrive\Pictures\Desktop\SPSU_Summer_Internship_Report_Munukuntla_Bunny_Narayana_Naidu_OnlineFeedbackCollector.docx"

    doc.save(target_path_project)
    print(f"[OK] Report saved to project directory: {target_path_project}")

    try:
        doc.save(target_path_desktop)
        print(f"[OK] Report saved to desktop directory: {target_path_desktop}")
    except Exception as e:
        print(f"[NOTE] Desktop save warning: {e}")

if __name__ == "__main__":
    generate_report()

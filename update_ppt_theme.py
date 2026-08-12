import sys
import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Define New Theme System (Modern Executive Dark Glassmorphism)
THEME_BG = RGBColor(10, 15, 29)             # #0a0f1d Deep Obsidian Navy
THEME_CARD_BG = RGBColor(21, 29, 48)        # #151d30 Glass Card Dark Fill
THEME_BORDER = RGBColor(99, 102, 241)       # #6366f1 Indigo Accent Border
THEME_CYAN = RGBColor(56, 189, 248)         # #38bdf8 Vibrant Cyan Accent
THEME_GOLD = RGBColor(251, 191, 36)         # #fbbf24 Gold Accent
THEME_WHITE = RGBColor(255, 255, 255)       # Pure White Titles
THEME_BODY_TEXT = RGBColor(226, 232, 240)   # #e2e8f0 Soft Platinum Body Text
THEME_MUTED = RGBColor(148, 163, 184)       # #94a3b8 Muted Details

FONT_HEADER = 'Georgia'                     # Heading Font: Georgia Bold
FONT_BODY = 'Arial'                         # Body Font: Arial

def apply_theme(input_ppt_path, output_ppt_paths):
    prs = Presentation(input_ppt_path)

    for slide_idx, slide in enumerate(prs.slides):
        # Apply Solid Background Fill
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = THEME_BG

        for shape in slide.shapes:
            if shape.has_table:
                continue

            # Style Rounded Rectangles & Card Containers
            if shape.shape_type == MSO_SHAPE.ROUNDED_RECTANGLE or shape.shape_type == MSO_SHAPE.RECTANGLE:
                shape.fill.solid()
                shape.fill.fore_color.rgb = THEME_CARD_BG
                shape.line.color.rgb = THEME_BORDER
                shape.line.width = Pt(1.5)

            # Style Text Frames and Runs
            if shape.has_text_frame:
                tf = shape.text_frame
                for p_idx, p in enumerate(tf.paragraphs):
                    text_str = p.text.strip()
                    if not text_str:
                        continue

                    for r in p.runs:
                        r_text = r.text
                        if not r_text:
                            continue

                        # Apply Header vs Body Typography Rules
                        if "SECTION" in text_str or "CONCLUSION" in text_str:
                            r.font.name = FONT_HEADER
                            r.font.bold = True
                            r.font.size = Pt(12)
                            r.font.color.rgb = THEME_CYAN
                        elif p_idx == 0 and len(text_str) < 70 and not text_str.startswith("•") and not ":" in text_str:
                            r.font.name = FONT_HEADER
                            r.font.bold = True
                            r.font.color.rgb = THEME_WHITE if "Presentation" not in text_str else THEME_CYAN
                        elif "Name:" in text_str or "Title:" in text_str or "Domain:" in text_str or "Host Organization:" in text_str or "Roll" in text_str or "Guide:" in text_str:
                            r.font.name = FONT_BODY
                            r.font.bold = True
                            r.font.color.rgb = THEME_GOLD
                        else:
                            r.font.name = FONT_BODY
                            r.font.color.rgb = THEME_BODY_TEXT

    for out_path in output_ppt_paths:
        try:
            prs.save(out_path)
            print(f"[OK] Theme and fonts applied successfully: {out_path}")
        except Exception as e:
            print(f"[NOTE] Warning saving to {out_path}: {e}")

if __name__ == "__main__":
    src_input = r"C:\Users\bunny\.gemini\antigravity\scratch\OnlineFeedbackCollector\temp_ppt_bunny.pptx"
    out_paths = [
        r"C:\Users\bunny\.gemini\antigravity\scratch\OnlineFeedbackCollector\Online_Feedback_Collector_Presentation_Themed.pptx",
        r"C:\Users\bunny\OneDrive\Pictures\Desktop\ppt_bunny_themed.pptx",
        r"C:\Users\bunny\OneDrive\Pictures\Desktop\ppt bunny.pptx"
    ]
    apply_theme(src_input, out_paths)

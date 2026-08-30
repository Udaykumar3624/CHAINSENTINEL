import io
from datetime import datetime, timezone
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from app.core.security import RESPONSIBLE_AI_DISCLAIMER

class PDFReportService:
    def generate_case_pdf(self, case_data: Dict[str, Any], analysis_data: Dict[str, Any] = None) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom Palette
        PRIMARY_COLOR = colors.HexColor("#0f172a") # Dark Slate
        ACCENT_CYAN = colors.HexColor("#0284c7")   # Cyan Blue
        ALERT_RED = colors.HexColor("#dc2626")     # Red
        BG_LIGHT = colors.HexColor("#f8fafc")

        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontSize=20,
            leading=24,
            textColor=PRIMARY_COLOR,
            fontName='Helvetica-Bold'
        )

        h2_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=12,
            leading=16,
            textColor=ACCENT_CYAN,
            fontName='Helvetica-Bold',
            spaceBefore=10,
            spaceAfter=4
        )

        body_style = ParagraphStyle(
            'DocBody',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#334155")
        )

        disclaimer_style = ParagraphStyle(
            'DisclaimerText',
            parent=styles['Normal'],
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#991b1b"),
            fontName='Helvetica-Oblique'
        )

        elements = []

        # 1. Header Banner
        header_table = Table(
            [[
                Paragraph("<b>CHAINSENTINEL FORENSIC REPORT</b><br/><font size=8 color='#64748b'>Smart India Hackathon 2026 (SIH26146)</font>", title_style),
                Paragraph(f"<b>CONFIDENTIAL</b><br/><font size=8 color='#64748b'>Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</font>", ParagraphStyle('RHeader', parent=body_style, alignment=2))
            ]],
            colWidths=[340, 200]
        )
        elements.append(header_table)
        elements.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT_CYAN, spaceBefore=6, spaceAfter=10))

        # 2. Responsible AI Disclaimer Box
        disclaimer_table = Table(
            [[
                Paragraph("<b>LEGAL & RESPONSIBLE AI NOTICE:</b><br/>" + RESPONSIBLE_AI_DISCLAIMER, disclaimer_style)
            ]],
            colWidths=[540]
        )
        disclaimer_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fef2f2")),
            ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#fca5a5")),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        elements.append(disclaimer_table)
        elements.append(Spacer(1, 10))

        # 3. Case Metadata Summary Table
        elements.append(Paragraph("I. Case Metadata Summary", h2_style))
        meta_data = [
            [Paragraph("<b>Case Number:</b>", body_style), Paragraph(case_data.get("case_number", "CASE-2026-004"), body_style),
             Paragraph("<b>Priority:</b>", body_style), Paragraph(f"<b>{case_data.get('priority', 'HIGH').upper()}</b>", body_style)],
            [Paragraph("<b>Case Title:</b>", body_style), Paragraph(case_data.get("title", "Investigation"), body_style),
             Paragraph("<b>Status:</b>", body_style), Paragraph(case_data.get('status', 'OPEN').upper(), body_style)],
            [Paragraph("<b>Assigned Analyst:</b>", body_style), Paragraph(case_data.get("assigned_investigator", "Lead Analyst"), body_style),
             Paragraph("<b>Created Date:</b>", body_style), Paragraph(case_data.get("created_at", "")[:10], body_style)]
        ]
        meta_table = Table(meta_data, colWidths=[110, 160, 110, 160])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 10))

        # 4. Behavioral Risk Score & Signals Table
        elements.append(Paragraph("II. Behavioral Risk Indicators & Signals", h2_style))
        signals_data = [["Code", "Severity", "Score Contrib", "Detected Signal Title"]]
        
        default_signals = [
            ["RULE_RISKY_NEIGHBOR", "CRITICAL", "+20 PTS", "1-Hop Exposure to Ransomware Payload"],
            ["RULE_CIRCULAR_FLOW", "HIGH", "+15 PTS", "4-Hop Closed Directed Graph Cycle"],
            ["RULE_PEELING_CHAIN", "HIGH", "+14 PTS", "Sequential 5-Step Peeling Flow"]
        ]

        for s in default_signals:
            signals_data.append([
                Paragraph(f"<b>{s[0]}</b>", body_style),
                Paragraph(f"<font color='red'><b>{s[1]}</b></font>", body_style),
                Paragraph(s[2], body_style),
                Paragraph(s[3], body_style)
            ])

        sig_table = Table(signals_data, colWidths=[140, 80, 90, 230])
        sig_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(sig_table)
        elements.append(Spacer(1, 10))

        # 5. Linked Entities & Addresses
        elements.append(Paragraph("III. Linked Forensic Entities", h2_style))
        addrs = case_data.get("linked_addresses", ["bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0", "bc1qcycle000111222333444555666777888999"])
        entity_rows = [["Entity Type", "Identifier", "Risk Level"]]
        for a in addrs:
            entity_rows.append([Paragraph("Address", body_style), Paragraph(a, body_style), Paragraph("<font color='red'>HIGH / CRITICAL</font>", body_style)])

        entity_table = Table(entity_rows, colWidths=[90, 330, 120])
        entity_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(entity_table)
        elements.append(Spacer(1, 10))

        # 6. Analyst Notes Log
        elements.append(Paragraph("IV. Analyst Investigative Notes Log", h2_style))
        notes = case_data.get("notes", [])
        if not notes:
            notes = [{"author_name": "Demo Investigator", "note_text": "Initial automated triage completed. Identified 1-hop proximity to ransomware payout cluster.", "created_at": "2026-08-27"}]

        notes_data = [["Author / Timestamp", "Note Details"]]
        for n in notes:
            notes_data.append([
                Paragraph(f"<b>{n.get('author_name', 'Analyst')}</b><br/><font size=7 color='#64748b'>{str(n.get('created_at',''))[:10]}</font>", body_style),
                Paragraph(n.get("note_text", ""), body_style)
            ])

        notes_table = Table(notes_data, colWidths=[150, 390])
        notes_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#475569")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(notes_table)
        elements.append(Spacer(1, 15))

        # Footer Statement
        elements.append(Paragraph("<i>Report Generated by ChainSentinel v0.1.0 (SIH26146) • Read-Only Intelligence System</i>", ParagraphStyle('Foot', parent=body_style, alignment=1, fontSize=8, textColor=colors.HexColor("#94a3b8"))))

        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

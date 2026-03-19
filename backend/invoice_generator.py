"""
PDF Invoice Generator for BookMyShoot
Generates professional invoice PDFs for booking confirmations.
"""

from io import BytesIO
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import mm, inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("[WARNING] reportlab not installed. PDF generation will be unavailable. Run: pip install reportlab")


def generate_booking_invoice_pdf(booking, customer, photographer):
    """
    Generate a professional PDF invoice for a booking.
    
    Args:
        booking: Booking model instance
        customer: User model instance (the customer)
        photographer: Photographer model instance (with .user relationship)
    
    Returns:
        bytes: PDF file content as bytes
    """
    if not REPORTLAB_AVAILABLE:
        return _generate_fallback_pdf(booking, customer, photographer)

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30*mm,
        leftMargin=30*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )

    elements = []
    styles = getSampleStyleSheet()
    width = A4[0] - 60*mm  # available width

    # ─── Custom Styles ───
    title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Title'],
        fontSize=26,
        textColor=HexColor('#667eea'),
        spaceAfter=2*mm,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'InvoiceSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#888888'),
        spaceBefore=0,
        spaceAfter=6*mm,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=HexColor('#333333'),
        spaceBefore=6*mm,
        spaceAfter=3*mm,
        fontName='Helvetica-Bold',
        borderPadding=(0, 0, 2, 0),
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#444444'),
        leading=14
    )

    bold_style = ParagraphStyle(
        'CustomBold',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#222222'),
        fontName='Helvetica-Bold',
        leading=14
    )

    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=8,
        textColor=HexColor('#999999'),
        alignment=TA_CENTER,
        leading=11
    )

    right_bold = ParagraphStyle(
        'RightBold',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#222222'),
        fontName='Helvetica-Bold',
        alignment=TA_RIGHT,
        leading=14
    )

    right_normal = ParagraphStyle(
        'RightNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#444444'),
        alignment=TA_RIGHT,
        leading=14
    )

    # ─── Header ───
    elements.append(Paragraph('📸 BookMyShoot', title_style))
    elements.append(Paragraph('Your Moments, Our Passion', subtitle_style))
    elements.append(HRFlowable(width='100%', thickness=2, color=HexColor('#667eea'), spaceAfter=5*mm))

    # ─── Invoice Info ───
    invoice_date = datetime.now().strftime('%B %d, %Y')
    invoice_number = f'BMS-{booking.id:05d}'

    invoice_info = [
        [Paragraph('<b>INVOICE</b>', ParagraphStyle('', parent=styles['Heading1'], fontSize=18, textColor=HexColor('#333333'))),
         Paragraph(f'<b>Invoice #:</b> {invoice_number}<br/><b>Date:</b> {invoice_date}', right_normal)]
    ]
    t = Table(invoice_info, colWidths=[width*0.5, width*0.5])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 5*mm))

    # ─── Bill To / Photographer Info ───
    photographer_name = f"{photographer.user.first_name} {photographer.user.last_name}"

    bill_data = [
        [Paragraph('<b>BILL TO:</b>', bold_style), Paragraph('<b>PHOTOGRAPHER:</b>', bold_style)],
        [Paragraph(f'{customer.first_name} {customer.last_name}', normal_style),
         Paragraph(photographer_name, normal_style)],
        [Paragraph(f'{customer.email}', normal_style),
         Paragraph(f'{photographer.user.email}', normal_style)],
        [Paragraph(f'{customer.phone or "N/A"}', normal_style),
         Paragraph(f'{photographer.specialty or "Photography"}', normal_style)],
    ]
    bill_table = Table(bill_data, colWidths=[width*0.5, width*0.5])
    bill_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f8f9fa')),
        ('LINEBELOW', (0, 0), (-1, 0), 1, HexColor('#dee2e6')),
    ]))
    elements.append(bill_table)
    elements.append(Spacer(1, 6*mm))

    # ─── Booking Details ───
    elements.append(Paragraph('Booking Details', heading_style))
    elements.append(HRFlowable(width='100%', thickness=1, color=HexColor('#e9ecef'), spaceAfter=3*mm))

    event_date = booking.event_date.strftime('%B %d, %Y') if booking.event_date else 'TBD'
    event_time = booking.event_time or 'TBD'

    detail_data = [
        [Paragraph('<b>Detail</b>', bold_style), Paragraph('<b>Information</b>', bold_style)],
        [Paragraph('Booking ID', normal_style), Paragraph(f'#{booking.id}', normal_style)],
        [Paragraph('Event Type', normal_style), Paragraph(booking.service_type.title(), normal_style)],
        [Paragraph('Package', normal_style), Paragraph(booking.package_name or 'Standard', normal_style)],
        [Paragraph('Event Date', normal_style), Paragraph(event_date, normal_style)],
        [Paragraph('Event Time', normal_style), Paragraph(event_time, normal_style)],
        [Paragraph('Location', normal_style), Paragraph(booking.location or 'TBD', normal_style)],
        [Paragraph('Status', normal_style), Paragraph('Accepted ✅', bold_style)],
    ]

    detail_table = Table(detail_data, colWidths=[width*0.4, width*0.6])
    detail_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#ffffff'), HexColor('#f8f9fa')]),
    ]))
    elements.append(detail_table)
    elements.append(Spacer(1, 6*mm))

    # ─── Payment Summary ───
    elements.append(Paragraph('Payment Summary', heading_style))
    elements.append(HRFlowable(width='100%', thickness=1, color=HexColor('#e9ecef'), spaceAfter=3*mm))

    total_price = booking.total_price or 0
    token_amount = booking.token_amount or 0
    remaining_amount = booking.remaining_amount or 0

    payment_data = [
        [Paragraph('<b>Description</b>', bold_style), Paragraph('<b>Amount</b>', right_bold)],
        [Paragraph(f'{booking.service_type.title()} Photography – {booking.package_name or "Standard"} Package', normal_style),
         Paragraph(f'₹{total_price:,.2f}', right_normal)],
        [Paragraph('', normal_style), Paragraph('', right_normal)],  # spacer row
        [Paragraph('<b>Total Package Price</b>', bold_style),
         Paragraph(f'<b>₹{total_price:,.2f}</b>', right_bold)],
        [Paragraph('<b>Token Amount (Pay Now)</b>',
                   ParagraphStyle('', parent=bold_style, textColor=HexColor('#e63946'))),
         Paragraph(f'<b>₹{token_amount:,.2f}</b>',
                   ParagraphStyle('', parent=right_bold, textColor=HexColor('#e63946')))],
        [Paragraph('Remaining Amount (After Event)', normal_style),
         Paragraph(f'₹{remaining_amount:,.2f}', right_normal)],
    ]

    payment_table = Table(payment_data, colWidths=[width*0.65, width*0.35])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#ffc107')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#333333')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
        ('LINEABOVE', (0, 3), (-1, 3), 1.5, HexColor('#333333')),
        ('BACKGROUND', (0, 4), (-1, 4), HexColor('#fff3cd')),
        ('ROWBACKGROUNDS', (0, 1), (-1, 2), [HexColor('#ffffff'), HexColor('#f8f9fa')]),
    ]))
    elements.append(payment_table)
    elements.append(Spacer(1, 8*mm))

    # ─── Notes Section ───
    if booking.notes:
        elements.append(Paragraph('Special Notes', heading_style))
        elements.append(HRFlowable(width='100%', thickness=1, color=HexColor('#e9ecef'), spaceAfter=3*mm))
        elements.append(Paragraph(booking.notes, normal_style))
        elements.append(Spacer(1, 6*mm))

    # ─── Important Notice ───
    notice_style = ParagraphStyle(
        'Notice',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#856404'),
        backColor=HexColor('#fff3cd'),
        borderPadding=10,
        leading=14
    )
    elements.append(Paragraph(
        '<b>⚠️ Important:</b> Please pay the token amount of ₹{:,.2f} to confirm your booking. '
        'You can complete the payment through your BookMyShoot dashboard. '
        'The remaining amount of ₹{:,.2f} is due after the event.'.format(token_amount, remaining_amount),
        notice_style
    ))
    elements.append(Spacer(1, 10*mm))

    # ─── Footer ───
    elements.append(HRFlowable(width='100%', thickness=1, color=HexColor('#dee2e6'), spaceAfter=3*mm))
    elements.append(Paragraph(
        f'Thank you for choosing BookMyShoot! 📸<br/>'
        f'This is a computer-generated invoice and does not require a signature.<br/>'
        f'© {datetime.now().year} BookMyShoot. All rights reserved.',
        small_style
    ))

    # Build PDF
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def _generate_fallback_pdf(booking, customer, photographer):
    """
    Generate a simple text-based PDF if reportlab is not available.
    Uses a minimal PDF structure.
    """
    photographer_name = f"{photographer.user.first_name} {photographer.user.last_name}"
    event_date = booking.event_date.strftime('%B %d, %Y') if booking.event_date else 'TBD'
    
    content = f"""BookMyShoot - Invoice

Invoice #: BMS-{booking.id:05d}
Date: {datetime.now().strftime('%B %d, %Y')}

BILL TO:
{customer.first_name} {customer.last_name}
{customer.email}

PHOTOGRAPHER: {photographer_name}

BOOKING DETAILS:
- Booking ID: #{booking.id}
- Event Type: {booking.service_type.title()}
- Package: {booking.package_name or 'Standard'}
- Event Date: {event_date}
- Event Time: {booking.event_time or 'TBD'}  
- Location: {booking.location or 'TBD'}
- Status: Accepted

PAYMENT SUMMARY:
- Total Package Price: Rs.{booking.total_price:,.2f}
- Token Amount (Pay Now): Rs.{booking.token_amount:,.2f}
- Remaining (After Event): Rs.{booking.remaining_amount:,.2f}

Please pay the token amount to confirm your booking.
Thank you for choosing BookMyShoot!
"""
    # Encode as a very basic PDF
    pdf_lines = [
        b'%PDF-1.4',
        b'1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj',
        b'2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj',
        b'3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<</Font<</F1 4 0 R>>>>/Contents 5 0 R>>endobj',
        b'4 0 obj<</Type/Font/Subtype/Type1/BaseFont/Courier>>endobj',
    ]
    
    # Build text stream
    text_lines = content.split('\n')
    stream_content = 'BT /F1 10 Tf '
    y = 750
    for line in text_lines:
        safe_line = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        stream_content += f'1 0 0 1 50 {y} Tm ({safe_line}) Tj '
        y -= 14
        if y < 50:
            break
    stream_content += 'ET'
    
    stream_bytes = stream_content.encode('latin-1', errors='replace')
    pdf_lines.append(f'5 0 obj<</Length {len(stream_bytes)}>>stream\n'.encode() + stream_bytes + b'\nendstream\nendobj')
    pdf_lines.append(b'xref\n0 6')
    pdf_lines.append(b'trailer<</Size 6/Root 1 0 R>>')
    pdf_lines.append(b'startxref\n0')
    pdf_lines.append(b'%%EOF')
    
    return b'\n'.join(pdf_lines)

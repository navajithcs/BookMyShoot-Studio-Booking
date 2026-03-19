"""
Email Service for BookMyShoot
Sends booking confirmation emails with PDF invoice attachments.
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime


# ─── Email Configuration ───
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = os.getenv('BOOKMYSHOOT_EMAIL', 'bookmyshoot78@gmail.com')
SENDER_PASSWORD = os.getenv('BOOKMYSHOOT_EMAIL_PASSWORD', '7865800155537864')
SENDER_NAME = 'BookMyShoot'


def send_booking_accepted_email(booking, customer, photographer, pdf_bytes):
    """
    Send booking acceptance email to the customer with PDF invoice attached.
    
    Args:
        booking: Booking model instance
        customer: User model instance (the customer)
        photographer: Photographer model instance (with .user relationship)
        pdf_bytes: bytes of the generated PDF invoice
    """
    try:
        # Build the email
        msg = MIMEMultipart('mixed')
        msg['From'] = f'{SENDER_NAME} <{SENDER_EMAIL}>'
        msg['To'] = customer.email
        msg['Subject'] = f'🎉 Booking Accepted – Invoice #{booking.id} | BookMyShoot'

        # ─── HTML Email Body ───
        photographer_name = f"{photographer.user.first_name} {photographer.user.last_name}"
        event_date = booking.event_date.strftime('%B %d, %Y') if booking.event_date else 'TBD'
        event_time = booking.event_time or 'TBD'

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin:0; padding:0; background-color:#f4f4f4; font-family: 'Segoe UI', Arial, sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f4; padding:30px 0;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.1);">
                            
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding:35px 40px; text-align:center;">
                                    <h1 style="color:#ffffff; margin:0; font-size:28px; font-weight:700; letter-spacing:1px;">📸 BookMyShoot</h1>
                                    <p style="color:#e8e0ff; margin:8px 0 0; font-size:14px;">Your Moments, Our Passion</p>
                                </td>
                            </tr>

                            <!-- Success Banner -->
                            <tr>
                                <td style="background-color:#d4edda; padding:20px 40px; text-align:center; border-bottom:2px solid #c3e6cb;">
                                    <h2 style="color:#155724; margin:0; font-size:22px;">✅ Your Booking Has Been Accepted!</h2>
                                </td>
                            </tr>
                            
                            <!-- Greeting -->
                            <tr>
                                <td style="padding:30px 40px 10px;">
                                    <p style="color:#333; font-size:16px; line-height:1.6; margin:0;">
                                        Dear <strong>{customer.first_name} {customer.last_name}</strong>,
                                    </p>
                                    <p style="color:#555; font-size:15px; line-height:1.7; margin:15px 0 0;">
                                        Great news! Your photography session has been <strong style="color:#28a745;">accepted</strong> by 
                                        <strong>{photographer_name}</strong>. We're excited to help capture your special moments!
                                    </p>
                                </td>
                            </tr>

                            <!-- Booking Details Card -->
                            <tr>
                                <td style="padding:20px 40px;">
                                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f8f9fa; border-radius:10px; border:1px solid #e9ecef;">
                                        <tr>
                                            <td style="padding:20px 25px;">
                                                <h3 style="color:#495057; margin:0 0 15px; font-size:17px; border-bottom:2px solid #667eea; padding-bottom:10px;">📋 Booking Details</h3>
                                                <table width="100%" cellpadding="5" cellspacing="0">
                                                    <tr>
                                                        <td style="color:#6c757d; font-size:14px; width:40%;">Booking ID:</td>
                                                        <td style="color:#333; font-size:14px; font-weight:600;">#{booking.id}</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="color:#6c757d; font-size:14px;">Event Type:</td>
                                                        <td style="color:#333; font-size:14px; font-weight:600;">{booking.service_type.title()}</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="color:#6c757d; font-size:14px;">Package:</td>
                                                        <td style="color:#333; font-size:14px; font-weight:600;">{booking.package_name or 'Standard'}</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="color:#6c757d; font-size:14px;">Photographer:</td>
                                                        <td style="color:#333; font-size:14px; font-weight:600;">{photographer_name}</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="color:#6c757d; font-size:14px;">Event Date:</td>
                                                        <td style="color:#333; font-size:14px; font-weight:600;">{event_date}</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="color:#6c757d; font-size:14px;">Event Time:</td>
                                                        <td style="color:#333; font-size:14px; font-weight:600;">{event_time}</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="color:#6c757d; font-size:14px;">Location:</td>
                                                        <td style="color:#333; font-size:14px; font-weight:600;">{booking.location or 'TBD'}</td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <!-- Pricing Card -->
                            <tr>
                                <td style="padding:5px 40px 20px;">
                                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#fff3cd; border-radius:10px; border:1px solid #ffc107;">
                                        <tr>
                                            <td style="padding:20px 25px;">
                                                <h3 style="color:#856404; margin:0 0 15px; font-size:17px;">💰 Payment Summary</h3>
                                                <table width="100%" cellpadding="5" cellspacing="0">
                                                    <tr>
                                                        <td style="color:#6c757d; font-size:14px;">Total Package Price:</td>
                                                        <td style="color:#333; font-size:14px; font-weight:600; text-align:right;">₹{booking.total_price:,.2f}</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="color:#856404; font-size:15px; font-weight:700;">Token Amount (to pay now):</td>
                                                        <td style="color:#856404; font-size:15px; font-weight:700; text-align:right;">₹{booking.token_amount:,.2f}</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="color:#6c757d; font-size:14px;">Remaining (pay after event):</td>
                                                        <td style="color:#333; font-size:14px; font-weight:600; text-align:right;">₹{booking.remaining_amount:,.2f}</td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <!-- Next Step CTA -->
                            <tr>
                                <td style="padding:10px 40px 25px; text-align:center;">
                                    <p style="color:#333; font-size:15px; margin:0 0 15px;">
                                        🔔 <strong>Next Step:</strong> Please pay the token amount of 
                                        <strong style="color:#e63946;">₹{booking.token_amount:,.2f}</strong> to confirm your booking.
                                    </p>
                                    <p style="color:#555; font-size:13px; margin:0;">
                                        Log in to your BookMyShoot dashboard to complete the payment.
                                    </p>
                                </td>
                            </tr>

                            <!-- PDF Note -->
                            <tr>
                                <td style="padding:0 40px 25px; text-align:center;">
                                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#e8f4fd; border-radius:8px; border:1px solid #bee5eb;">
                                        <tr>
                                            <td style="padding:15px 20px; text-align:center;">
                                                <p style="color:#0c5460; font-size:14px; margin:0;">
                                                    📎 <strong>Invoice attached as PDF.</strong> You can download and save it for your records.
                                                </p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="background-color:#2d3436; padding:25px 40px; text-align:center;">
                                    <p style="color:#b2bec3; font-size:13px; margin:0;">
                                        Thank you for choosing <strong style="color:#fff;">BookMyShoot</strong> 📸
                                    </p>
                                    <p style="color:#636e72; font-size:12px; margin:8px 0 0;">
                                        This is an automated email. Please do not reply directly.
                                    </p>
                                    <p style="color:#636e72; font-size:11px; margin:8px 0 0;">
                                        &copy; {datetime.now().year} BookMyShoot. All rights reserved.
                                    </p>
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        # Attach the HTML body
        html_part = MIMEText(html_body, 'html', 'utf-8')
        msg.attach(html_part)

        # Attach the PDF invoice
        pdf_attachment = MIMEApplication(pdf_bytes, _subtype='pdf')
        pdf_attachment.add_header(
            'Content-Disposition', 'attachment',
            filename=f'BookMyShoot_Invoice_{booking.id}.pdf'
        )
        msg.attach(pdf_attachment)

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"[EMAIL] Booking acceptance email sent to {customer.email} for Booking #{booking.id}")
        return True

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email to {customer.email}: {e}")
        return False


def send_booking_cancelled_email(booking, customer, photographer, reason=None):
    """
    Send booking cancellation email to the customer when photographer cancels.
    """
    try:
        msg = MIMEMultipart('mixed')
        msg['From'] = f'{SENDER_NAME} <{SENDER_EMAIL}>'
        msg['To'] = customer.email
        msg['Subject'] = f'⚠️ Booking Cancelled – #{booking.id} | BookMyShoot'

        photographer_name = f"{photographer.user.first_name} {photographer.user.last_name}"
        event_date = booking.event_date.strftime('%B %d, %Y') if booking.event_date else 'TBD'
        
        reason_html = f"<p style='color:#e63946; font-size:15px; margin:15px 0 0;'><strong>Reason for cancellation:</strong> {reason}</p>" if reason else ""

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin:0; padding:0; background-color:#f4f4f4; font-family: 'Segoe UI', Arial, sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f4; padding:30px 0;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 20px rgba(0,0,0,0.1);">
                            
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #e63946 0%, #d62828 100%); padding:35px 40px; text-align:center;">
                                    <h1 style="color:#ffffff; margin:0; font-size:28px; font-weight:700; letter-spacing:1px;">📸 BookMyShoot</h1>
                                </td>
                            </tr>

                            <!-- Cancellation Banner -->
                            <tr>
                                <td style="background-color:#fff5f5; padding:20px 40px; text-align:center; border-bottom:2px solid #feb2b2;">
                                    <h2 style="color:#c53030; margin:0; font-size:22px;">Booking Cancelled by Photographer</h2>
                                </td>
                            </tr>
                            
                            <!-- Greeting -->
                            <tr>
                                <td style="padding:30px 40px 10px;">
                                    <p style="color:#333; font-size:16px; line-height:1.6; margin:0;">
                                        Dear <strong>{customer.first_name} {customer.last_name}</strong>,
                                    </p>
                                    <p style="color:#555; font-size:15px; line-height:1.7; margin:15px 0 0;">
                                        We regret to inform you that <strong>{photographer_name}</strong> has cancelled your {booking.service_type} booking for <strong>{event_date}</strong>.
                                    </p>
                                    {reason_html}
                                    <p style="color:#555; font-size:15px; line-height:1.7; margin:15px 0 0;">
                                        If you have paid a token amount, a refund request has been automatically initiated. Our team will process it shortly.
                                    </p>
                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="background-color:#2d3436; padding:25px 40px; text-align:center;">
                                    <p style="color:#b2bec3; font-size:13px; margin:0;">
                                        We apologize for the inconvenience. <strong style="color:#fff;">BookMyShoot</strong> 📸
                                    </p>
                                    <p style="color:#636e72; font-size:11px; margin:8px 0 0;">
                                        &copy; {datetime.now().year} BookMyShoot. All rights reserved.
                                    </p>
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html', 'utf-8'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send cancellation email: {e}")
        return False

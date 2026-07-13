from celery import Celery
from models import User, Trek, Booking
from mail import send_email , send_email_with_attachment
from celery.schedules import crontab
import csv
import io


celery = Celery(
    "trekcentral",
    broker="redis://localhost:6379/0"
)

celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False,
)

from app import app as flask_app

@celery.task
def send_daily_reminders():

    with flask_app.app_context():

        users = User.query.filter_by(role='user' , is_blacklisted=False).all()
        trek_html = ""
        upcoming_treks = Trek.query.filter_by(status='Approved').all()

        if upcoming_treks:
            for trek in upcoming_treks:
                trek_html += f"""
                        <hr>
                        <p>Here are some upcoming adventures waiting for you.</p>
                        <br>
                        <h3>{trek.name}</h3>

                        <p><b>📍 Location:</b> {trek.location}</p>

                        <p><b>📅 Starts:</b> {trek.start_date.strftime("%d %B %Y")}</p>

                        <p><b>📅 Ends:</b> {trek.end_date.strftime("%d %B %Y")}</p>
                        
                        <p><b>⛰ Difficulty:</b> {trek.difficulty}</p>
                        
                        <p><b>💰 Price:</b> ₹{trek.price}</p>
                        
                        <br>
                        
                        <p>Don't miss your next adventure.</p>
                        <p>Visit TrekCentral and reserve your slot today!</p>

                        
                        """
        else:
            trek_html = """
            <br>
            <p>No upcoming treks are available right now.</p>
            <p>We're constantly adding exciting adventures.</p>
            <p>Stay tuned for exciting adventures!</p>
            """             
        
        for user in users:
            html = f"""
            <html>
                <body>
                    <h2>TrekCentral Daily Reminder</h2>
                    
                        <p>Hello, {user.fullname}!</p>

                        <p>Hope you're having a great day!</p>
                        {trek_html}
                        <br>
                        <p>Happy Trekking!</p>
                        <p><b>Team TrekCentral</b></p>
                        <br>
                </body>
            </html>
            """
            try:
                send_email(user.email,"TrekCentral Daily Reminder",html)
            except Exception as e:
                print("Failed to send daily reminder email to user:", user.email, e)
                continue
    
    return "Reminder emails sent successfully."


@celery.task
def send_monthly_reminders_admin():
    with flask_app.app_context():
        admin = User.query.filter_by(role='admin').first()
        
        
        conducted_treks = Trek.query.filter(Trek.status.in_(['Started', 'Completed'])).all()
        total_treks_conducted = len(conducted_treks)
        
        contributed_treks = Trek.query.filter(Trek.status.in_(['Open','Closed','Started', 'Completed'])).all()
        
        total_users = User.query.filter_by(role='user').count()
        blacklisted_users = User.query.filter_by(role='user', is_blacklisted=True).count()

        total_staff = User.query.filter_by(role='staff').count()
        blacklisted_staff = User.query.filter_by(role='staff', is_blacklisted=True).count()
        
        total_treks = Trek.query.filter(Trek.status != 'Pending').count()
        pending_treks = Trek.query.filter_by(status='Pending').count()
        
        total_participants = 0
        total_revenue = 0
        popular_trek_name = "No treks conducted yet"
        highest_booking_count = 0

        for trek in contributed_treks:
            booked_count = len([b for b in trek.bookings if b.status == 'Booked'])

            total_participants += booked_count
            total_revenue += trek.price * booked_count

            if booked_count > highest_booking_count:
                highest_booking_count = booked_count
                popular_trek_name = trek.name
                
        html = f"""
        
        <html>
            <body>
                <h2>TrekCentral Monthly Activity Report</h2>

                <p>Hello, {admin.fullname}!</p>
                <p>Here's a summary of TrekCentral's activity so far.</p>

                <hr>

                <h3>Trek Overview</h3>
                <p><b>🏔 Total Treks Conducted(Completed or Started):</b> {total_treks_conducted}</p>
                <p><b>📋 Total Active Treks (Assigned):</b> {total_treks}</p>
                <p><b>⏳ Pending Treks (Unassigned):</b> {pending_treks}</p>

                <hr>

                <h3>Participation & Revenue</h3>
                <p><b>👥 Total Participants:</b> {total_participants}</p>
                <p><b>💰 Total Revenue:</b> ₹{total_revenue}</p>
                <p><b>⭐ Most Popular Trek:</b> {popular_trek_name} ({highest_booking_count} bookings)</p>

                <hr>

                <h3>User & Staff Overview</h3>
                <p><b>🧑 Total Users:</b> {total_users}</p>
                <p><b>🚫 Blacklisted Users:</b> {blacklisted_users}</p>
                <p><b>🧑‍✈️ Total Staff:</b> {total_staff}</p>
                <p><b>🚫 Blacklisted Staff:</b> {blacklisted_staff}</p>

                <br>
                <p>Keep up the great work!</p>
                <p><b>Team TrekCentral</b></p>
            </body>
        </html>
        """

        try:
            send_email(admin.email, "TrekCentral Monthly Activity Report", html)
            return "Monthly report sent successfully."
        except Exception as e:
            print("Failed to send monthly report to admin:", admin.email, e)
            return "Failed to send monthly report."

    
            
        
celery.conf.beat_schedule = {
    "daily-reminders": { "task": "celery_app.send_daily_reminders", "schedule": crontab(hour=1, minute=40) },
    "monthly-reminders-admin": { "task": "celery_app.send_monthly_reminders_admin", "schedule": crontab(day_of_month=14, hour=1, minute=40) }
}



@celery.task
def export_user_bookings_csv(user_id):

    with flask_app.app_context():
        user = User.query.get(user_id)
        if not user:
            return "User not found."

        bookings = Booking.query.filter_by(user_id=user_id).all()
        
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)

        writer.writerow(['Booking ID', 'Trek Name', 'Location', 'Difficulty', 'Start Date', 'End Date', 'Booking Date', 'Status'])

        for booking in bookings:
            trek = booking.trek
            writer.writerow([
                booking.id,
                trek.name,
                trek.location,
                trek.difficulty,
                trek.start_date.strftime("%d %B %Y"),
                trek.end_date.strftime("%d %B %Y"),
                booking.booking_date.strftime("%d %B %Y"),
                booking.status
            ])

        csv_data = csv_buffer.getvalue()
        
        html = f"""
        <html>
            <body>
                <h2>Your Trekking History Export</h2>
                <p>Hello, {user.fullname}!</p>
                <p>Your requested trekking history export is ready and attached to this email as a CSV file.</p>
                <br>
                <p><b> Please click on MIME section of the email and download the  application/octet-stream attachment for you CSV file.</b></p>
                <br>
                <p>Happy Trekking!</p>
                <p><b>Team TrekCentral</b></p>
            </body>
        </html>
        """

        try:
            send_email_with_attachment( user.email,  "TrekCentral - Your Trekking History Export", html, csv_data.encode('utf-8'), 'trekking_history.csv')
            return "CSV export sent successfully."
        except Exception as e:
            print("Failed to send CSV export to user:", user.email, e)
            return "Failed to send CSV export."
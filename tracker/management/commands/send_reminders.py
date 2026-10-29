from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from tracker.models import Medicine

class Command(BaseCommand):
    help = 'Checks for active medicine schedules matching current hour and minute, then sends email reminders.'

    def handle(self, *args, **options):
        # Get current local time using TIME_ZONE setting ('Africa/Nairobi')
        now = timezone.localtime()
        current_hour = now.hour
        current_minute = now.minute

        # Query active medicines scheduled for this exact hour and minute
        medicines = Medicine.objects.filter(
            reminder_enabled=True,
            reminder_time__hour=current_hour,
            reminder_time__minute=current_minute
        ).select_related('user')

        count = 0
        for medicine in medicines:
            user_email = medicine.user.email
            if user_email:
                subject = f"💊 Reminder: Time to take your {medicine.name}"
                message = (
                    f"Hello {medicine.user.username},\n\n"
                    f"This is your scheduled reminder to take:\n"
                    f"• Medicine: {medicine.name}\n"
                    f"• Dosage: {medicine.dosage}\n"
                    f"• Frequency: {medicine.frequency}\n\n"
                    f"Stay healthy,\nMedTrack Team"
                )
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user_email],
                    fail_silently=False,  # Raises visible exceptions if Gmail SMTP fails
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully sent {count} medicine reminder(s) at {now.strftime("%H:%M")}.'))
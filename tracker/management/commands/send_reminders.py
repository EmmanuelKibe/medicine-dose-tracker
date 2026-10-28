from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from tracker.models import Medicine

class Command(BaseCommand):
    help = 'Checks for active medicine schedules matching current hour and sends email reminders.'

    def handle(self, *args, **options):
        current_time = datetime.now().time()
        current_hour = current_time.hour
        current_minute = current_time.minute

        # Find medicines matching the current hour and minute
        medicines = Medicine.objects.filter(
            reminder_enabled=True,
            reminder_time__hour=current_hour,
            reminder_time__minute=current_minute
        ).select_related('user')

        count = 0
        for medicine in medicines:
            if medicine.user.email:
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
                    [medicine.user.email],
                    fail_silently=True,
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully sent {count} medicine reminder(s).'))
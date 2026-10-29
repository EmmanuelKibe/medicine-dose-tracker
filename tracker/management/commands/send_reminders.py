from django.utils import timezone
from tracker.models import Medicine

class Command(BaseCommand):
    help = 'Sends email reminders'

    def handle(self, *args, **options):
        # Get local time based on TIME_ZONE setting in settings.py
        now = timezone.localtime()
        
        # Query active reminders for the current hour and minute
        medicines = Medicine.objects.filter(
            reminder_enabled=True,
            reminder_time__hour=now.hour,
            reminder_time__minute=now.minute
        ).select_related('user')

        count = 0
        for medicine in medicines:
            if medicine.user.email:
                send_mail(
                    subject=f"💊 Reminder: Time to take {medicine.name}",
                    message=f"Hello {medicine.user.username},\n\nIt's time to take your {medicine.name} ({medicine.dosage}).",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[medicine.user.email],
                    fail_silently=False  # Raises error if SMTP fails
                )
                count += 1

        self.stdout.write(f"Processed {count} reminder(s) at {now.strftime('%H:%M:%S')}")
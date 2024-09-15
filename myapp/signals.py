import threading
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        # Print the current thread to demonstrate signals run in the same thread as the caller
        print(f"Signal handler running in thread: {threading.current_thread().name}")

        # Demonstrate synchronous execution by delaying the handler
        print(f"Signal handler: User {instance.username} created")
        time.sleep(5)  # Simulate a long-running task
        print("Signal handler done after 5 seconds")

        # The signal is fired regardless of whether the transaction is rolled back
        print("Signal handler completed.")

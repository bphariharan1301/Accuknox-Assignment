from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.db import transaction
import threading


def create_user(request):
    # Print the current thread to demonstrate that the view and signal handler run in the same thread
    print(f"View running in thread: {threading.current_thread().name}")

    try:
        # Start a transaction
        with transaction.atomic():
            print("Starting user creation process...")

            # Create a user (this will trigger the post_save signal)
            user = User.objects.create(username=threading.current_thread().name + "1")

            print(
                "User creation process finished, but before committing transaction..."
            )

            # Simulate an error to roll back the transaction based on a query parameter
            if request.GET.get("fail", "no") == "yes":
                raise Exception("Simulating an error to roll back the transaction")

    except Exception as e:
        print(f"Exception occurred: {e}")
        return HttpResponse("Transaction failed, user was not created!")

    # If no exception occurs, the transaction commits successfully
    return HttpResponse("User created successfully!")

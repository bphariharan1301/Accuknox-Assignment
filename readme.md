# Django Signals Demonstration

This document answers the following questions:

1. By default, are Django signals executed synchronously or asynchronously?
2. Do Django signals run in the same thread as the caller?
3. By default, do Django signals run in the same database transaction as the caller?

---

## Question 1: Are Django signals executed synchronously or asynchronously?

**Answer**: By default, Django signals are executed **synchronously**. This means that the signal handler runs immediately after the signal is triggered, blocking the flow of the calling thread until the signal handler completes.

### Code Snippet:

In the following code, the signal handler is delayed by `time.sleep(5)` to simulate a long-running task. This demonstrates that the signal blocks the caller thread, proving it is executed synchronously.

### `signals.py`

```python
import threading
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        # Simulate a long-running task with sleep
        print(f"Signal handler: User {instance.username} created")
        time.sleep(5)  # Delay to simulate synchronous execution
        print("Signal handler done after 5 seconds")
```

## Question 2: Do Django signals run in the same thread as the caller?

**Answer**: Yes, Django signals run in the **same thread** as the caller. To prove this, both the view and the signal handler print the current thread they are running on, which will show that they are running on the same thread.

### Code Snippet:

### `signals.py`

```python
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"Signal handler running in thread: {threading.current_thread().name}")
        print(f"Signal handler: User {instance.username} created")
```

### `views.py`

```python
import threading
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User

def create_user(request):
    print(f"View running in thread: {threading.current_thread().name}")
    print("Starting user creation process...")
    user = User.objects.create(username="testuser")
    print("User creation process finished.")
    return HttpResponse("User created successfully!")
```

## Question 3: By default, do Django signals run in the same database transaction as the caller?

**Answer**: By default, Django signals do **not** run in the same database transaction as the caller. This means the signal handler runs even if the transaction that triggered the signal is not committed. To run signals in the same transaction, Django provides the `transaction.on_commit()` hook.

### Code Snippet:

### `signals.py`

```python
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models.User

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"Signal handler running in thread: {threading.current_thread().name}")
        print(f"Signal handler: User {instance.username} created")
```

### `views.py`

```python
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.db import transaction
import threading

def create_user(request):
    print(f"View running in thread: {threading.current_thread().name}")

    try:
        # Start a transaction
        with transaction.atomic():
            print("Starting user creation process...")

            # Create a user (this will trigger the post_save signal)
            user = User.objects.create(username="transactiontestuser")

            print("User creation process finished, but before committing transaction...")

            # Simulate an error to roll back the transaction based on a query parameter
            if request.GET.get('fail', 'no') == 'yes':
                raise Exception("Simulating an error to roll back the transaction")

    except Exception as e:
        print(f"Exception occurred: {e}")
        return HttpResponse("Transaction failed, user was not created!")

    # If no exception occurs, the transaction commits successfully
    return HttpResponse("User created successfully!")
```

Here is the corrected version of your example scenarios:

## Example Scenarios:

### 1. Successful User Creation:

Visit the URL without the `fail` parameter, or set it to `no`:

```url
http://127.0.0.1:8000/create-user/
```

or

```url
http://127.0.0.1:8000/create-user/?fail=no
```

### 2. Failed User Creation (Transaction Rolled Back):

Visit the URL with `fail=yes` to simulate a failure and trigger the transaction rollback:

```url
http://127.0.0.1:8000/create-user/?fail=yes
```

## Expected Terminal Output:

```bash
View running in thread: MainThread
Starting user creation process...
Signal handler running in thread: MainThread
Signal handler: User transactiontestuser created
Exception occurred: Simulating an error to roll back the transaction
```

### This output shows:

1. **Synchronous execution**: The `sleep(5)` in the signal handler delays further execution in the view.
2. **Same thread**: Both the view and the signal handler are executed in the `MainThread`.
3. **Signal outside transaction**: The signal handler runs even though the transaction is rolled back, indicating that signals are triggered regardless of the success of the database transaction.

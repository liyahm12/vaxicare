import threading
import time


def start_notification_thread():

    from .notification import check_all_notifications

    def run():

        while True:

            try:
                check_all_notifications()

            except Exception as e:
                print("Notification error:", e)

            # For testing: check every 1 minute
            time.sleep(60)

    thread = threading.Thread(
        target=run,
        daemon=True
    )

    thread.start()
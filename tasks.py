
from django.conf import settings
import time
import datetime
from SobujPrithibi_Quiz.models import *
from SobujPrithibi_Quiz.utils import *


def runTasks(init=0):
    print("Scheduled Task Started")
    try:
        with transaction.atomic(durable=True):
            otp_exp = zonetime.now() - datetime.timedelta(minutes=settings.OTP_VALID_FOR)
            OTP.objects.filter(created_at__lte=otp_exp).delete()
            link_exp = zonetime.now() - datetime.timedelta(minutes=settings.LINK_VALID_FOR)
            ResetPasswordLink.objects.filter(created_at__lte=link_exp).delete()
        print("Scheduled Task Completed")
        return True
    except Exception as e:
        init += 1
        traceback.print_exc()
        print("\n\n")
        if init <= 3:
            runTasks(init)  # if failed run again till 3 times.
        print("Scheduled Task Completed")
        return False
    

# if __name__ == "__main__":
#     runTasks()
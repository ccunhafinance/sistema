from celery import shared_task


@shared_task
def rr(request):
    print('oi')


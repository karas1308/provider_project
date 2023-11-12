# # Create your views here.
#
# import time
#
# import schedule
#
# from celery_tasks import check_balances_and_notify
#
# schedule.every().day.at("10:00").do(check_balances_and_notify)
#
#
# def run_schedule():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
#
# if __name__ == '__main__':
#     from multiprocessing import Process
#
#     schedule_process = Process(target=run_schedule)
#     schedule_process.start()
#     schedule_process.join()

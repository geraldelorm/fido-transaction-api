from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.crud.analytics_service import compute_and_store_analytics

scheduler = AsyncIOScheduler()

#Schedule the job to run every 30 minutes
def start_scheduler():
    scheduler.add_job(compute_and_store_analytics, 'interval', hours=0.005)
    scheduler.start()
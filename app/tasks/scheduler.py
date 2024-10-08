from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.crud.analytics_service import compute_and_store_analytics

scheduler = AsyncIOScheduler()

#Schedule the job to run every 15 minutes
def start_scheduler():
    scheduler.add_job(compute_and_store_analytics, 'interval', hours=0.025)
    scheduler.start()
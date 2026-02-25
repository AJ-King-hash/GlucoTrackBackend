from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from repositories import NotificationRepo
from datetime import datetime,timedelta, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import firebase_admin
import models
import json
from firebase_admin import credentials, messaging
from schemas import FCMTokenUpdate,UserReminderUpdate
router=APIRouter(
    prefix="/notification",
    tags=["Notifications"]
)

cred = credentials.Certificate("firebase-service-account.json")
firebase_admin.initialize_app(cred)



scheduler=AsyncIOScheduler()

async def send_reminders():
    now = datetime.now(timezone.utc)
    db = SessionLocal()
    try:
        # Medicine reminders
        medicine_users = db.query(models.User).filter(
            models.User.medicine_reminder <= now,
            models.User.medicine_reminder.isnot(None),
            models.User.fcm_token.isnot(None)
        ).all()
        for user in medicine_users:
            try:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="Medicine Reminder",
                        body="It's time to take your medicine!"
                    ),
                    token=user.fcm_token
                )
                messaging.send(message)
                user.medicine_reminder += timedelta(days=1)
            except Exception as e:
                print(f"Error sending to {user.id}: {e}")
        
        # Glucose reminders
        gluco_users = db.query(models.User).filter(
            models.User.gluco_reminder <= now,
            models.User.gluco_reminder.isnot(None),
            models.User.fcm_token.isnot(None)
        ).all()
        for user in gluco_users:
            try:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title="Blood Glucose Reminder",
                        body="Time to check your blood sugar (تحليل سكر الدم)!"
                    ),
                    token=user.fcm_token
                )
                messaging.send(message)
                user.gluco_reminder += timedelta(days=1)
            except Exception as e:
                print(f"Error sending to {user.id}: {e}")
        
        db.commit()
    finally:
        db.close()

@router.get("/trigger-reminders") 
async def trigger(): 
    await send_reminders();
    return {"done": True}

@router.on_event("startup")
async def startup():
    scheduler.add_job(send_reminders, IntervalTrigger(minutes=1))  # Check every minute
    scheduler.start()

@router.on_event("shutdown")
async def shutdown():
    scheduler.shutdown()


@router.put("/{user_id}/reminders")
def set_reminders(user_id: int, reminder: UserReminderUpdate, db: Session = Depends(get_db)):
    updated_user = NotificationRepo.update_reminders(db, user_id, reminder.gluco_time, reminder.medicine_time, reminder.timezone)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Reminders updated"}

@router.post("/{user_id}/fcm-token")
def set_fcm_token(user_id: int, token: FCMTokenUpdate, db: Session = Depends(get_db)):
    updated_user = NotificationRepo.update_fcm_token(db, user_id, token.fcm_token)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "FCM token updated"}
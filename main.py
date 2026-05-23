from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# قاعدة بيانات تخيلية للمستخدمين ورصيدهم (بالدولار)
# المستخدم رقم 1 معاه 10 دولار، والمستخدم رقم 2 معاه 0.10 دولار
USERS_DB = {
    1: {"username": "ahmed", "wallet_balance": 10.00},
    2: {"username": "mohamed", "wallet_balance": 0.10}
}

# سِجل العمليات التخيلي
TRANSACTIONS_LOG = []
class VideoRequest(BaseModel):
    user_id: int
    prompt: str

VIDEO_PRICE = 0.25  # سعر الفيديو 25 سنت مثلاً

@app.post("/generate-video")
async def generate_video(request: VideoRequest):
    # 1. التأكد من وجود المستخدم
    if request.user_id not in USERS_DB:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
        
    user = USERS_DB[request.user_id]
    
    # 2. التأكد من أن الرصيد كافي
    if user["wallet_balance"] < VIDEO_PRICE:
        raise HTTPException(
            status_code=402, 
            detail=f"رصيدك الحالي ({user['wallet_balance']}$) غير كافٍ. تكلفة الفيديو {VIDEO_PRICE}$"
        )
        
    # 3. خصم المبلغ مؤقتاً
    user["wallet_balance"] -= VIDEO_PRICE
    
    # 4. تسجيل العملية
    TRANSACTIONS_LOG.append({
        "user_id": request.user_id,
        "amount": -VIDEO_PRICE,
        "status": "success"
    })
    
    # 5. رد السيرفر بنجاح الخصم (وهنا هنربط موديل الفيديو لاحقاً)
    return {
        "status": "success",
        "message": "تم خصم التكلفة وجاري توليد الفيديو الخاص بك...",
        "remaining_balance": f"{user['wallet_balance']}$"
    }

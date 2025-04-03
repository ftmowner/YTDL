import motor.motor_asyncio
import datetime
from info import MONGO_URI, MONGO_NAME, DAILY_LIMITS, LOG_CHANNEL

class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[MONGO_NAME]
        self.col = self.db["users"]
        self.downloads_collection = self.db["downloads"]

    def new_user(self, id, name):
        return {
            "user_id": int(id),
            "name": name,
            "joined_at": datetime.datetime.utcnow(),
            "user_type": "free",
            "tasks_used": 0,      
            "last_reset": datetime.datetime.utcnow().strftime("%Y-%m-%d")
        }
        
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):      
        user = await self.col.find_one({"user_id": int(id)})
        return bool(user)


    async def reset_daily_tasks(self, bot):
        await self.col.update_many({}, {"$set": {"tasks_used": 0}})
        await bot.send_message(LOG_CHANNEL, "🔄 **Daily task limits have been reset for all users!** ✅ ")

    
    async def check_task_limit(self, user_id):
        user = await self.col.find_one({"user_id": user_id}, {"tasks_used": 1, "user_type": 1}, limit=1)
    
        if not user:  # User agar exist nahi karta
            return True  # ✅ Allow task

        if user.get("user_type") == "premium":
            return True  # ✅ Premium users ke liye unlimited tasks

        return user.get("tasks_used", 0) < DAILY_LIMITS  # ✅ Free users ke liye limit check


    async def increment_task(self, user_id):
        """User ka task count +1 karega"""
        result = await self.col.update_one(
            {"user_id": int(user_id)},  
            {"$inc": {"tasks_used": 1}},  
            upsert=True  
        )
        return result.modified_count > 0
        
    
    async def increment_download_count(self):
        await self.downloads_collection.update_one(
            {}, 
            {"$setOnInsert": {"total_downloads": 0}},
            upsert=True
        )
        
        await self.downloads_collection.update_one({}, {"$inc": {"total_downloads": 1}})

    async def get_all_users(self):
        return self.col.find({})

    async def get_total_downloads(self):  
        result = await self.db["downloads"].find_one({}, {"total_downloads": 1})
        if result:
            return result.get("total_downloads", 0)
        return 0
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def block_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def save_thumbnail(self, user_id, file_id):
        """Save the thumbnail file_id for a user"""
        existing_user = await self.col.find_one({"user_id": int(user_id)})
        
        if existing_user:
            # If user exists, update their thumbnail
            await self.col.update_one(
                {"user_id": int(user_id)},
                {"$set": {"thumbnail": file_id}}
            )
        else:
            user_data = self.new_user(user_id, "Unknown")
            user_data["thumbnail"] = file_id
            await self.col.insert_one(user_data)

    async def get_user_thumbnail(self, user_id):
        """Get the user's thumbnail file_id"""
        user = await self.col.find_one({"user_id": int(user_id)})
        if user and "thumbnail" in user:
            return user["thumbnail"]
        return None

    async def remove_thumbnail(self, user_id):
        """Remove user's thumbnail (soft delete)"""
        result = await self.col.update_one(
            {"user_id": int(user_id)},
            {"$unset": {"thumbnail": ""}}
        )
        return result.modified_count > 0

db = Database()

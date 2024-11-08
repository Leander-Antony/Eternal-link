from pymongo import MongoClient

uri = "***************************************"
try:
    client = MongoClient(uri)
    # client = MongoClient('mongodb://localhost:27017/') 
    db = client['fate'] 
    collection = db['fate']  
    data = {"message": "data"}  
    collection.insert_one(data)  
    print("Connected to MongoDB and document inserted!")
except Exception as e:
    print(f"Connection failed: {e}")

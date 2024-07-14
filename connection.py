from pymongo import MongoClient
MONGO_URI = "mongodb+srv://admin:admin12345678@cluster0.2her3q6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['therapy']


collection = db['therapist']

import uvicorn, random, pymongo, string, time, argon2, jwt, uuid as uuid_lib
from datetime import datetime, timedelta
from fastapi import FastAPI
from pydantic import BaseModel

#TODO: fix error codes


config = {
    # "domain": "zeppellin.neralaiko.lt",
    "domain": "127.0.0.1",
    # "school_domain": "@jurgucioprogimnazija.lt",
    "school_domain": "@gmail.com",
    "force_school_domain": True
}


mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["Zeppellin"]
pass_hasher = argon2.PasswordHasher()
app = FastAPI()


SECRET_KEY = "19af3f10a75b525537ba2eb275bff44c59563a2f94aa39653e71908c61cdae4d" #NOTE: For testing



class Token(BaseModel):
    access_token: str
    token_type: str

class auth_man:
    def __init__(self, email: str, password: str, created: int = 0, mongo_db = None, edited: int = 0) -> None:
        self.email = email
        self.password = password
        self.created = created
        self.mongo_db = mongo_db
        
        if created != 0 and edited == 0: self.edited = created
        else: self.edited = edited
        if created == 0: created = list(mongo_db["users"].find({'email': self.email}))[0]["created"]

    def gen_salt(self):
        return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8))
    
    def verify_format(self):
        if self.email != config["school_domain"] and self.email.endswith(config["school_domain"]):
            if self.password != None:
                if self.password.isascii():
                    if len(self.password) > 7: 
                        if any(char in self.password for char in string.punctuation + string.digits):
                            return {"success": True, "error_code": False, "message": "", "content": False}
                        else: return {"success": False, "error_code": 0, "message": "Password must contain a number or symbol", "content": False}
                    else: return {"success": False, "error_code": 1, "message": "Password must be at least 8 characters long", "content": False}
                else: return {"success": False, "error_code": 3, "message": "Password must only contain ASCII symbols", "content": False}
            else: return {"success": False, "error_code": 2, "message": "Please specify a password! (Must concist of 8 characters, 1 symbol or number)", "content": False}
        elif self.email == config["school_domain"]: return {"success": False, "error_code": 0, "message": "E-Mail must be specified"}
        elif not self.email.endswith(config["school_domain"]): return {"success": False, "error_code": 1, "message": f"E-Mail must be from your school ({config['school_domain']})"}

    def gen_hash(self):
        pass_format_verify = self.verify_format()
        if pass_format_verify["success"]:
            self.salt = self.gen_salt()
            self.hash = pass_hasher.hash(f"{self.created}|{self.email}-{self.salt}|{self.password}|{self.edited}")
            return {"success": True, "error_code": False, "message": "", "content": {"hash": self.hash, "salt": self.salt, "created": self.created, "edited": self.edited}}
        else:
            return pass_format_verify
    
    def verify_hash(self):
        users = list(mongo_db["users"].find({'email': self.email}))
        if users:
            pass_format_verify = self.verify_format()
            if pass_format_verify["success"]:
                user = users[0]
                try:
                    if pass_hasher.verify(user['hash'], f"{user['created']}|{user['email']}-{user['salt']}|{self.password}|{user['edited']}"): 
                        return {"success": True, "error_code": False, "message": "Logged in successfully", "content": False}
                    else: return {"success": False, "error_code": False, "message": "Password invalid", "content": False}
                except argon2.exceptions.InvalidHash: return {"success": False, "error_code": False, "message": "Password invalid", "content": False}
            else: return pass_format_verify
        else: return {"success": False, "error_code": 1, "message": f"Such account doesn't exist!"}

    
    def gen_uuid(self):
        gen_uuid = True
        while gen_uuid:
            uuid = str(uuid_lib.uuid4())
            if list(self.mongo_db["users"].find({'UUID': uuid})) == []: gen_uuid = False  
        return uuid

    
    def return_token(self):
        encoded = jwt.encode({"email": self.email, "UUID": ""}, SECRET_KEY, algorithm="RS256")


        

class User_Item(BaseModel):  
    email: str | None = config["school_domain"]
    UUID: str | None = None
    password: str | None = None
    tos_pirvacy_accepted: bool | None = None #Used ONLY when registering, just in case someone creates an API call outside of the frontend - using the API.



@app.post("/register")
async def register_user(user: User_Item):         #TODO: Implement sessions, cookies, 2FA 
    if user.tos_pirvacy_accepted:                                         
            if list(mongo_db["users"].find({'email': user.email})) == []: #If no users are found
                timestamp = int(time.time())
                authentication_man = auth_man(user.email, user.password, timestamp, mongo_db)
                result, uuid = authentication_man.gen_hash(), authentication_man.gen_uuid()
                if result["success"]:    
                    mongo_db["users"].insert_one({"email": user.email, "UUID": uuid, "hash": result["content"]["hash"], "salt": result["content"]["salt"], "created": result["content"]["created"], "edited": result["content"]["edited"]})
                    return {"success": True, "error_code": False, "message": "Account created successfully!", "content": {"UUID": uuid, "redirect": f"/login"}} #NOTE: SWITCH TO ID. SUBDOMAIN IN PRODUCTION
                else: return result
            else: return {"success": False, "error_code": 1, "message": f"Account already exists!"}
    else: return {"success": False, "error_code": 1, "message": f"Please read and accept the ToS / Privacy Policy!"}

@app.post("/login")
async def authenticate_user(user: User_Item):         #TODO: Implement sessions, cookies, 2FA 
    authentication_man = auth_man(user.email, user.password, mongo_db=mongo_db)
    return authentication_man.verify_hash()


        



uvicorn.run(app, host = "0.0.0.0")
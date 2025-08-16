import arrow
import jwt

user_id = input("User id: ")
future_time = arrow.utcnow().int_timestamp + 3600
token = jwt.encode({"user_id": user_id, "exp": future_time}, key="", algorithm="HS256")

print(token)

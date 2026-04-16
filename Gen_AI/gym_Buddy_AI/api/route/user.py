print("enter you name: ") 
name = input()
print("Enter you Email: ")
email = input()
print("Enter you password: ")
password = input()

from service import user_service    


async def register_user(name, email, password):
    user_info = await user_service.create_user(name, email, password)
    if user_info:
        return "User registered successfully"
    return "Failed to register user"
import requests
import hashlib

def check_leaked_password(password):
    sha1hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1hash[:5], sha1hash[5:]
    
    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    if response.status_code == 200:
        for line in response.text.splitlines():
            if line.split(":")[0] == suffix:
                return int(line.split(":")[1])
    
    return 0

file_path = "users.txt"

with open(file_path, "r") as file:
    for line in file:
        username, password = line.strip().split(",")
        leaked_count = check_leaked_password(password)
        
        if leaked_count > 0:
            print(f"Password for user {username} has been leaked {leaked_count} times!")
        else:
            print(f"Password for user {username} is secure.")

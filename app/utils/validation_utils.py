from fastapi import HTTPException

def validate_password(password: str):
    # Example validation rules
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
    if not any(char.isupper() for char in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter.")
    if not any(char.islower() for char in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter.")
    if not any(char.isdigit() for char in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one digit.")
    if not any(char in "!@#$%^&*()-_+=<>?/{}~|[]:" for char in password):
        raise HTTPException(status_code=400, detail="Password must contain at least one special character.")

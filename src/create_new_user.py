if __name__ == "__main__":
    import re
    import uuid
    from main import app

    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # valid username == email address
    check_valid_username = lambda email: re.match(email_regex, email) is not None
    check_password_length = lambda passwd: len(passwd) >= 8

    with app.app_context():
        from src.models import db, Users
        from werkzeug.security import generate_password_hash

        print("\nCreate a New User")
        print("- username must be a valid email address")
        print("- password must be at least 8 characters long\n")
        print("=" * 32)

        username = input("Enter username: ")

        if check_valid_username(username) is False:
            print("Username must be a valid email address.")
            exit(1)

        if  Users.query.filter_by(username=username).first() is not None:
            print(f"User '{username}' already exists")
            exit(1)

        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")

        if confirm_password != password:
            print("Passwords do not match. Please try again.")
            exit(1)

        if check_password_length(password) is False:
            print("Password must be at least 8 characters long")
            exit(1)

        user =  Users(
            id=uuid.uuid4(),
            first_name="",
            last_name="",
            username=username,
            password=generate_password_hash(password),
        )
        if user:
            print(f"User - {username} created successfully!")
            db.session.add(user)
            db.session.commit()
            print("=" * 32)
        else:
            print("Failed to create user. Please try again.")

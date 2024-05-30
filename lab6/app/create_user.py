from app import app, db
from models import User

with app.app_context():
    # создайте нового пользователя
    new_user = User(
        first_name="Дарья",
        last_name="Трифонова",
        login="trifonova",
    )

    # установите пароль
    new_user.set_password("qwerty")

    # добавьте и сохраните пользователя в базе данных
    db.session.add(new_user)
    db.session.commit()

    print(f"User {new_user.login} created successfully.")

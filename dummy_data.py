import random
from faker import Faker
from flask import Flask
from comments.database_setup import make_connection_string
from comments.models import db, User, Comment


fake = Faker()


def create_users(db):
    users = []
    for _ in range(10):
        user = User(
            username=fake.user_name(),
            password=fake.password(),
            display_name=fake.name(),
            email=fake.email(),
            avatar=fake.image_url(),
        )
        users.append(user)
        db.session.add(user)

    db.session.commit()
    return users


def create_comments(db, users):
    urls = [
        "https://example.com/post1",
        "https://example.com/post2",
        "https://example.com/post3",
        "https://example.com/post4",
        "https://example.com/post5",
    ]

    for url in urls:
        # Create root comments
        for _ in range(random.randint(1, 5)):
            user = random.choice(users)
            comment = Comment(
                url=url,
                user_id=user.id,
                content=fake.paragraph(nb_sentences=random.randint(1, 5)),
            )
            db.session.add(comment)
            db.session.commit()

            # Create reply comments
            for _ in range(random.randint(0, 3)):
                reply_user = random.choice(users)
                reply = Comment(
                    url=url,
                    parent_id=comment.id,
                    user_id=reply_user.id,
                    content=fake.paragraph(nb_sentences=random.randint(1, 3)),
                )
                db.session.add(reply)
                db.session.commit()

                # Add upvotes and downvotes
                reply.upvotes = random.randint(0, 10)
                reply.downvotes = random.randint(0, 5)
                db.session.commit()

            # Add upvotes and downvotes to root comments
            comment.upvotes = random.randint(0, 20)
            comment.downvotes = random.randint(0, 10)
            db.session.commit()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = make_connection_string()

with app.app_context():
    db.init_app(app)

    users = create_users(db)
    create_comments(db, users)


print("Dummy data generated successfully!")

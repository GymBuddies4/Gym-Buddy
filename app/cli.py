import typer
from app.database import engine
from app.models.user import User
from app.models.workout import Workout
from app.utilities.security import encrypt_password
from sqlmodel import Session

cli = typer.Typer()

@cli.command()
def user():
    with Session(engine) as session:
        users = [
            User(username = "bob", email="bobname@info2602.com", password=encrypt_password("bobpass"), role = "user"),
        ]
        for user in users:
            session.add(user)
        session.commit()
        print("You have succesfully logged in!")

if __name__ == "__main__":
    cli()
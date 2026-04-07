import typer
from app.database import get_cli_session
from app.models.user import User

cli = typer.Typer()

@cli.command()
def user():
    with get_cli_session() as session:
        users = [
            User(username = "bob", email="bobname@info2602.com", password = "bobpass", role = "user"),
        ]
        for user in users:
            session.add(user)
            session.commit()
            print("You have succesfully logged in!")
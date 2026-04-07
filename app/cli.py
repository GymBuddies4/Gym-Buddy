import typer
from app.database import get_cli_session
from app.models.user import User

app = typer.Typer()

@cli.command()

"""This module provides the RP To-Do CLI."""
# rptodo/cli.py

from pathlib import Path
from typing import List, Optional
from typing import Optional

import typer

from rptodo import (
    ERRORS, __app_name__, __version__, config, database, rptodo
)

app = typer.Typer()

def get_todoer() -> rptodo.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "rptodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return rptodo.Todoer(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "rptodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="to-do database location?",
    ),
) -> None:
    """Initialize the to-do database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do database is {db_path}", fg=typer.colors.GREEN)


@app.command()
def test(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--test",
        "-test",
    ),
) -> None:
    """Test to-do database."""
    typer.secho(
            f'Creating database failed with',
            fg=typer.colors.RED,
        )
    typer.secho(f"The to-do database is {db_path}", fg=typer.colors.GREEN)

@app.command()
def getall():
    """Get all to-do in the database."""
    todoer = get_todoer()
    data = todoer.get_all()
    typer.secho(
        f'data: {data}',
        fg=typer.colors.GREEN
    )

@app.command()
def add(
    description: List[str] = typer.Argument(...),
    priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    todoer = get_todoer()
    todo, error = todoer.add(description, priority)
    if error:
        typer.secho(
            f'Adding to-do failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""to-do: "{todo['Description']}" was added """
            f"""with priority: {priority}""",
            fg=typer.colors.GREEN,
        )


@app.command()
def delete():
    """delete all data to-do in the database."""
    todoer = get_todoer()
    delete, error = todoer.delete_all()
    if error:
        typer.secho(
            f'delete all to-do failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    typer.secho(
            f"""deleted all data """,
            fg=typer.colors.GREEN,
        )

@app.command()
def deletebyuuid(uuid: str):
    """delete data by uuid to-do in the database."""
    todoer = get_todoer()
    delete, error = todoer.delete_by_uuid(uuid)
    if error:
        typer.secho(
            f'delete all to-do failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    typer.secho(
            f"""deleted data by uuid""",
            fg=typer.colors.GREEN,
        )
    
    
def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()
    

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
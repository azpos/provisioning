import pydantic_settings

import pydantic
import rich
import typer


class Settings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_prefix="SEAREPORT_")

    location: str = "westeurope"
    project: str
    environment: str


SETTINGS_VALIDATION_ERROR_MESSAGE = "There were [bold red]errors[/bold red] while trying to validate the project settings. You probably forgot to define the necessary [bold green]ENV[/bold green] variables.\n\n More Info:\n"

def check_settings() -> None:
    try:
        Settings()
    except pydantic.ValidationError as exc:
        rich.print(SETTINGS_VALIDATION_ERROR_MESSAGE)
        rich.print(f"[bold]{exc}[/bold]")
        raise typer.Abort() from exc


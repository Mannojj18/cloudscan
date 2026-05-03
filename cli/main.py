
import typer
from cli.commands.scan import scan_command
from cli.commands.explain import explain_command

app = typer.Typer()

app.command("scan")(scan_command)
app.command("explain")(explain_command)

if __name__ == "__main__":
    app()


from rich.console import Console
from jobqueue.worker import enqueue_scan

console = Console()

def scan_command():
    console.print("[bold cyan]Submitting CloudFriend3 scan job...[/bold cyan]")
    enqueue_scan()
    console.print("[green]Scan queued[/green]")

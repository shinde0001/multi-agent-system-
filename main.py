from config import BookBrief, DEFAULT_BRIEF
from orchestrator import Orchestrator
import logging
from rich.prompt import Prompt
from rich.console import Console

# Suppress debug logs from libraries to keep CLI clean
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("trafilatura").setLevel(logging.WARNING)

console = Console()

def main():
    try:
        console.print("[bold cyan]Welcome to the Multi-Agent Book Writer![/]")
        
        use_default = Prompt.ask("Do you want to write the default 'UPI' book? (y/n)", choices=["y", "n"], default="y")
        
        if use_default.lower() == 'n':
            custom_title = Prompt.ask("What is the title/topic of your book?")
            custom_audience = Prompt.ask("Who is the target audience?", default="General readers")
            custom_tone = Prompt.ask("What tone should the book have?", default="Professional and engaging")
            
            brief = BookBrief(
                title=custom_title,
                audience=custom_audience,
                tone=custom_tone,
                length_instructions="3 chapters, about 600-900 words each.",
                citation_rules="Every fact, figure and date must have a numbered citation in the text, for example [1]. Each chapter ends with a reference list giving the source name, title and a working link. Prefer official sources and reputable news. Each chapter ends with one line starting with 'Takeaway:', placed before its reference list."
            )
        else:
            brief = DEFAULT_BRIEF
            
        app = Orchestrator(brief)
        app.run()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")

if __name__ == "__main__":
    main()

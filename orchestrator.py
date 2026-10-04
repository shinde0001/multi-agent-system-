from config import BookBrief, MAX_REVISIONS
from agents import PlannerAgent, ResearcherAgent, WriterAgent, EditorAgent, FactCheckerAgent
from rich.console import Console
from rich.panel import Panel
import os
import pathlib
from md2pdf.core import md2pdf

console = Console()

class Orchestrator:
    def __init__(self, brief: BookBrief):
        self.brief = brief
        self.planner = PlannerAgent()
        self.researcher = ResearcherAgent()
        self.writer = WriterAgent()
        self.editor = EditorAgent()
        self.fact_checker = FactCheckerAgent()
        self.book_chapters = []

    def run(self):
        console.print(Panel(f"[bold cyan]📖 Multi-Agent Book Writer[/]\n[yellow]\"{self.brief.title}\"[/]", border_style="cyan"))
        
        # 1. PLAN
        with console.status("[bold green]Phase 1: Planning book outline...[/]"):
            outline = self.planner.plan(self.brief)
            
        if not outline or len(outline.chapters) != 3:
            console.print("[red]❌ Planner failed to create a valid 3-chapter outline.[/]")
            return
            
        console.print(f"[green]✓ Created outline:[/] {len(outline.chapters)} chapters.")
        
        # Process each chapter
        for i, chapter_outline in enumerate(outline.chapters, 1):
            console.print(f"\n[bold magenta]Processing Chapter {i}: {chapter_outline.title}[/]")
            
            # 2. RESEARCH
            with console.status(f"[bold cyan]Phase 2: Researching data points for Chapter {i}...[/]"):
                dossier = self.researcher.research_chapter(chapter_outline)
                
            console.print(f"[green]✓ Research dossier ready:[/] Found {len(dossier.sources)} verified sources.")
            
            # 3. WRITE & EDIT LOOP
            chapter_draft = None
            editor_feedback = None
            for edit_round in range(MAX_REVISIONS + 1):
                with console.status(f"[bold yellow]Phase 3: Writing Chapter {i} (Round {edit_round + 1})...[/]"):
                    chapter_draft = self.writer.write_chapter(self.brief, chapter_outline, dossier, editor_feedback)
                    
                if not chapter_draft:
                    console.print("[red]❌ Writer failed to generate chapter.[/]")
                    return
                    
                with console.status(f"[bold magenta]Phase 4: Editing Chapter {i}...[/]"):
                    edit_result = self.editor.review_chapter(self.brief, chapter_draft)
                    
                if not edit_result:
                    console.print("[yellow]⚠️ Editor failed to review. Accepting draft as-is.[/]")
                    break
                    
                if edit_result.status == 'approved':
                    console.print(f"[green]✓ Chapter {i} approved by Editor.[/]")
                    break
                else:
                    editor_feedback = "\\n".join(edit_result.feedback)
                    console.print(f"[yellow]⚠️ Revision needed (Round {edit_round + 1}):[/]\n{editor_feedback}")
                    if edit_round == MAX_REVISIONS - 1:
                        console.print(f"[yellow]⚠️ Max revisions reached. Forcing acceptance.[/]")
            
            # 4. FACT CHECK
            with console.status(f"[bold blue]Phase 5: Fact-checking Chapter {i}...[/]"):
                fc_result = self.fact_checker.verify_citations(chapter_draft)
                
            if fc_result.status == 'approved':
                console.print(f"[green]✓ All citations in Chapter {i} verified![/]")
            else:
                failed = len(fc_result.failed_citations)
                console.print(f"[red]⚠️ Fact-check flagged {failed} citations as unsupported/broken.[/]")
                for item in fc_result.details:
                    if not item.claim_supported or not item.url_accessible:
                        console.print(f"  - Citation [{item.citation_id}]: {item.notes}")
                console.print("[yellow]Note: Proceeding with warnings as per orchestrator config.[/]")
                
            self.book_chapters.append(chapter_draft)

        # 5. ASSEMBLE
        self._assemble_book()
        
    def _assemble_book(self):
        console.print("\n[bold green]📚 Assembling final book...[/]")
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, 'book.md')
        
        with open(filepath, 'w') as f:
            f.write(f"# {self.brief.title}\n\n")
            
            for i, chapter in enumerate(self.book_chapters, 1):
                f.write(f"## Chapter {i}\n\n")
                f.write(chapter.content)
                f.write("\n\n### References\n")
                for ref in chapter.references:
                    f.write(f"[{ref.citation_id}] {ref.source_name}: *{ref.title}* - {ref.url}\n")
                f.write("\n\n---\n\n")
                
        pdf_path = os.path.join(output_dir, 'book.pdf')
        css_path = os.path.join(os.path.dirname(__file__), 'style.css')
        try:
            console.print("[cyan]Converting Markdown to PDF...[/]")
            md2pdf(pathlib.Path(pdf_path), md=pathlib.Path(filepath), css=pathlib.Path(css_path))
            pdf_success = True
        except Exception as e:
            console.print(f"[red]⚠️ Failed to generate PDF: {e}[/]")
            pdf_success = False
            
        console.print(f"[bold green]✨ Done! Book saved to: {filepath}[/]")
        if pdf_success:
            console.print(f"[bold green]📄 PDF also saved to: {pdf_path}[/]")

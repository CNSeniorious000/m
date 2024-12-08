from typing import ClassVar

from rich.markdown import CodeBlock, Markdown
from rich.syntax import Syntax
from rich.text import Text


class Markdown(Markdown):
    class CleanCodeBlock(CodeBlock):
        def __rich_console__(self, console, options):
            code = str(self.text).rstrip()
            yield Text(f"```{self.lexer_name}", style="dim")
            yield Syntax(code, self.lexer_name, theme=self.theme, background_color="default", word_wrap=True)
            yield Text("```", style="dim")

    elements: ClassVar = {**Markdown.elements, "fence": CleanCodeBlock}


class TruncatedMarkdown(Markdown):
    def __rich_console__(self, console, options):
        results = list(super().__rich_console__(console, options))
        height = console.height
        count = 0
        buffer = []
        for segment in reversed(results):
            count += segment.text.count("\n")  # type: ignore
            if count > height:
                break
            buffer.append(segment)

        yield from reversed(buffer)

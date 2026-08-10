import datetime
from internal.tui.jobList import JobListItem, JobOffer
from textual.app import App, ComposeResult
from textual.widgets import (
    Footer,
    # Header,
    MarkdownViewer,
    ListView,
    ListItem,
    Label,
    Static,
)
from textual.containers import Center
from textual.screen import Screen


LOGO_ASCII = r"""
     _     _
    (o)-=-(o)         ___        ___ ___ ___ _   _ __  __ ___
  __(  ___  )__      | _ \_  _  | _ \ __/ __| | | |  \/  | __|
 / _/ '---' \_ \     |  _/ || | |   / _|\__ \ |_| | |\/| | _|
| \ \       / / |    |_|  \_, | |_|_\___|___/\___/|_|  |_|___|
 \_>_)/_\-/_\(_<_/         |__/
"""


def open_md_file():
    ret = ""
    with open("test.md", "r") as md:
        ret = md.read()

    return ret


class Header(Center):
    DEFAULT_CSS = """
    Header {
        height: auto;
        width: auto;
        dock: top;
        color: $success
        }
        """

    def compose(self) -> ComposeResult:
        yield Label(LOGO_ASCII, id="Header", markup=False)


class PyCV(App):
    BINDINGS = [
        ("g", "generate", "Generate"),
        ("r", "regen", "Regenerate"),
        ("o", "open", "Open"),
        ("d", "diff", "Diff CV"),
    ]

    CSS_PATH = "../../style/layout.tcss"

    def __init__(self, offers: list[JobOffer]) -> None:
        super().__init__()
        self.offers = offers

    def compose(self) -> ComposeResult:
        yield Header()
        yield ListView(*(JobListItem(o) for o in self.offers), classes="box")
        yield MarkdownViewer(
            markdown=open_md_file(),
            name="Markdown viewer",
            show_table_of_contents=False,
            classes="box",
        )
        yield Footer()

    def action_regen(self) -> None:
        lv = self.query_one("#jobs", ListView)
        item = lv.highlighted_child
        if isinstance(item, JobListItem) and item.offer:
            offer = item.offer
            offer.generated_at = datetime.datetime.now()
            item.offer = offer
            item.mutate_reactive(JobListItem.offer)

    # def on_ready(self) -> None:
    #    self.push_screen(BaseScreen())

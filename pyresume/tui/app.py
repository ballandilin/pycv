import datetime
from os import path
from pyresume.models import JobOffer
from pyresume.tui.add_offer import AddOfferScreen
from pyresume.tui.joblist import JobListItem
from textual.app import App, ComposeResult
from textual.widgets import Footer, MarkdownViewer, ListView, Label, Static
from textual.widget import Widget
from textual.reactive import reactive
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen


LOGO_ASCII = r"""
     _     _
    (o)-=-(o)         ___        ___ ___ ___ _   _ __  __ ___
  __(  ___  )__      | _ \_  _  | _ \ __/ __| | | |  \/  | __|
 / _/ '---' \_ \     |  _/ || | |   / _|\__ \ |_| | |\/| | _|
| \ \       / / |    |_|  \_, | |_|_\___|___/\___/|_|  |_|___|
 \_>_)/_\-/_\(_<_/         |__/
"""


def open_md_file(src: str):
    ret = f"no such file {src}"
    if path.exists(src):
        with open(src, "r") as md:
            ret = md.read()

    return ret


class Header(Center):
    DEFAULT_CSS = """
    Header {
        height: auto;
        width: auto;
        dock: top;
        color: $success;
        }
        """

    def compose(self) -> ComposeResult:
        yield Label(LOGO_ASCII, id="Header", markup=False)


class MarkdownViewerWidget(Widget):
    job_content: reactive[str] = reactive("", recompose=True)

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        yield MarkdownViewer(
            markdown=self.job_content,
            show_table_of_contents=False,
            id="preview",
            classes="box",
        )

        # def watch_job_content(self, source: str) -> None:
        # self.query_one(MarkdownViewer).document.update(source)


class PyResume(App):
    BINDINGS = [
        ("g", "gen", "Generate"),
        ("o", "open", "Open"),
        ("d", "diff", "Diff CV"),
        ("a", "add", "Add Offer"),
        ("r", "remove", "Remove offer"),
    ]

    CSS_PATH = "../../style/layout.tcss"

    def __init__(self, offers: list[JobOffer]) -> None:
        super().__init__()
        self.offers = offers
        self.highlighted_item = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main"):
            yield ListView(
                *(JobListItem(o) for o in self.offers),
                id="jobs",
                classes="box",
            )
            yield MarkdownViewerWidget()
            yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if isinstance(item, JobListItem) and item.offer:
            self.notify(f"Selected : {item.offer.title}")
            self.query_one(MarkdownViewerWidget).job_content = open_md_file(
                item.offer.source
            )

    def action_add(self) -> None:
        def on_close(offer: JobOffer | None) -> None:
            if offer is None:
                return
            self.offers.append(offer)
            self.query_one("#jobs", ListView).append(JobListItem(offer))

        self.push_screen(AddOfferScreen(), on_close)

    def action_open(self) -> None:
        pass

    def action_remove(self) -> None:
        listview = self.query_one("#jobs", ListView)
        if listview.highlighted_child is not None:
            listview.pop(listview.index)

    def action_gen(self) -> None:
        lv = self.query_one("#jobs", ListView)
        item = lv.highlighted_child
        if isinstance(item, JobListItem) and item.offer:
            self.notify(f"Regenerate document for : {item.offer.title}")
            offer = item.offer
            offer.generated_at = datetime.datetime.now()
            item.offer = offer
            item.mutate_reactive(JobListItem.offer)

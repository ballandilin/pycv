import sys

from pyresume import cli
from pyresume.mock import MOCK_OFFERS
from pyresume.tui.app import PyResume


def main():
    if len(sys.argv) > 1:
        cli.main()
    else:
        PyResume(MOCK_OFFERS).run()


if __name__ == "__main__":
    main()

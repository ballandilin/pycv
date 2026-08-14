import sys

from pycv import cli
from pycv.mock import MOCK_OFFERS
from pycv.tui.app import PyCV


def main():
    if len(sys.argv) > 1:
        cli.main()
    else:
        PyCV(MOCK_OFFERS).run()


if __name__ == "__main__":
    main()

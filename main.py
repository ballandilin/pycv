import sys

import cli
from internal.mock import MOCK_OFFERS
from internal.tui.app import PyCV


def main():
    if len(sys.argv) > 1:
        cli.main()
    else:
        PyCV(MOCK_OFFERS).run()


if __name__ == "__main__":
    main()

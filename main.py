from internal.mock import MOCK_OFFERS
from internal.tui.app import PyCV


def main():
    PyCV(MOCK_OFFERS).run()


if __name__ == "__main__":
    main()

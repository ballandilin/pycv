from internal.mock import MOCK_OFFERS
from internal.models import jobOffer
from internal.tui.app import PyCV
from internal.models.jobOffer import JobOffer


def main():
    job_offer_list = []
    PyCV(job_offer_list).run()


if __name__ == "__main__":
    main()

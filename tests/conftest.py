import os
import logging
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="module")
def logger(pytestconfig):
    logg = logging.getLogger(__name__)
    if not logg.hasHandlers():
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        )
        logg.addHandler(handler)
    return logg

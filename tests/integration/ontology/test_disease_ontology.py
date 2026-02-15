import logging
from pathlib import Path

import pronto
import pytest

logger = logging.getLogger(__name__)

DOID_PATH = Path(__file__).resolve().parents[3] / "src" / "rx_scout" / "data" / "doid.obo"


@pytest.fixture(scope="module")
def ontology():
    if not DOID_PATH.exists():
        pytest.skip(f"doid.obo not found at {DOID_PATH}")
    return pronto.Ontology(str(DOID_PATH))


@pytest.mark.integration
def test_load_ontology(ontology):
    assert len(ontology.terms()) > 0


@pytest.mark.integration
def test_lookup_type2_diabetes(ontology):
    term = ontology["DOID:9352"]
    assert term.name == "type 2 diabetes mellitus"
    assert term.definition is not None


@pytest.mark.integration
def test_term_synonyms(ontology):
    term = ontology["DOID:9352"]
    synonym_texts = {s.description for s in term.synonyms}
    assert len(synonym_texts) > 0


@pytest.mark.integration
def test_term_superclasses(ontology):
    term = ontology["DOID:9352"]
    superclasses = list(term.superclasses())
    assert len(superclasses) > 1  # at least itself + parent


@pytest.mark.integration
def test_term_subclasses(ontology):
    term = ontology["DOID:9352"]
    subclasses = list(term.subclasses())
    assert len(subclasses) >= 1  # at least itself

import pytest
from pydantic import ValidationError

from rx_scout.models import DiseaseSimilarityModel


def test_valid_disease_similarity():
    sim = DiseaseSimilarityModel(
        disease_id_1=1,
        disease_id_2=2,
        similarity_score=0.85,
        similarity_type="phenotypic",
    )
    assert sim.disease_id_1 == 1
    assert sim.disease_id_2 == 2
    assert sim.similarity_score == 0.85
    assert sim.similarity_type == "phenotypic"


def test_missing_required_field():
    with pytest.raises(ValidationError):
        DiseaseSimilarityModel(
            disease_id_1=1,
            disease_id_2=2,
            # similarity_score is missing
            similarity_type="phenotypic",
        )


def test_boundary_scores():
    sim_zero = DiseaseSimilarityModel(
        disease_id_1=1,
        disease_id_2=2,
        similarity_score=0.0,
        similarity_type="genetic",
    )
    assert sim_zero.similarity_score == 0.0

    sim_one = DiseaseSimilarityModel(
        disease_id_1=1,
        disease_id_2=2,
        similarity_score=1.0,
        similarity_type="genetic",
    )
    assert sim_one.similarity_score == 1.0

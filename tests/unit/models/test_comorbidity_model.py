import pytest
from pydantic import ValidationError

from rx_scout.models import ComorbidityModel


def test_valid_comorbidity():
    cm = ComorbidityModel(
        disease_id_1=1,
        disease_id_2=2,
        co_occurrence_score=0.45,
    )
    assert cm.disease_id_1 == 1
    assert cm.disease_id_2 == 2
    assert cm.co_occurrence_score == 0.45


def test_missing_required_field():
    with pytest.raises(ValidationError):
        ComorbidityModel(
            disease_id_1=1,
            disease_id_2=2,
            # co_occurrence_score is missing
        )


def test_boundary_scores():
    cm_zero = ComorbidityModel(
        disease_id_1=1,
        disease_id_2=2,
        co_occurrence_score=0.0,
    )
    assert cm_zero.co_occurrence_score == 0.0

    cm_one = ComorbidityModel(
        disease_id_1=1,
        disease_id_2=2,
        co_occurrence_score=1.0,
    )
    assert cm_one.co_occurrence_score == 1.0

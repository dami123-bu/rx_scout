import pytest
from pydantic import ValidationError

from rx_scout.models import SideEffectModel


def test_valid_side_effect():
    se = SideEffectModel(
        drug_id=1,
        side_effect="Nausea",
        frequency="common",
    )
    assert se.drug_id == 1
    assert se.side_effect == "Nausea"
    assert se.frequency == "common"


def test_missing_required_field():
    with pytest.raises(ValidationError):
        SideEffectModel(
            drug_id=1,
            # side_effect is missing
            frequency="rare",
        )

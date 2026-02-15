import pytest
from pydantic import ValidationError

from rx_scout.models import DrugModel


def test_valid_drug():
    drug = DrugModel(
        external_id="DB00331",
        name="Metformin",
        drug_class="Biguanide",
        atc_codes=["A10BA02"],
        mechanism="AMPK activation",
        indications=["Type 2 Diabetes"],
        side_effects=["Nausea", "Diarrhea"],
    )
    assert drug.external_id == "DB00331"
    assert drug.name == "Metformin"
    assert drug.drug_class == "Biguanide"
    assert drug.atc_codes == ["A10BA02"]
    assert drug.mechanism == "AMPK activation"
    assert drug.indications == ["Type 2 Diabetes"]
    assert drug.side_effects == ["Nausea", "Diarrhea"]


def test_missing_required_field():
    with pytest.raises(ValidationError):
        DrugModel(
            external_id="DB00331",
            # name is missing
            drug_class="Biguanide",
            atc_codes=["A10BA02"],
            mechanism="AMPK activation",
            indications=["Type 2 Diabetes"],
            side_effects=["Nausea"],
        )


def test_empty_lists_accepted():
    drug = DrugModel(
        external_id="DB00331",
        name="Metformin",
        drug_class="Biguanide",
        atc_codes=[],
        mechanism="AMPK activation",
        indications=[],
        side_effects=[],
    )
    assert drug.atc_codes == []
    assert drug.indications == []
    assert drug.side_effects == []

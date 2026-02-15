import pytest

from rx_scout.models import SideEffectModel
from rx_scout.sqlalchemy import Drug, SideEffect


@pytest.mark.integration
def test_create_side_effect(session):
    drug = Drug(
        external_id="DB00331",
        name="Metformin",
        drug_class="Biguanide",
        atc_codes=["A10BA02"],
        mechanism="AMPK activation",
        indications=["Type 2 Diabetes"],
        side_effects=["Nausea"],
    )
    session.add(drug)
    session.flush()

    se = SideEffect(
        drug_id=drug.id,
        side_effect="Nausea",
        frequency="common",
    )
    session.add(se)
    session.flush()

    assert se.id is not None
    assert se.drug_id == drug.id
    assert se.side_effect == "Nausea"
    assert se.frequency == "common"


@pytest.mark.integration
def test_side_effect_drug_relationship(session):
    drug = Drug(
        external_id="DB00331",
        name="Metformin",
        drug_class="Biguanide",
        atc_codes=["A10BA02"],
        mechanism="AMPK activation",
        indications=["Type 2 Diabetes"],
        side_effects=["Nausea"],
    )
    session.add(drug)
    session.flush()

    se = SideEffect(
        drug_id=drug.id,
        side_effect="Diarrhea",
        frequency="common",
    )
    session.add(se)
    session.flush()

    assert se.drug.name == "Metformin"
    assert len(drug.side_effect_entries) == 1
    assert drug.side_effect_entries[0].side_effect == "Diarrhea"


@pytest.mark.integration
def test_query_side_effects_by_drug(session):
    drug = Drug(
        external_id="DB00331",
        name="Metformin",
        drug_class="Biguanide",
        atc_codes=["A10BA02"],
        mechanism="AMPK activation",
        indications=["Type 2 Diabetes"],
        side_effects=["Nausea"],
    )
    session.add(drug)
    session.flush()

    se1 = SideEffect(drug_id=drug.id, side_effect="Nausea", frequency="common")
    se2 = SideEffect(drug_id=drug.id, side_effect="Lactic acidosis", frequency="rare")
    session.add_all([se1, se2])
    session.flush()

    results = (
        session.query(SideEffect)
        .filter(SideEffect.drug_id == drug.id)
        .all()
    )
    assert len(results) == 2
    side_effect_names = {r.side_effect for r in results}
    assert side_effect_names == {"Nausea", "Lactic acidosis"}


@pytest.mark.integration
def test_side_effect_from_attributes(session):
    drug = Drug(
        external_id="DB00331",
        name="Metformin",
        drug_class="Biguanide",
        atc_codes=["A10BA02"],
        mechanism="AMPK activation",
        indications=["Type 2 Diabetes"],
        side_effects=["Nausea"],
    )
    session.add(drug)
    session.flush()

    db_se = SideEffect(
        drug_id=drug.id,
        side_effect="Nausea",
        frequency="common",
    )
    session.add(db_se)
    session.flush()

    model = SideEffectModel.model_validate(db_se)
    assert model.drug_id == drug.id
    assert model.side_effect == "Nausea"
    assert model.frequency == "common"

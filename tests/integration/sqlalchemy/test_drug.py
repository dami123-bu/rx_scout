import pytest

from rx_scout.models import DrugModel
from rx_scout.sqlalchemy import Disease, Drug, DrugDiseaseApproval


@pytest.mark.integration
def test_create_drug(session):
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
    assert drug.id is not None
    assert drug.external_id == "DB00331"
    assert drug.name == "Metformin"
    assert drug.drug_class == "Biguanide"
    assert drug.atc_codes == ["A10BA02"]
    assert drug.mechanism == "AMPK activation"
    assert drug.indications == ["Type 2 Diabetes"]
    assert drug.side_effects == ["Nausea"]


@pytest.mark.integration
def test_query_drug_by_name(session):
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

    result = session.query(Drug).filter(Drug.name == "Metformin").first()
    assert result.external_id == "DB00331"
    assert result.name == "Metformin"
    assert result.drug_class == "Biguanide"
    assert result.atc_codes == ["A10BA02"]
    assert result.mechanism == "AMPK activation"
    assert result.indications == ["Type 2 Diabetes"]
    assert result.side_effects == ["Nausea"]


@pytest.mark.integration
def test_drug_approvals_relationship(session):
    drug = Drug(
        external_id="DB00331",
        name="Metformin",
        drug_class="Biguanide",
        atc_codes=["A10BA02"],
        mechanism="AMPK activation",
        indications=["Type 2 Diabetes"],
        side_effects=["Nausea"],
    )
    disease = Disease(
        name="Type 2 Diabetes",
        external_ids=["MESH:D003924"],
        phenotype_features=["Hyperglycemia"],
    )
    session.add_all([drug, disease])
    session.flush()

    approval = DrugDiseaseApproval(drug_id=drug.id, disease_id=disease.id)
    session.add(approval)
    session.flush()

    assert len(drug.approvals) == 1
    assert drug.approvals[0].disease.name == "Type 2 Diabetes"


@pytest.mark.integration
def test_drug_from_attributes(session):
    db_drug = Drug(
        external_id="DB00331",
        name="Metformin",
        drug_class="Biguanide",
        atc_codes=["A10BA02"],
        mechanism="AMPK activation",
        indications=["Type 2 Diabetes"],
        side_effects=["Nausea"],
    )
    session.add(db_drug)
    session.flush()

    model = DrugModel.model_validate(db_drug)
    assert model.external_id == "DB00331"
    assert model.name == "Metformin"
    assert model.drug_class == "Biguanide"
    assert model.atc_codes == ["A10BA02"]
    assert model.mechanism == "AMPK activation"
    assert model.indications == ["Type 2 Diabetes"]
    assert model.side_effects == ["Nausea"]

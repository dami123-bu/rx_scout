import pytest

from rx_scout.models import DiseaseModel
from rx_scout.sqlalchemy import Disease, Drug, DrugDiseaseApproval


@pytest.mark.integration
def test_create_disease(session):
    disease = Disease(
        name="Alzheimer's Disease",
        external_ids=["MESH:D000544"],
        phenotype_features=["Memory loss", "Cognitive decline"],
    )
    session.add(disease)
    session.flush()
    assert disease.id is not None
    assert disease.name == "Alzheimer's Disease"
    assert disease.external_ids == ["MESH:D000544"]
    assert disease.phenotype_features == ["Memory loss", "Cognitive decline"]


@pytest.mark.integration
def test_query_disease_by_name(session):
    disease = Disease(
        name="Alzheimer's Disease",
        external_ids=["MESH:D000544"],
        phenotype_features=["Memory loss"],
    )
    session.add(disease)
    session.flush()

    result = session.query(Disease).filter(Disease.name == "Alzheimer's Disease").first()
    assert result.name == "Alzheimer's Disease"
    assert result.external_ids == ["MESH:D000544"]
    assert result.phenotype_features == ["Memory loss"]


@pytest.mark.integration
def test_disease_approvals_relationship(session):
    disease = Disease(
        name="Type 2 Diabetes",
        external_ids=["MESH:D003924"],
        phenotype_features=["Hyperglycemia"],
    )
    drug = Drug(
        external_id="DB00331",
        name="Metformin",
        drug_class="Biguanide",
        atc_codes=["A10BA02"],
        mechanism="AMPK activation",
        indications=["Type 2 Diabetes"],
        side_effects=["Nausea"],
    )
    session.add_all([drug, disease])
    session.flush()

    approval = DrugDiseaseApproval(drug_id=drug.id, disease_id=disease.id)
    session.add(approval)
    session.flush()

    assert len(disease.approvals) == 1
    assert disease.approvals[0].drug.name == "Metformin"


@pytest.mark.integration
def test_disease_from_attributes(session):
    db_disease = Disease(
        name="Alzheimer's Disease",
        external_ids=["MESH:D000544"],
        phenotype_features=["Memory loss"],
    )
    session.add(db_disease)
    session.flush()

    model = DiseaseModel.model_validate(db_disease)
    assert model.external_ids == ["MESH:D000544"]
    assert model.name == "Alzheimer's Disease"
    assert model.phenotype_features == ["Memory loss"]

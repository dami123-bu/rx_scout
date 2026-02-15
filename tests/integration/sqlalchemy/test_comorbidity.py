import pytest

from rx_scout.models import ComorbidityModel
from rx_scout.sqlalchemy import Comorbidity, Disease


@pytest.mark.integration
def test_create_comorbidity(session):
    disease_1 = Disease(
        name="Type 2 Diabetes",
        external_ids=["MESH:D003924"],
        phenotype_features=["Hyperglycemia"],
    )
    disease_2 = Disease(
        name="Obesity",
        external_ids=["MESH:D009765"],
        phenotype_features=["Excess body weight"],
    )
    session.add_all([disease_1, disease_2])
    session.flush()

    cm = Comorbidity(
        disease_id_1=disease_1.id,
        disease_id_2=disease_2.id,
        co_occurrence_score=0.78,
    )
    session.add(cm)
    session.flush()

    assert cm.id is not None
    assert cm.disease_id_1 == disease_1.id
    assert cm.disease_id_2 == disease_2.id
    assert cm.co_occurrence_score == 0.78


@pytest.mark.integration
def test_comorbidity_relationships(session):
    disease_1 = Disease(
        name="Type 2 Diabetes",
        external_ids=["MESH:D003924"],
        phenotype_features=["Hyperglycemia"],
    )
    disease_2 = Disease(
        name="Cardiovascular Disease",
        external_ids=["MESH:D002318"],
        phenotype_features=["Chest pain"],
    )
    session.add_all([disease_1, disease_2])
    session.flush()

    cm = Comorbidity(
        disease_id_1=disease_1.id,
        disease_id_2=disease_2.id,
        co_occurrence_score=0.65,
    )
    session.add(cm)
    session.flush()

    assert cm.disease_1.name == "Type 2 Diabetes"
    assert cm.disease_2.name == "Cardiovascular Disease"


@pytest.mark.integration
def test_query_comorbidity_by_disease(session):
    disease_1 = Disease(
        name="Type 2 Diabetes",
        external_ids=["MESH:D003924"],
        phenotype_features=["Hyperglycemia"],
    )
    disease_2 = Disease(
        name="Obesity",
        external_ids=["MESH:D009765"],
        phenotype_features=["Excess body weight"],
    )
    session.add_all([disease_1, disease_2])
    session.flush()

    cm = Comorbidity(
        disease_id_1=disease_1.id,
        disease_id_2=disease_2.id,
        co_occurrence_score=0.78,
    )
    session.add(cm)
    session.flush()

    result = (
        session.query(Comorbidity)
        .filter(Comorbidity.disease_id_1 == disease_1.id)
        .first()
    )
    assert result.disease_id_2 == disease_2.id
    assert result.co_occurrence_score == 0.78


@pytest.mark.integration
def test_comorbidity_from_attributes(session):
    disease_1 = Disease(
        name="Type 2 Diabetes",
        external_ids=["MESH:D003924"],
        phenotype_features=["Hyperglycemia"],
    )
    disease_2 = Disease(
        name="Obesity",
        external_ids=["MESH:D009765"],
        phenotype_features=["Excess body weight"],
    )
    session.add_all([disease_1, disease_2])
    session.flush()

    db_cm = Comorbidity(
        disease_id_1=disease_1.id,
        disease_id_2=disease_2.id,
        co_occurrence_score=0.78,
    )
    session.add(db_cm)
    session.flush()

    model = ComorbidityModel.model_validate(db_cm)
    assert model.disease_id_1 == disease_1.id
    assert model.disease_id_2 == disease_2.id
    assert model.co_occurrence_score == 0.78

import pytest

from rx_scout.models import DiseaseSimilarityModel
from rx_scout.sqlalchemy import Disease
from rx_scout.sqlalchemy.disease_similarity import DiseaseSimilarity


@pytest.mark.integration
def test_create_disease_similarity(session):
    disease_1 = Disease(
        name="Alzheimer's Disease",
        external_ids=["MESH:D000544"],
        phenotype_features=["Memory loss"],
    )
    disease_2 = Disease(
        name="Parkinson's Disease",
        external_ids=["MESH:D010300"],
        phenotype_features=["Tremor"],
    )
    session.add_all([disease_1, disease_2])
    session.flush()

    sim = DiseaseSimilarity(
        disease_id_1=disease_1.id,
        disease_id_2=disease_2.id,
        similarity_score=0.72,
        similarity_type="phenotypic",
    )
    session.add(sim)
    session.flush()

    assert sim.id is not None
    assert sim.disease_id_1 == disease_1.id
    assert sim.disease_id_2 == disease_2.id
    assert sim.similarity_score == 0.72
    assert sim.similarity_type == "phenotypic"


@pytest.mark.integration
def test_disease_similarity_relationships(session):
    disease_1 = Disease(
        name="Alzheimer's Disease",
        external_ids=["MESH:D000544"],
        phenotype_features=["Memory loss"],
    )
    disease_2 = Disease(
        name="Parkinson's Disease",
        external_ids=["MESH:D010300"],
        phenotype_features=["Tremor"],
    )
    session.add_all([disease_1, disease_2])
    session.flush()

    sim = DiseaseSimilarity(
        disease_id_1=disease_1.id,
        disease_id_2=disease_2.id,
        similarity_score=0.65,
        similarity_type="genetic",
    )
    session.add(sim)
    session.flush()

    assert sim.disease_1.name == "Alzheimer's Disease"
    assert sim.disease_2.name == "Parkinson's Disease"


@pytest.mark.integration
def test_query_disease_similarity_by_type(session):
    disease_1 = Disease(
        name="Alzheimer's Disease",
        external_ids=["MESH:D000544"],
        phenotype_features=["Memory loss"],
    )
    disease_2 = Disease(
        name="Parkinson's Disease",
        external_ids=["MESH:D010300"],
        phenotype_features=["Tremor"],
    )
    session.add_all([disease_1, disease_2])
    session.flush()

    sim = DiseaseSimilarity(
        disease_id_1=disease_1.id,
        disease_id_2=disease_2.id,
        similarity_score=0.72,
        similarity_type="phenotypic",
    )
    session.add(sim)
    session.flush()

    result = (
        session.query(DiseaseSimilarity)
        .filter(DiseaseSimilarity.similarity_type == "phenotypic")
        .first()
    )
    assert result.similarity_score == 0.72
    assert result.disease_id_1 == disease_1.id
    assert result.disease_id_2 == disease_2.id
    assert result.similarity_type == "phenotypic"


@pytest.mark.integration
def test_disease_similarity_from_attributes(session):
    disease_1 = Disease(
        name="Alzheimer's Disease",
        external_ids=["MESH:D000544"],
        phenotype_features=["Memory loss"],
    )
    disease_2 = Disease(
        name="Parkinson's Disease",
        external_ids=["MESH:D010300"],
        phenotype_features=["Tremor"],
    )
    session.add_all([disease_1, disease_2])
    session.flush()

    db_sim = DiseaseSimilarity(
        disease_id_1=disease_1.id,
        disease_id_2=disease_2.id,
        similarity_score=0.72,
        similarity_type="phenotypic",
    )
    session.add(db_sim)
    session.flush()

    model = DiseaseSimilarityModel.model_validate(db_sim)
    assert model.disease_id_1 == disease_1.id
    assert model.disease_id_2 == disease_2.id
    assert model.similarity_score == 0.72
    assert model.similarity_type == "phenotypic"

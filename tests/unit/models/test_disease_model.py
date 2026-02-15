import pytest
from pydantic import ValidationError

from rx_scout.models import DiseaseModel


def test_valid_disease():
    disease = DiseaseModel(
        external_ids=["MESH:D000544"],
        name="Alzheimer's Disease",
        phenotype_features=["Memory loss", "Cognitive decline"],
    )
    assert disease.external_ids == ["MESH:D000544"]
    assert disease.name == "Alzheimer's Disease"
    assert disease.phenotype_features == ["Memory loss", "Cognitive decline"]


def test_missing_required_field():
    with pytest.raises(ValidationError):
        DiseaseModel(
            external_ids=["MESH:D000544"],
            # name is missing
            phenotype_features=["Memory loss"],
        )

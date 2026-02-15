import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DiseaseModel(BaseModel):
    model_config = {"from_attributes": True}

    external_ids: list[str]
    name: str
    phenotype_features: list[str]

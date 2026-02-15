import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DiseaseSimilarityModel(BaseModel):
    model_config = {"from_attributes": True}

    disease_id_1: int
    disease_id_2: int
    similarity_score: float
    similarity_type: str

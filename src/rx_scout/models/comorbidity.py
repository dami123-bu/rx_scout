import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ComorbidityModel(BaseModel):
    model_config = {"from_attributes": True}

    disease_id_1: int
    disease_id_2: int
    co_occurrence_score: float

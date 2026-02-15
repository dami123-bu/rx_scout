import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SideEffectModel(BaseModel):
    model_config = {"from_attributes": True}

    drug_id: int
    side_effect: str
    frequency: str

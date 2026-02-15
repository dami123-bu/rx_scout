import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DrugModel(BaseModel):
    model_config = {"from_attributes": True}

    external_id: str
    name: str
    drug_class: str
    atc_codes: list[str]
    mechanism: str
    indications: list[str]
    side_effects: list[str]

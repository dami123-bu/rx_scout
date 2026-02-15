import logging
from datetime import date

from pydantic import BaseModel

logger = logging.getLogger(__name__)

class DrugDiseaseApprovalBase(BaseModel):
    model_config = {"from_attributes": True}
    drug_id: int
    disease_id: int
    approval_date: date | None = None
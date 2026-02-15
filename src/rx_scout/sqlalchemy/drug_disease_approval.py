import logging
from datetime import date

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rx_scout.db.base import Base

logger = logging.getLogger(__name__)


class DrugDiseaseApproval(Base):
    __tablename__ = "drug_disease_approvals"

    id: Mapped[int] = mapped_column(primary_key=True)
    drug_id: Mapped[int] = mapped_column(ForeignKey("drugs.id"))
    disease_id: Mapped[int] = mapped_column(ForeignKey("diseases.id"))
    approval_date: Mapped[date | None]

    drug = relationship("Drug", back_populates="approvals")
    disease = relationship("Disease", back_populates="approvals")

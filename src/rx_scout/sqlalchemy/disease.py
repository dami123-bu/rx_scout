import logging

from sqlalchemy import Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rx_scout.db.base import Base

logger = logging.getLogger(__name__)


class Disease(Base):
    __tablename__ = "diseases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    external_ids: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    phenotype_features: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)

    approvals = relationship("DrugDiseaseApproval", back_populates="disease")

import logging

from sqlalchemy import Text, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rx_scout.db.base import Base

logger = logging.getLogger(__name__)


class Drug(Base):
    __tablename__ = "drugs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_id: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    drug_class: Mapped[str] = mapped_column(Text, nullable=False)
    atc_codes: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    mechanism: Mapped[str] = mapped_column(Text, nullable=False)
    indications: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    side_effects: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)

    approvals = relationship("DrugDiseaseApproval", back_populates="drug")

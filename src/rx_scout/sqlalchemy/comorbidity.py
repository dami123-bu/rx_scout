import logging

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rx_scout.db.base import Base

logger = logging.getLogger(__name__)


class Comorbidity(Base):
    __tablename__ = "comorbidities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    disease_id_1: Mapped[int] = mapped_column(ForeignKey("diseases.id"))
    disease_id_2: Mapped[int] = mapped_column(ForeignKey("diseases.id"))
    co_occurrence_score: Mapped[float] = mapped_column(Float, nullable=False)

    disease_1 = relationship("Disease", foreign_keys=[disease_id_1])
    disease_2 = relationship("Disease", foreign_keys=[disease_id_2])

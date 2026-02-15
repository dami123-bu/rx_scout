import logging

from sqlalchemy import Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rx_scout.db.base import Base

logger = logging.getLogger(__name__)


class DiseaseSimilarity(Base):
    __tablename__ = "disease_similarities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    disease_id_1: Mapped[int] = mapped_column(ForeignKey("diseases.id"))
    disease_id_2: Mapped[int] = mapped_column(ForeignKey("diseases.id"))
    similarity_score: Mapped[float] = mapped_column(Float, nullable=False)
    similarity_type: Mapped[str] = mapped_column(Text, nullable=False)

    disease_1 = relationship("Disease", foreign_keys=[disease_id_1])
    disease_2 = relationship("Disease", foreign_keys=[disease_id_2])

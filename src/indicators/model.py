from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.base_model import Base


class Indicator(Base):
    """Индикаторы достижения компетенций."""
    __tablename__ = 'indicators'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    competency_id: Mapped[int] = mapped_column(Integer, ForeignKey('competencies.id'))

    competency = relationship('Competency', back_populates='indicators')

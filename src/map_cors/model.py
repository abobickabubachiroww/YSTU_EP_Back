from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import Base


class MapCore(Base):
    """Ядра карты."""
    __tablename__ = 'map_cors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    semesters_count: Mapped[int] = mapped_column(Integer, nullable=False)

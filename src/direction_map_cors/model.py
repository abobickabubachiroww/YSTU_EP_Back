from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import Base


class DirectionMapCore(Base):
    """Связи направлений подготовки и ядер карт."""
    __tablename__ = 'direction_map_cors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    direction_id: Mapped[int] = mapped_column(Integer, ForeignKey('directions.id'))
    map_core_id: Mapped[int] = mapped_column(Integer, ForeignKey('map_cors.id'))

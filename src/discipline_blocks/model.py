from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import Base


class DisciplineBlock(Base):
    """Блоки дисциплин."""
    __tablename__ = 'discipline_blocks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    discipline_id: Mapped[int] = mapped_column(Integer, ForeignKey('disciplines.id'))
    credit_units: Mapped[int] = mapped_column(Integer, nullable=False)
    control_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('control_types.id'))
    lecture_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    practice_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    lab_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    semester_number: Mapped[int] = mapped_column(Integer, nullable=False)
    map_core_id: Mapped[int] = mapped_column(Integer, ForeignKey('map_cors.id'))

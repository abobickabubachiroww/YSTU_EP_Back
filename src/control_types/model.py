from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import Base


class ControlType(Base):
    """Виды контроля дисциплин (зачет, экзамен, дифференцированный зачет)."""
    __tablename__ = 'control_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

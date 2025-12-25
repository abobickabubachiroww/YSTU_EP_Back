from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.base_model import Base


class Discipline(Base):
    """Дисциплины."""
    __tablename__ = 'disciplines'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    short_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey('departments.id'))

    department = relationship('Department', back_populates='disciplines')

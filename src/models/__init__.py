import uuid
import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Uuid, Boolean, DateTime, ForeignKey


class Base(DeclarativeBase):
    pass


db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[int] = mapped_column(DateTime, default=dt.datetime.now())
    is_authenticated: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_anonymous: Mapped[bool] = mapped_column(Boolean, default=False)
    # Relationship to Records
    records: Mapped[list["Records"]] = relationship(
        "Records", back_populates="created_by_user", cascade="all, delete-orphan"
    )

    # Class Methods
    def __repr__(self):
        return f"<User {self.username}>"

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.is_authenticated

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "created_at": self.created_at,
            # "is_authenticated": self.is_authenticated == True or False,
            "is_active": self.is_active,
            "is_anonymous": self.is_anonymous,
        }


class Records(db.Model):
    __tablename__ = "records"
    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.now())
    # Foreign Key to User
    created_by: Mapped[str] = mapped_column(
        Uuid, ForeignKey("users.id"), nullable=False
    )
    # Relationship to User
    created_by_user: Mapped["Users"] = relationship("Users", back_populates="records")
    # Relationship to Entries
    entries: Mapped[list["Entries"]] = relationship("Entries", back_populates="record", cascade="all, delete")
    # Relationship to GeneralSummary
    general_summary: Mapped[list["GeneralSummary"]] = relationship(
        "GeneralSummary", back_populates="record", cascade="all, delete"
    )

    def __repr__(self):
        username = Users.query.filter_by(id=self.created_by).first().username
        return f"<Record {self.name} by {username}>"

    def get_user_profile(self):
        return Users.query.filter_by(id=self.created_by).first()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "created_by": self.created_by,
        }


class Entries(db.Model):
    __tablename__ = "entries"
    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    subtitle: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(String, nullable=True)
    quote: Mapped[str] = mapped_column(String, nullable=True)
    # Foreign Key to Record
    record_id: Mapped[str] = mapped_column(
        Uuid, ForeignKey("records.id"), nullable=False
    )
    # Relationship to Record
    record: Mapped["Records"] = relationship("Records", back_populates="entries")

    def __repr__(self):
        return f"<Entry {self.title} IN {self.record}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "summary": self.summary,
            "quote": self.quote,
            "record": self.record,
        }


class GeneralSummary(db.Model):
    __tablename__ = "general_summary"
    id: Mapped[str] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(String, nullable=True)
    # Foreign Key to Record
    record_id: Mapped[str] = mapped_column(
        Uuid, ForeignKey("records.id"), nullable=False
    )
    # Relationship to Record
    record: Mapped["Records"] = relationship("Records", back_populates="general_summary")

    def __repr__(self):
        return f"<General Summary {self.title} FOR {self.record}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "record": self.record,
        }
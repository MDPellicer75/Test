"""Initial schema - users, trips, trip_days, activities, travel_dna

Revision ID: 001
Revises: None
Create Date: 2026-07-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, index=True, nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("language", sa.String(10), server_default="es"),
        sa.Column("country", sa.String(100), nullable=True),
        sa.Column("photo_url", sa.String(500), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )

    # Trips
    op.create_table(
        "trips",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("destination", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("budget", sa.Float(), nullable=True),
        sa.Column("currency", sa.String(3), server_default="USD"),
        sa.Column(
            "status",
            sa.Enum("planning", "active", "completed", "cancelled", name="tripstatus"),
            server_default="planning",
        ),
        sa.Column("travelers_count", sa.Integer(), server_default="1"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )

    # Trip Days
    op.create_table(
        "trip_days",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "trip_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("trips.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("day_number", sa.Integer(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
    )

    # Activities
    op.create_table(
        "activities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "trip_day_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("trip_days.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("location_name", sa.String(300), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("start_time", sa.Time(), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("cost", sa.Float(), nullable=True),
        sa.Column("currency", sa.String(3), server_default="USD"),
        sa.Column("category", sa.String(50), nullable=True),
        sa.Column("booking_url", sa.String(500), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("order", sa.Integer(), server_default="0"),
    )

    # Travel DNA
    op.create_table(
        "travel_dna",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            unique=True,
            nullable=False,
        ),
        sa.Column("food_score", sa.Float(), server_default="0.5"),
        sa.Column("museum_score", sa.Float(), server_default="0.5"),
        sa.Column("walking_score", sa.Float(), server_default="0.5"),
        sa.Column("nightlife_score", sa.Float(), server_default="0.5"),
        sa.Column("history_score", sa.Float(), server_default="0.5"),
        sa.Column("nature_score", sa.Float(), server_default="0.5"),
        sa.Column("photography_score", sa.Float(), server_default="0.5"),
        sa.Column("adventure_score", sa.Float(), server_default="0.5"),
        sa.Column("shopping_score", sa.Float(), server_default="0.5"),
        sa.Column("relaxation_score", sa.Float(), server_default="0.5"),
        sa.Column("sports_score", sa.Float(), server_default="0.5"),
        sa.Column("art_score", sa.Float(), server_default="0.5"),
        sa.Column("budget_level", sa.Integer(), server_default="3"),
        sa.Column("pace", sa.Integer(), server_default="3"),
        sa.Column("planning_style", sa.Integer(), server_default="3"),
        sa.Column("social_level", sa.Integer(), server_default="3"),
        sa.Column("fitness_level", sa.Integer(), server_default="3"),
        sa.Column("max_walking_km", sa.Float(), server_default="10.0"),
        sa.Column("dietary_preferences", sa.String(200), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_table("travel_dna")
    op.drop_table("activities")
    op.drop_table("trip_days")
    op.drop_table("trips")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS tripstatus")

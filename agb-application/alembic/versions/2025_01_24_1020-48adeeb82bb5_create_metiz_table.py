"""create metiz table

Revision ID: 48adeeb82bb5
Revises: e0d98a4bf7ca
Create Date: 2025-01-24 10:20:15.102428

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "48adeeb82bb5"
down_revision: Union[str, None] = "e0d98a4bf7ca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "metizs",
        sa.Column("number_in_catalog", sa.String(length=50), nullable=True),
        sa.Column(
            "number_in_catalog_agb", sa.String(length=50), nullable=True
        ),
        sa.Column("name_in_catalog", sa.String(length=50), nullable=True),
        sa.Column("name_in_KD", sa.String(length=50), nullable=True),
        sa.Column("name_in_catalog_agb", sa.String(length=50), nullable=True),
        sa.Column("standard", sa.String(length=50), nullable=True),
        sa.Column("hardware_type", sa.String(length=50), nullable=True),
        sa.Column("thread_profile", sa.String(length=50), nullable=True),
        sa.Column("nominal_diameter", sa.String(length=50), nullable=True),
        sa.Column("thread_pitch", sa.String(length=50), nullable=True),
        sa.Column("length", sa.String(length=50), nullable=True),
        sa.Column("strength_class", sa.String(length=50), nullable=True),
        sa.Column("Material_or_coating", sa.String(length=50), nullable=True),
        sa.Column("assigned", sa.String(length=50), nullable=False),
        sa.Column("note", sa.String(length=50), nullable=True),
        sa.Column("applicability", sa.String(length=50), nullable=True),
        sa.Column("date", sa.String(length=50), nullable=True),
        sa.Column("marked_for_deletion", sa.Boolean(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_metizs")),
        sa.UniqueConstraint(
            "number_in_catalog", name=op.f("uq_metizs_number_in_catalog")
        ),
        sa.UniqueConstraint(
            "number_in_catalog_agb",
            name=op.f("uq_metizs_number_in_catalog_agb"),
        ),
    )



def downgrade() -> None:
    op.drop_table("metizs")


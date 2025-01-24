"""create all other table

Revision ID: 2698c7ed6095
Revises: d0299c5ca509
Create Date: 2025-01-24 15:23:03.485377

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2698c7ed6095"
down_revision: Union[str, None] = "d0299c5ca509"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "according_to_the_drawings",
        sa.Column("name", sa.String(length=50), nullable=True),
        sa.Column("number_in_catalog", sa.String(length=50), nullable=True),
        sa.Column(
            "number_in_catalog_agb", sa.String(length=50), nullable=True
        ),
        sa.Column("name_in_catalog", sa.String(length=50), nullable=True),
        sa.Column("applicability", sa.String(length=50), nullable=True),
        sa.Column("note", sa.String(length=50), nullable=True),
        sa.Column("developed", sa.String(length=50), nullable=False),
        sa.Column("KD", sa.String(length=50), nullable=True),
        sa.Column("date", sa.String(length=50), nullable=True),
        sa.Column("marked_for_deletion", sa.Boolean(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_according_to_the_drawings")
        ),
        sa.UniqueConstraint(
            "number_in_catalog",
            name=op.f("uq_according_to_the_drawings_number_in_catalog"),
        ),
        sa.UniqueConstraint(
            "number_in_catalog_agb",
            name=op.f("uq_according_to_the_drawings_number_in_catalog_agb"),
        ),
    )
    op.create_table(
        "adapters_and_plugss",
        sa.Column("number_in_catalog", sa.String(length=50), nullable=True),
        sa.Column(
            "number_in_catalog_agb", sa.String(length=50), nullable=True
        ),
        sa.Column("name_in_catalog", sa.String(length=50), nullable=True),
        sa.Column("name_in_KD", sa.String(length=50), nullable=True),
        sa.Column("name_in_catalog_agb", sa.String(length=50), nullable=True),
        sa.Column("adapter_type", sa.String(length=50), nullable=True),
        sa.Column("adapter_angle", sa.String(length=50), nullable=True),
        sa.Column("exit_first", sa.String(length=50), nullable=True),
        sa.Column("exit_second", sa.String(length=50), nullable=True),
        sa.Column("center_exit", sa.String(length=50), nullable=True),
        sa.Column("name_in_OEM", sa.String(length=50), nullable=True),
        sa.Column("assigned", sa.String(length=50), nullable=False),
        sa.Column("note", sa.String(length=50), nullable=True),
        sa.Column("applicability", sa.String(length=50), nullable=True),
        sa.Column("date", sa.String(length=50), nullable=True),
        sa.Column("marked_for_deletion", sa.Boolean(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_adapters_and_plugss")),
        sa.UniqueConstraint(
            "number_in_catalog",
            name=op.f("uq_adapters_and_plugss_number_in_catalog"),
        ),
        sa.UniqueConstraint(
            "number_in_catalog_agb",
            name=op.f("uq_adapters_and_plugss_number_in_catalog_agb"),
        ),
    )
    op.create_table(
        "projects",
        sa.Column("classifier", sa.String(length=50), nullable=False),
        sa.Column("project", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_projects")),
        sa.UniqueConstraint("classifier", name=op.f("uq_projects_classifier")),
        sa.UniqueConstraint("project", name=op.f("uq_projects_project")),
    )
    op.create_table(
        "purchased_hydroperforators",
        sa.Column("number_in_catalog", sa.String(length=50), nullable=True),
        sa.Column(
            "number_in_catalog_agb", sa.String(length=50), nullable=True
        ),
        sa.Column("name_in_catalog", sa.String(length=50), nullable=True),
        sa.Column("name_in_KD", sa.String(length=50), nullable=True),
        sa.Column("name_in_catalog_agb", sa.String(length=50), nullable=True),
        sa.Column("name_in_OEM", sa.String(length=50), nullable=True),
        sa.Column("assigned", sa.String(length=50), nullable=False),
        sa.Column("note", sa.String(length=50), nullable=True),
        sa.Column("applicability", sa.String(length=50), nullable=True),
        sa.Column("marked_for_deletion", sa.Boolean(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_purchased_hydroperforators")
        ),
        sa.UniqueConstraint(
            "number_in_catalog",
            name=op.f("uq_purchased_hydroperforators_number_in_catalog"),
        ),
        sa.UniqueConstraint(
            "number_in_catalog_agb",
            name=op.f("uq_purchased_hydroperforators_number_in_catalog_agb"),
        ),
    )
    op.create_table(
        "purchaseds",
        sa.Column(
            "number_in_catalog_agb", sa.String(length=50), nullable=True
        ),
        sa.Column("name_in_catalog", sa.String(length=50), nullable=True),
        sa.Column("name_in_KD", sa.String(length=50), nullable=True),
        sa.Column("name_in_catalog_agb", sa.String(length=50), nullable=True),
        sa.Column("name_in_OEM", sa.String(length=50), nullable=True),
        sa.Column("assigned", sa.String(length=50), nullable=False),
        sa.Column("date", sa.String(length=50), nullable=True),
        sa.Column("applicability", sa.String(length=50), nullable=True),
        sa.Column("note", sa.String(length=50), nullable=True),
        sa.Column("marked_for_deletion", sa.Boolean(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_purchaseds")),
        sa.UniqueConstraint(
            "number_in_catalog_agb",
            name=op.f("uq_purchaseds_number_in_catalog_agb"),
        ),
    )
    op.create_table(
        "rwds",
        sa.Column("number", sa.String(length=50), nullable=True),
        sa.Column("date", sa.String(length=50), nullable=True),
        sa.Column("article_number_agb", sa.String(length=50), nullable=True),
        sa.Column("nomenclature", sa.String(length=50), nullable=True),
        sa.Column("note", sa.String(length=50), nullable=True),
        sa.Column("marked_for_deletion", sa.Boolean(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_rwds")),
        sa.UniqueConstraint("nomenclature", name=op.f("uq_rwds_nomenclature")),
        sa.UniqueConstraint("number", name=op.f("uq_rwds_number")),
    )



def downgrade() -> None:

    op.drop_table("rwds")
    op.drop_table("purchaseds")
    op.drop_table("purchased_hydroperforators")
    op.drop_table("projects")
    op.drop_table("adapters_and_plugss")
    op.drop_table("according_to_the_drawings")


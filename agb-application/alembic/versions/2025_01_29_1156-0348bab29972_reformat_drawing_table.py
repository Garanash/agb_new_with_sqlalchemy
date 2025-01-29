"""reformat drawing table

Revision ID: 0348bab29972
Revises: 2698c7ed6095
Create Date: 2025-01-29 11:56:43.023104

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0348bab29972"
down_revision: Union[str, None] = "2698c7ed6095"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "according_to_the_drawings",
        sa.Column("name_in_KD", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "according_to_the_drawings",
        sa.Column("first_applicability", sa.String(length=50), nullable=True),
    )
    op.drop_column("according_to_the_drawings", "applicability")



def downgrade() -> None:

    op.add_column(
        "according_to_the_drawings",
        sa.Column(
            "applicability",
            sa.VARCHAR(length=50),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("according_to_the_drawings", "first_applicability")
    op.drop_column("according_to_the_drawings", "name_in_KD")


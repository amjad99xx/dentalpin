"""core — clinics.tax_id becomes nullable.

Tax ID is not universally established at setup time (e.g. a clinic
mid-registration, or a jurisdiction where it isn't required). Setup
and clinic-info editing both already treat it as optional on the
frontend; the database must not be the one place that still rejects
an empty value.

Revision ID: 0010
Revises: 0009
Create Date: 2026-10-31
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0010"
down_revision: str | None = "0009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("clinics", "tax_id", existing_type=sa.String(length=20), nullable=True)


def downgrade() -> None:
    op.alter_column("clinics", "tax_id", existing_type=sa.String(length=20), nullable=False)

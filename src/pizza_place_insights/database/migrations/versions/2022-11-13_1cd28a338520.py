"""first migration

Revision ID: 1cd28a338520
Revises:
Create Date: 2022-11-13 04:13:39.985982

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "1cd28a338520"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "pizza_types",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("category", sa.String, nullable=False),
        sa.Column("ingredients", postgresql.ARRAY(sa.String, dimensions=1), nullable=False),
    )

    op.create_table(
        "pizzas",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("pizza_type_id", sa.String, sa.ForeignKey("pizza_types.id"), nullable=False),
        sa.Column("size", sa.String, nullable=False),
        sa.Column("price", sa.DECIMAL, nullable=False),
    )

    op.create_table(
        "order_imports",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("import_datetime", sa.DateTime, nullable=False),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "order_import_id",
            sa.Integer,
            sa.ForeignKey("order_imports.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("time", sa.Time, nullable=False),
    )

    op.create_table(
        "order_details",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("pizza_id", sa.String, sa.ForeignKey("pizzas.id"), nullable=False),
        sa.Column(
            "order_id", sa.Integer, sa.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("quantity", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("order_details")
    op.drop_table("orders")
    op.drop_table("order_imports")
    op.drop_table("pizzas")
    op.drop_table("pizza_types")

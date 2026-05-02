"""migrate booking seats to json"""

import json
from alembic import op
import sqlalchemy as sa


revision = "20260420_0002"
down_revision = "20260420_0001"
branch_labels = None
depends_on = None


def _split_seats(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [seat.strip() for seat in str(value).split(",") if seat.strip()]


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("bookings")}

    if "seats_json" not in columns:
        with op.batch_alter_table("bookings") as batch_op:
            batch_op.add_column(sa.Column("seats_json", sa.JSON(), nullable=True))

    bookings = bind.execute(sa.text("SELECT id, seats FROM bookings")).fetchall()
    for booking_id, seats in bookings:
        bind.execute(
            sa.text("UPDATE bookings SET seats_json = :seats WHERE id = :booking_id"),
            {"seats": json.dumps(_split_seats(seats)), "booking_id": booking_id},
        )

    with op.batch_alter_table("bookings") as batch_op:
        batch_op.drop_column("seats")
        batch_op.alter_column("seats_json", new_column_name="seats", existing_type=sa.JSON(), nullable=False)


def downgrade() -> None:
    bind = op.get_bind()
    with op.batch_alter_table("bookings") as batch_op:
        batch_op.add_column(sa.Column("seats_text", sa.String(), nullable=True))

    bookings = bind.execute(sa.text("SELECT id, seats FROM bookings")).fetchall()
    for booking_id, seats in bookings:
        normalized = seats if isinstance(seats, list) else json.loads(seats or "[]")
        bind.execute(
            sa.text("UPDATE bookings SET seats_text = :seats WHERE id = :booking_id"),
            {"seats": ",".join(normalized), "booking_id": booking_id},
        )

    with op.batch_alter_table("bookings") as batch_op:
        batch_op.drop_column("seats")
        batch_op.alter_column("seats_text", new_column_name="seats", existing_type=sa.String(), nullable=True)

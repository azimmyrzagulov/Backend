"""set not null constraints"""

from alembic import op
import sqlalchemy as sa


revision = "20260420_0003"
down_revision = "20260420_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column("email", existing_type=sa.String(), nullable=False)
        batch_op.alter_column("hashed_password", existing_type=sa.String(), nullable=False)
        batch_op.alter_column("role", existing_type=sa.String(), nullable=False)

    with op.batch_alter_table("movies") as batch_op:
        batch_op.alter_column("title", existing_type=sa.String(), nullable=False)
        batch_op.alter_column("description", existing_type=sa.String(), nullable=False)
        batch_op.alter_column("genre", existing_type=sa.String(), nullable=False)
        batch_op.alter_column("duration", existing_type=sa.Integer(), nullable=False)
        batch_op.alter_column("release_date", existing_type=sa.DateTime(), nullable=False)
        batch_op.alter_column("poster_url", existing_type=sa.String(), nullable=False)

    with op.batch_alter_table("theaters") as batch_op:
        batch_op.alter_column("name", existing_type=sa.String(), nullable=False)
        batch_op.alter_column("location", existing_type=sa.String(), nullable=False)

    with op.batch_alter_table("bookings") as batch_op:
        batch_op.alter_column("user_id", existing_type=sa.Integer(), nullable=False)
        batch_op.alter_column("movie_id", existing_type=sa.Integer(), nullable=False)
        batch_op.alter_column("theater_id", existing_type=sa.Integer(), nullable=False)
        batch_op.alter_column("show_time", existing_type=sa.DateTime(), nullable=False)


def downgrade() -> None:
    with op.batch_alter_table("bookings") as batch_op:
        batch_op.alter_column("show_time", existing_type=sa.DateTime(), nullable=True)
        batch_op.alter_column("theater_id", existing_type=sa.Integer(), nullable=True)
        batch_op.alter_column("movie_id", existing_type=sa.Integer(), nullable=True)
        batch_op.alter_column("user_id", existing_type=sa.Integer(), nullable=True)

    with op.batch_alter_table("theaters") as batch_op:
        batch_op.alter_column("location", existing_type=sa.String(), nullable=True)
        batch_op.alter_column("name", existing_type=sa.String(), nullable=True)

    with op.batch_alter_table("movies") as batch_op:
        batch_op.alter_column("poster_url", existing_type=sa.String(), nullable=True)
        batch_op.alter_column("release_date", existing_type=sa.DateTime(), nullable=True)
        batch_op.alter_column("duration", existing_type=sa.Integer(), nullable=True)
        batch_op.alter_column("genre", existing_type=sa.String(), nullable=True)
        batch_op.alter_column("description", existing_type=sa.String(), nullable=True)
        batch_op.alter_column("title", existing_type=sa.String(), nullable=True)

    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column("role", existing_type=sa.String(), nullable=True)
        batch_op.alter_column("hashed_password", existing_type=sa.String(), nullable=True)
        batch_op.alter_column("email", existing_type=sa.String(), nullable=True)

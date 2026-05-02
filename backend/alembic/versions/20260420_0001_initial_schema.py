"""initial schema"""

from alembic import op
import sqlalchemy as sa


revision = "20260420_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("role", sa.String(), nullable=True),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_id", "users", ["id"], unique=False)

    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("genre", sa.String(), nullable=True),
        sa.Column("duration", sa.Integer(), nullable=True),
        sa.Column("release_date", sa.DateTime(), nullable=True),
        sa.Column("poster_url", sa.String(), nullable=True),
    )
    op.create_index("ix_movies_id", "movies", ["id"], unique=False)
    op.create_index("ix_movies_title", "movies", ["title"], unique=False)

    op.create_table(
        "theaters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("location", sa.String(), nullable=True),
    )
    op.create_index("ix_theaters_id", "theaters", ["id"], unique=False)

    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("movie_id", sa.Integer(), sa.ForeignKey("movies.id"), nullable=True),
        sa.Column("theater_id", sa.Integer(), sa.ForeignKey("theaters.id"), nullable=True),
        sa.Column("show_time", sa.DateTime(), nullable=True),
        sa.Column("seats", sa.String(), nullable=True),
    )
    op.create_index("ix_bookings_id", "bookings", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_bookings_id", table_name="bookings")
    op.drop_table("bookings")
    op.drop_index("ix_theaters_id", table_name="theaters")
    op.drop_table("theaters")
    op.drop_index("ix_movies_title", table_name="movies")
    op.drop_index("ix_movies_id", table_name="movies")
    op.drop_table("movies")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

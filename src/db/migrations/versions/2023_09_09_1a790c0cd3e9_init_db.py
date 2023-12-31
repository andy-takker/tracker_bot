"""Init db

Revision ID: 1a790c0cd3e9
Revises:
Create Date: 2023-09-09 18:37:15.583176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1a790c0cd3e9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "system_message",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("value", sa.String(length=1024), nullable=False),
        sa.Column("mtype", sa.String(length=16), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__system_message")),
    )
    op.create_index(
        op.f("ix__system_message__mtype"), "system_message", ["mtype"], unique=False
    )
    op.create_table(
        "user",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("period", sa.Integer(), nullable=False),
        sa.Column("time_zone", sa.SmallInteger(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("is_working", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__user")),
    )
    op.create_index(op.f("ix__user__created_at"), "user", ["created_at"], unique=False)
    op.create_index(op.f("ix__user__period"), "user", ["period"], unique=False)
    op.create_table(
        "track",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("started_work_at", sa.DateTime(), nullable=False),
        sa.Column("ended_work_at", sa.DateTime(), nullable=False),
        sa.Column("message", sa.String(length=300), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name=op.f("fk__track__user_id__user")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__track")),
    )
    op.create_index(
        op.f("ix__track__created_at"), "track", ["created_at"], unique=False
    )
    op.create_index(op.f("ix__track__user_id"), "track", ["user_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix__track__user_id"), table_name="track")
    op.drop_index(op.f("ix__track__created_at"), table_name="track")
    op.drop_table("track")
    op.drop_index(op.f("ix__user__period"), table_name="user")
    op.drop_index(op.f("ix__user__created_at"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix__system_message__mtype"), table_name="system_message")
    op.drop_table("system_message")
    # ### end Alembic commands ###

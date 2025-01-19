"""Initial migration

Revision ID: ce750e0a2ea0
Revises: 9f11edaa07a9
Create Date: 2025-01-17 14:10:07.851687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce750e0a2ea0'
down_revision: Union[str, None] = '9f11edaa07a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('in_progres', 'done', 'cancel', name='statusproject'), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_image'), 'projects', ['image'], unique=False)
    op.create_table('project_programmer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('programmer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['programmer_id'], ['employees.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_employees_image', table_name='employees')
    op.create_index(op.f('ix_employees_image'), 'employees', ['image'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_employees_image'), table_name='employees')
    op.create_index('ix_employees_image', 'employees', ['image'], unique=True)
    op.drop_table('project_programmer')
    op.drop_index(op.f('ix_projects_image'), table_name='projects')
    op.drop_table('projects')
    # ### end Alembic commands ###

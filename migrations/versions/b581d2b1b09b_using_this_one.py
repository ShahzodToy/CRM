"""using this one 

Revision ID: b581d2b1b09b
Revises: 39f1326543cd
Create Date: 2025-02-11 22:58:25.833627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b581d2b1b09b'
down_revision: Union[str, None] = '39f1326543cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('employees_position_id_fkey', 'employees', type_='foreignkey')
    op.create_foreign_key(None, 'employees', 'positions', ['position_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('expences_employee_salary_id_fkey', 'expences', type_='foreignkey')
    op.create_foreign_key(None, 'expences', 'employees', ['employee_salary_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('incomes_project_id_fkey', 'incomes', type_='foreignkey')
    op.create_foreign_key(None, 'incomes', 'projects', ['project_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('operators_operator_type_id_fkey', 'operators', type_='foreignkey')
    op.create_foreign_key(None, 'operators', 'operator_type', ['operator_type_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('project_programmer_project_id_fkey', 'project_programmer', type_='foreignkey')
    op.drop_constraint('project_programmer_programmer_id_fkey', 'project_programmer', type_='foreignkey')
    op.create_foreign_key(None, 'project_programmer', 'projects', ['project_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'project_programmer', 'employees', ['programmer_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project_programmer', type_='foreignkey')
    op.drop_constraint(None, 'project_programmer', type_='foreignkey')
    op.create_foreign_key('project_programmer_programmer_id_fkey', 'project_programmer', 'employees', ['programmer_id'], ['id'])
    op.create_foreign_key('project_programmer_project_id_fkey', 'project_programmer', 'projects', ['project_id'], ['id'])
    op.drop_constraint(None, 'operators', type_='foreignkey')
    op.create_foreign_key('operators_operator_type_id_fkey', 'operators', 'operator_type', ['operator_type_id'], ['id'], onupdate='CASCADE')
    op.drop_constraint(None, 'incomes', type_='foreignkey')
    op.create_foreign_key('incomes_project_id_fkey', 'incomes', 'projects', ['project_id'], ['id'], onupdate='CASCADE')
    op.drop_constraint(None, 'expences', type_='foreignkey')
    op.create_foreign_key('expences_employee_salary_id_fkey', 'expences', 'employees', ['employee_salary_id'], ['id'], onupdate='CASCADE')
    op.drop_constraint(None, 'employees', type_='foreignkey')
    op.create_foreign_key('employees_position_id_fkey', 'employees', 'positions', ['position_id'], ['id'], onupdate='CASCADE')
    # ### end Alembic commands ###

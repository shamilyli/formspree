"""email templates and plan enum

Revision ID: 7446b8bbc888
Revises: a156683c29f2
Create Date: 2018-09-19 22:38:57.679264

"""

# revision identifiers, used by Alembic.
revision = '7446b8bbc888'
down_revision = 'a156683c29f2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM

plans = ENUM('v1_free', 'v1_gold', 'v1_platinum', name='plans', create_type=False)

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email_templates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.Text(), nullable=False),
    sa.Column('from_name', sa.Text(), nullable=False),
    sa.Column('style', sa.Text(), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('form_id')
    )
    op.alter_column('submissions', 'form_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    plans.create(op.get_bind(), checkfirst=True)
    op.add_column('users', sa.Column('plan', plans, nullable=True))
    op.execute("UPDATE users SET plan = 'v1_gold' WHERE upgraded")
    op.execute("UPDATE users SET plan = 'v1_free' WHERE NOT upgraded")
    op.drop_column('users', 'upgraded')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('upgraded', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.execute("UPDATE users SET upgraded = true WHERE plan != 'v1_free'")
    op.execute("UPDATE users SET upgraded = false WHERE plan = 'v1_free'")
    op.drop_column('users', 'plan')
    op.alter_column('submissions', 'form_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_table('email_templates')
    # ### end Alembic commands ###
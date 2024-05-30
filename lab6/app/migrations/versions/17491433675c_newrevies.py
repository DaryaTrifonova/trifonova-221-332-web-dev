"""NewRevies

Revision ID: 17491433675c
Revises: 5b33dfa90058
Create Date: 2024-05-30 13:33:10.445193

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '17491433675c'
down_revision = '5b33dfa90058'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.alter_column('rating',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.Enum('EXCELLENT', 'GOOD', 'SATISFACTORY', 'UNSATISFACTORY', 'POOR', 'TERRIBLE', name='ratingenum'),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.alter_column('rating',
               existing_type=sa.Enum('EXCELLENT', 'GOOD', 'SATISFACTORY', 'UNSATISFACTORY', 'POOR', 'TERRIBLE', name='ratingenum'),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)

    # ### end Alembic commands ###

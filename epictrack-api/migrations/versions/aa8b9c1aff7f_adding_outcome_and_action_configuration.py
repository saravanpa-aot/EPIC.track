"""adding outcome and action configuration

Revision ID: aa8b9c1aff7f
Revises: 5547605183f6
Create Date: 2023-09-26 20:13:37.293253

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'aa8b9c1aff7f'
down_revision = '5547605183f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('outcome_configurations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('event_configuration_id', sa.Integer(), nullable=False),
    sa.Column('sort_order', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column('updated_by', sa.String(length=255), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default='t', nullable=False),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=False),
    sa.ForeignKeyConstraint(['event_configuration_id'], ['event_configurations.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sqlite_autoincrement=True
    )
    op.create_table('outcome_configurations_history',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(), autoincrement=False, nullable=False),
    sa.Column('event_configuration_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('sort_order', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('created_by', sa.String(length=255), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), autoincrement=False, nullable=True),
    sa.Column('updated_by', sa.String(length=255), autoincrement=False, nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.Boolean(), autoincrement=False, nullable=False),
    sa.Column('is_deleted', sa.Boolean(), autoincrement=False, nullable=False),
    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('during', postgresql.TSTZRANGE(), nullable=True),
    sa.ForeignKeyConstraint(['event_configuration_id'], ['event_configurations.id'], ),
    sa.PrimaryKeyConstraint('id', 'pk'),
    sqlite_autoincrement=True
    )
    op.create_table('action_configurations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('outcome_configuration_id', sa.Integer(), nullable=False),
    sa.Column('action_id', sa.Integer(), nullable=False),
    sa.Column('additional_params', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('sort_order', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column('updated_by', sa.String(length=255), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default='t', nullable=False),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=False),
    sa.ForeignKeyConstraint(['action_id'], ['actions.id'], ),
    sa.ForeignKeyConstraint(['outcome_configuration_id'], ['outcome_configurations.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sqlite_autoincrement=True
    )
    op.create_table('action_configurations_history',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('outcome_configuration_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('action_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('additional_params', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('sort_order', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('created_by', sa.String(length=255), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), autoincrement=False, nullable=True),
    sa.Column('updated_by', sa.String(length=255), autoincrement=False, nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.Boolean(), autoincrement=False, nullable=False),
    sa.Column('is_deleted', sa.Boolean(), autoincrement=False, nullable=False),
    sa.Column('pk', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('during', postgresql.TSTZRANGE(), nullable=True),
    sa.ForeignKeyConstraint(['action_id'], ['actions.id'], ),
    sa.ForeignKeyConstraint(['outcome_configuration_id'], ['outcome_configurations.id'], ),
    sa.PrimaryKeyConstraint('id', 'pk'),
    sqlite_autoincrement=True
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('action_configurations_history')
    op.drop_table('action_configurations')
    op.drop_table('outcome_configurations_history')
    op.drop_table('outcome_configurations')
    # ### end Alembic commands ###
"""Initial migration - Create all tables

Revision ID: 001_initial
Revises:
Create Date: 2026-06-10

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('username', sa.String(32), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'])
    op.create_index(op.f('ix_users_username'), 'users', ['username'])

    op.create_table(
        'refresh_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('jti_hash', sa.String(64), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('jti_hash'),
    )
    op.create_index(op.f('ix_refresh_tokens_jti_hash'), 'refresh_tokens', ['jti_hash'])
    op.create_index(op.f('ix_refresh_tokens_user_id'), 'refresh_tokens', ['user_id'])

    op.create_table(
        'workspaces',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('language', sa.String(32), nullable=False),
        sa.Column('code', sa.Text(), nullable=True),
        sa.Column('custom_input', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_workspaces_created_at'), 'workspaces', ['created_at'])
    op.create_index(op.f('ix_workspaces_language'), 'workspaces', ['language'])
    op.create_index(op.f('ix_workspaces_user_id'), 'workspaces', ['user_id'])

    op.create_table(
        'problem_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('problem_statement', sa.Text(), nullable=False),
        sa.Column('response', sa.Text(), nullable=False),
        sa.Column('model_used', sa.String(64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_problem_analyses_created_at'), 'problem_analyses', ['created_at'])
    op.create_index(op.f('ix_problem_analyses_model_used'), 'problem_analyses', ['model_used'])
    op.create_index(op.f('ix_problem_analyses_user_id'), 'problem_analyses', ['user_id'])

    op.create_table(
        'ai_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('workspace_id', sa.Integer(), nullable=True),
        sa.Column('action_type', sa.String(64), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('response', sa.Text(), nullable=False),
        sa.Column('model_used', sa.String(64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_ai_sessions_action_type'), 'ai_sessions', ['action_type'])
    op.create_index(op.f('ix_ai_sessions_created_at'), 'ai_sessions', ['created_at'])
    op.create_index(op.f('ix_ai_sessions_model_used'), 'ai_sessions', ['model_used'])
    op.create_index(op.f('ix_ai_sessions_user_id'), 'ai_sessions', ['user_id'])
    op.create_index(op.f('ix_ai_sessions_workspace_id'), 'ai_sessions', ['workspace_id'])

    op.create_table(
        'code_executions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('workspace_id', sa.Integer(), nullable=True),
        sa.Column('language', sa.String(32), nullable=False),
        sa.Column('code', sa.Text(), nullable=False),
        sa.Column('custom_input', sa.Text(), nullable=True),
        sa.Column('output', sa.Text(), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('execution_time_ms', sa.Float(), nullable=True),
        sa.Column('memory_usage_bytes', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(32), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_code_executions_created_at'), 'code_executions', ['created_at'])
    op.create_index(op.f('ix_code_executions_language'), 'code_executions', ['language'])
    op.create_index(op.f('ix_code_executions_status'), 'code_executions', ['status'])
    op.create_index(op.f('ix_code_executions_user_id'), 'code_executions', ['user_id'])
    op.create_index(op.f('ix_code_executions_workspace_id'), 'code_executions', ['workspace_id'])


def downgrade() -> None:
    op.drop_index(op.f('ix_code_executions_workspace_id'), table_name='code_executions')
    op.drop_index(op.f('ix_code_executions_user_id'), table_name='code_executions')
    op.drop_index(op.f('ix_code_executions_status'), table_name='code_executions')
    op.drop_index(op.f('ix_code_executions_language'), table_name='code_executions')
    op.drop_index(op.f('ix_code_executions_created_at'), table_name='code_executions')
    op.drop_table('code_executions')

    op.drop_index(op.f('ix_ai_sessions_workspace_id'), table_name='ai_sessions')
    op.drop_index(op.f('ix_ai_sessions_user_id'), table_name='ai_sessions')
    op.drop_index(op.f('ix_ai_sessions_model_used'), table_name='ai_sessions')
    op.drop_index(op.f('ix_ai_sessions_created_at'), table_name='ai_sessions')
    op.drop_index(op.f('ix_ai_sessions_action_type'), table_name='ai_sessions')
    op.drop_table('ai_sessions')

    op.drop_index(op.f('ix_problem_analyses_user_id'), table_name='problem_analyses')
    op.drop_index(op.f('ix_problem_analyses_model_used'), table_name='problem_analyses')
    op.drop_index(op.f('ix_problem_analyses_created_at'), table_name='problem_analyses')
    op.drop_table('problem_analyses')

    op.drop_index(op.f('ix_workspaces_user_id'), table_name='workspaces')
    op.drop_index(op.f('ix_workspaces_language'), table_name='workspaces')
    op.drop_index(op.f('ix_workspaces_created_at'), table_name='workspaces')
    op.drop_table('workspaces')

    op.drop_index(op.f('ix_refresh_tokens_user_id'), table_name='refresh_tokens')
    op.drop_index(op.f('ix_refresh_tokens_jti_hash'), table_name='refresh_tokens')
    op.drop_table('refresh_tokens')

    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

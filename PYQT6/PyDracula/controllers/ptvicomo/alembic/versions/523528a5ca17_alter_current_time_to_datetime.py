"""alter current_time to datetime

Revision ID: 523528a5ca17
Revises: 80ffb6696d77
Create Date: 2025-03-21 20:25:51.754520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.inspection import inspect

# from controllers.ptvicomo.config_ptvicomo_04 import TABLE_NAME, DB_TYPE

TABLE_NAME = 'data_record'
DB_TYPE = 'sqlite'

# revision identifiers, used by Alembic.
revision: str = '523528a5ca17'
down_revision: Union[str, None] = '80ffb6696d77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def column_exists(inspector, table_name, column_name):
    """检查指定表中是否存在指定列"""
    columns = inspector.get_columns(table_name)
    for column in columns:
        if column['name'] == column_name:
            return column
    return None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = inspect(bind)

    column_info = column_exists(inspector, TABLE_NAME, '当前时间')
    if not column_info:
        print(f"Column '当前时间' does not exist in table '{TABLE_NAME}'. Skipping upgrade.")
        return

    if column_info['type'] != sa.String or column_info['type'] != sa.TEXT:
        print(f"Column '当前时间' is not of type String in table '{TABLE_NAME}'. Skipping upgrade.")
        return

    try:
        if DB_TYPE == 'sqlite':
            _upgrade_sqlite(TABLE_NAME, inspector)
        elif DB_TYPE == 'mysql':
            _upgrade_mysql(TABLE_NAME, inspector)
        else:
            raise ValueError(f"Unsupported database type: {DB_TYPE}")
    except Exception as e:
        print(f"Error during upgrade: {e}")


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = inspect(bind)

    column_info = column_exists(inspector, TABLE_NAME, '当前时间')
    if not column_info:
        print(f"Column '当前时间' does not exist in table '{TABLE_NAME}'. Skipping downgrade.")
        return

    if column_info['type'] != sa.DATETIME:
        print(f"Column '当前时间' is not of type DATETIME in table '{TABLE_NAME}'. Skipping downgrade.")
        return

    try:
        if DB_TYPE == 'sqlite':
            _downgrade_sqlite(TABLE_NAME, inspector)
        elif DB_TYPE == 'mysql':
            _downgrade_mysql(TABLE_NAME, inspector)
        else:
            raise ValueError(f"Unsupported database type: {DB_TYPE}")
    except Exception as e:
        print(f"Error during downgrade: {e}")


def _upgrade_sqlite(table_name, inspector):
    """SQLite 升级逻辑"""
    op.alter_column(table_name, '当前时间', new_column_name='当前时间_old', existing_type=sa.String)
    op.add_column(table_name, sa.Column('当前时间_new', sa.DATETIME))
    op.execute(op.text(f'UPDATE "{table_name}" SET 当前时间_new = STR_TO_DATE(当前时间_old, "%Y-%m-%d %H:%i:%s")'))
    op.drop_column(table_name, '当前时间_old')
    op.alter_column(table_name, '当前时间_new', new_column_name='当前时间')


def _upgrade_mysql(table_name, inspector):
    """MySQL 升级逻辑"""
    op.alter_column(table_name, '当前时间', new_column_name='当前时间_old', existing_type=sa.String)
    op.add_column(table_name, sa.Column('当前时间_new', sa.DATETIME))
    op.execute(op.text(f'UPDATE `{table_name}` SET 当前时间_new = STR_TO_DATE(当前时间_old, "%Y-%m-%d %H:%i:%s")'))
    op.drop_column(table_name, '当前时间_old')
    op.alter_column(table_name, '当前时间_new', new_column_name='当前时间')


def _downgrade_sqlite(table_name, inspector):
    """SQLite 降级逻辑"""
    op.alter_column(table_name, '当前时间', new_column_name='当前时间_new', existing_type=sa.DATETIME)
    op.add_column(table_name, sa.Column('当前时间_old', sa.String))
    op.execute(op.text(f'UPDATE "{table_name}" SET 当前时间_old = datetime(当前时间_new)'))
    op.drop_column(table_name, '当前时间_new')
    op.alter_column(table_name, '当前时间_old', new_column_name='当前时间')


def _downgrade_mysql(table_name, inspector):
    """MySQL 降级逻辑"""
    op.alter_column(table_name, '当前时间', new_column_name='当前时间_new', existing_type=sa.DATETIME)
    op.add_column(table_name, sa.Column('当前时间_old', sa.String))
    op.execute(op.text(f'UPDATE `{table_name}` SET 当前时间_old = DATE_FORMAT(当前时间_new, "%Y-%m-%d %H:%i:%s")'))
    op.drop_column(table_name, '当前时间_new')
    op.alter_column(table_name, '当前时间_old', new_column_name='当前时间')

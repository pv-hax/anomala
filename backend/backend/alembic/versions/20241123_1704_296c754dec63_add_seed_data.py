"""Add seed data

Revision ID: 296c754dec63
Revises: c530704aecd8
Create Date: 2024-11-23 17:04:50.338468

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = '296c754dec63'
down_revision: Union[str, None] = 'c530704aecd8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Create reference tables
    customers = table('customers',
        column('id', sa.Integer),
        column('domain', sa.String)
    )

    ip_lists = table('ip_lists',
        column('id', sa.Integer),
        column('ip_address', sa.BigInteger),
        column('is_blocked', sa.Boolean),
        column('domain', sa.String)
    )

    text_messages = table('text_messages',
        column('id', sa.Integer),
        column('domain', sa.String),
        column('ip_address', sa.BigInteger),
        column('message', sa.String),
        column('type', sa.String),
        column('is_malicious', sa.Boolean)
    )

    mouse_events = table('mouse_events',
        column('id', sa.Integer),
        column('domain', sa.String),
        column('ip_address', sa.BigInteger),
        column('x', sa.Integer),
        column('y', sa.Integer),
        column('viewport_x', sa.Integer),
        column('viewport_y', sa.Integer),
        column('is_malicious', sa.Boolean)
    )

    network_events = table('network_events',
        column('id', sa.Integer),
        column('domain', sa.String),
        column('ip_address', sa.BigInteger),
        column('headers', sa.JSON),
        column('method', sa.String),
        column('body', sa.JSON),
        column('cookies', sa.JSON),
        column('url', sa.String),
        column('status_code', sa.Integer),
        column('is_malicious', sa.Boolean)
    )

    # Insert seed data
    op.bulk_insert(customers,
        [
            {'domain': 'example.com'},
            {'domain': 'test.com'}
        ]
    )

    op.bulk_insert(ip_lists,
        [
            {
                'ip_address': 3232235777,  # 192.168.1.1
                'is_blocked': False,
                'domain': 'example.com'
            },
            {
                'ip_address': 3232235778,  # 192.168.1.2
                'is_blocked': True,
                'domain': 'test.com'
            }
        ]
    )

    op.bulk_insert(text_messages,
        [
            {
                'domain': 'example.com',
                'ip_address': 3232235777,
                'message': 'Hello, this is a test message',
                'type': 'user_input',
                'is_malicious': False
            }
        ]
    )

    op.bulk_insert(mouse_events,
        [
            {
                'domain': 'example.com',
                'ip_address': 3232235777,
                'x': 100,
                'y': 200,
                'viewport_x': 1920,
                'viewport_y': 1080,
                'is_malicious': False
            }
        ]
    )

    op.bulk_insert(network_events,
        [
            {
                'domain': 'example.com',
                'ip_address': 3232235777,
                'headers': {'Content-Type': 'application/json'},
                'method': 'POST',
                'body': {'key': 'value'},
                'cookies': {'session': 'abc123'},
                'url': 'https://example.com/api',
                'status_code': 200,
                'is_malicious': False
            }
        ]
    )

def downgrade():
    op.execute('DELETE FROM network_events')
    op.execute('DELETE FROM mouse_events')
    op.execute('DELETE FROM text_messages')
    op.execute('DELETE FROM ip_lists')
    op.execute('DELETE FROM customers')

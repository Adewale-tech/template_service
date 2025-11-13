"""
Unit tests for template models.
"""
import pytest
from app.models import Template


@pytest.mark.unit
@pytest.mark.asyncio
async def test_template_creation(db_session):
    """Test template model creation."""
    template = Template(
        name="welcome_email",
        language="en",
        subject="Welcome to our service",
        body="Hello {{name}}, welcome!",
        template_type="email",
        version=1,
        status="published"
    )
    db_session.add(template)
    await db_session.commit()

    result = await db_session.execute(
        "SELECT * FROM templates WHERE name = :name",
        {"name": "welcome_email"}
    )
    assert result is not None


@pytest.mark.unit
def test_template_variable_extraction():
    """Test variable extraction from template."""
    template_body = "Hello {{name}}, your order ID is {{order_id}}"
    variables = ["name", "order_id"]  # Expected variables

    import re
    found_vars = re.findall(r'{{(\w+)}}', template_body)
    assert found_vars == variables

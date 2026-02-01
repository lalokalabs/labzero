import os
import shutil
import click
from pathlib import Path


@click.command()
@click.argument("project_name")
@click.option("--directory", "-d", default=".", help="Directory to create project in")
def init(project_name, directory):
    """Initialize a new labzero project."""

    project_path = Path(directory) / project_name

    if project_path.exists():
        click.echo(f"Error: Directory {project_path} already exists!")
        return

    # Create project directory
    project_path.mkdir(parents=True)
    click.echo(f"Creating project {project_name} in {project_path}")

    # Create directory structure
    dirs_to_create = [
        "templates",
        "static",
        "static/mix/build",
        "media",
        project_name,
    ]

    for dir_name in dirs_to_create:
        (project_path / dir_name).mkdir(parents=True, exist_ok=True)

    # Create minimal settings.py
    settings_content = f'''import os
from labzero.settings import get_base_settings

# Get base settings from labzero
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_settings = get_base_settings(BASE_DIR)

# Import all base settings
globals().update(base_settings)

# Project-specific settings
ROOT_URLCONF = "{project_name}.urls"
WSGI_APPLICATION = "{project_name}.wsgi.application"

# Override any settings here if needed
# For example:
# DEBUG = True
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']
'''

    with open(project_path / project_name / "settings.py", "w") as f:
        f.write(settings_content)

    # Create minimal urls.py
    urls_content = f"""from django.urls import path, include
from labzero.urls import get_urlpatterns

# Import your views here
# from . import views

urlpatterns = [
    # Add your project-specific URLs here
    # path("", views.index, name="index"),
    
    # Include labzero default URLs
] + get_urlpatterns()
"""

    with open(project_path / project_name / "urls.py", "w") as f:
        f.write(urls_content)

    # Create minimal wsgi.py
    wsgi_content = f"""import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')

application = get_wsgi_application()
"""

    with open(project_path / project_name / "wsgi.py", "w") as f:
        f.write(wsgi_content)

    # Create __init__.py
    with open(project_path / project_name / "__init__.py", "w") as f:
        f.write("")

    # Create manage.py
    manage_content = f'''#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{project_name}.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
'''

    with open(project_path / "manage.py", "w") as f:
        f.write(manage_content)

    # Make manage.py executable
    os.chmod(project_path / "manage.py", 0o755)

    # Create pyproject.toml
    pyproject_content = f'''[project]
name = "{project_name}"
version = "0.1.0"
description = "A labzero project"
dependencies = [
    "labzero>=1.0.0",
    "django-umin>=2.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
'''

    with open(project_path / "pyproject.toml", "w") as f:
        f.write(pyproject_content)

    # Create .env.example
    env_content = """# Environment variables
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3

# Add your environment variables here
"""

    with open(project_path / ".env.example", "w") as f:
        f.write(env_content)

    # Create basic templates
    login_template_content = """{% extends "base.html" %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3>Login</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary">Login</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

    templates_dir = project_path / "templates" / "labzero"
    templates_dir.mkdir(parents=True, exist_ok=True)

    with open(templates_dir / "login.html", "w") as f:
        f.write(login_template_content)

    click.echo(f"✅ Project {project_name} created successfully!")
    click.echo(f"📁 Location: {project_path}")
    click.echo("")
    click.echo("Next steps:")
    click.echo(f"1. cd {project_name}")
    click.echo("2. cp .env.example .env")
    click.echo("3. Edit .env with your settings")
    click.echo("4. uv sync")
    click.echo("5. uv run manage.py migrate")
    click.echo("6. uv run manage.py createsuperuser")
    click.echo("7. uv run manage.py runserver")

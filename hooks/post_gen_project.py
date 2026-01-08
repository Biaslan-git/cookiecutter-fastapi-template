#!/usr/bin/env python
"""
Post-generation hook for cookiecutter template
"""
import subprocess
import sys
import os
import shutil


ALEMBIC_ENV_TEMPLATE = '''
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context


from app.db import Base
from app.models import *
from app.core import settings


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''


def run_command(cmd: list[str], description: str) -> None:
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    print("=" * 60)
    print("🚀 Initializing FastAPI project...")
    print("=" * 60)
    
    # 1. Initialize uv project
    run_command(
        ["uv", "init", "--no-readme"],
        "Initializing uv project"
    )
    
    # 2. Add main dependencies
    print("\n📥 Installing dependencies...")
    dependencies = [
        "fastapi",
        "uvicorn[standard]",
        "sqlalchemy[asyncio]",
        "aiosqlite",
        "alembic",
        "pydantic",
        "pydantic-settings",
        "pydantic[email]",
        "python-dotenv",
    ]
    
    for dep in dependencies:
        run_command(
            ["uv", "add", dep],
            f"Adding {dep}"
        )
    
    # 3. Add dev dependencies
    print("\n🛠️  Installing dev dependencies...")
    dev_dependencies = [
        "pytest",
        "pytest-asyncio",
        "httpx",
        "ruff",
    ]
    
    for dep in dev_dependencies:
        run_command(
            ["uv", "add", "--dev", dep],
            f"Adding {dep} (dev)"
        )
    
    # 4. Remove default hello.py if exists (created by uv init)
    if os.path.exists("hello.py"):
        os.remove("hello.py")
        print("🗑️  Removed default hello.py")
    
    # 5. Initialize Alembic with async template
    print("\n🔧 Initializing Alembic with async support...")
    run_command(
        ["uv", "run", "alembic", "init", "-t", "async", "alembic"],
        "Setting up Alembic (async)"
    )
    
    # 6. Replace alembic/env.py with our customized template
    print("⚙️  Replacing Alembic env.py with custom template...")
    env_path = "alembic/env.py"
    
    if os.path.exists(env_path):
        with open(env_path, "w") as f:
            f.write(ALEMBIC_ENV_TEMPLATE)
        print("✅ Replaced env.py with custom template")
    else:
        print("❌ alembic/env.py not found")
        sys.exit(1)
    
    # 9. Initialize git
    print("\n📝 Initializing git repository...")
    run_command(
        ["git", "init"],
        "Git initialization"
    )
    run_command(
        ["git", "add", "."],
        "Adding files to git"
    )
    
    print("\n" + "=" * 60)
    print("✅ Project successfully created!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Review and update .env file")
    print("2. Create first migration:")
    print("   uv run alembic revision --autogenerate -m 'Initial migration'")
    print("3. Apply migrations:")
    print("   uv run alembic upgrade head")
    print("4. Run the application:")
    print("   uv run uvicorn main:app --reload")
    print("\n📚 API documentation will be available at:")
    print("   http://localhost:8000/docs")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

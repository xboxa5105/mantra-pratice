#!/usr/bin/env python3
"""
Alembic 設定和初始化腳本
"""
import os
import sys
import subprocess
from pathlib import Path

# 添加 src 到 Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def run_command(command: list[str], description: str) -> bool:
    """執行命令並處理錯誤"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        if result.stdout:
            print(f"   輸出: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失敗")
        print(f"   錯誤: {e.stderr.strip()}")
        return False


def setup_alembic():
    """設定 Alembic"""
    print("🚀 開始設定 Alembic...")
    
    # 檢查是否已經初始化
    alembic_dir = project_root / "alembic"
    if alembic_dir.exists():
        print("⚠️  Alembic 已經初始化，跳過初始化步驟")
    else:
        # 初始化 Alembic
        if not run_command(["alembic", "init", "alembic"], "初始化 Alembic"):
            return False
    
    # 更新 alembic.ini 配置
    alembic_ini = project_root / "alembic.ini"
    if alembic_ini.exists():
        print("🔧 更新 alembic.ini 配置...")
        with open(alembic_ini, 'r') as f:
            content = f.read()
        
        # 更新資料庫 URL
        content = content.replace(
            "sqlalchemy.url = driver://user:pass@localhost/dbname",
            "sqlalchemy.url = postgresql+psycopg://user:password@localhost:5432/mydb"
        )
        
        with open(alembic_ini, 'w') as f:
            f.write(content)
        print("✅ alembic.ini 配置更新完成")
    
    return True


def update_env_py():
    """更新 alembic/env.py 以支援我們的模型"""
    env_py_path = project_root / "alembic" / "env.py"
    if not env_py_path.exists():
        print("❌ alembic/env.py 不存在")
        return False
    
    env_py_content = '''"""Alembic environment configuration"""
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 添加 src 到 path
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# 導入模型
from model.user import Base as UserBase
from model.record import Base as RecordBase

# 合併所有 Base 的 metadata
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# 將所有模型的 metadata 合併
def combine_metadata():
    """合併所有模型的 metadata"""
    from sqlalchemy import MetaData
    combined_metadata = MetaData()
    
    # 複製所有表格定義
    for table in UserBase.metadata.tables.values():
        table.tometadata(combined_metadata)
    
    for table in RecordBase.metadata.tables.values():
        table.tometadata(combined_metadata)
    
    return combined_metadata

target_metadata = combine_metadata()

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode with async engine."""
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
    
    with open(env_py_path, 'w') as f:
        f.write(env_py_content)
    
    print("✅ alembic/env.py 更新完成")
    return True


def main():
    """主函數"""
    print("=" * 50)
    print("🔧 Alembic Migration 設定工具")
    print("=" * 50)
    
    if not setup_alembic():
        sys.exit(1)
    
    if not update_env_py():
        sys.exit(1)
    
    print("\n🎉 Alembic 設定完成！")
    print("\n📝 接下來你可以使用以下命令：")
    print("   • 創建新的 migration: alembic revision --autogenerate -m 'description'")
    print("   • 執行 migration: alembic upgrade head")
    print("   • 查看 migration 歷史: alembic history")
    print("   • 回滾 migration: alembic downgrade -1")


if __name__ == "__main__":
    main()
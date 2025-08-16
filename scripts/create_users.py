#!/usr/bin/env python3
"""
自動創建測試用戶的腳本
"""
import asyncio
import sys
import uuid
from pathlib import Path

# 添加 src 到 Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from model.user import User

# 資料庫配置
DATABASE_URL = "postgresql+psycopg://user:password@localhost:5432/mydb"

# 預設用戶資料
DEFAULT_USERS = [
    {
        "username": "test_user_1",
        "user_id": "550e8400-e29b-41d4-a716-446655440001"
    },
    {
        "username": "test_user_2", 
        "user_id": "550e8400-e29b-41d4-a716-446655440002"
    }
]


async def create_database_session() -> AsyncSession:
    """創建資料庫連線"""
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,  # 顯示 SQL 查詢
        pool_pre_ping=True,
        pool_recycle=1500,
        pool_size=1,
        max_overflow=1,
    )
    
    async_session = async_sessionmaker(bind=engine)
    return async_session()


async def user_exists(session: AsyncSession, username: str) -> bool:
    """檢查用戶是否已存在"""
    from sqlalchemy import select
    
    result = await session.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none() is not None


async def create_user(session: AsyncSession, username: str, user_id: str = None) -> User:
    """創建新用戶"""
    if await user_exists(session, username):
        print(f"⚠️  用戶 '{username}' 已存在，跳過創建")
        result = await session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one()
    
    # 創建新用戶
    new_user = User(
        username=username,
        user_id=uuid.UUID(user_id) if user_id else uuid.uuid4()
    )
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    print(f"✅ 用戶 '{username}' 創建成功")
    print(f"   ID: {new_user.id}")
    print(f"   User ID: {new_user.user_id}")
    print(f"   創建時間: {new_user.created_at}")
    
    return new_user


async def create_default_users():
    """創建預設用戶"""
    print("🚀 開始創建測試用戶...")
    
    try:
        session = await create_database_session()
        
        created_users = []
        for user_data in DEFAULT_USERS:
            user = await create_user(
                session, 
                user_data["username"], 
                user_data["user_id"]
            )
            created_users.append(user)
        
        await session.close()
        
        print(f"\n🎉 完成！共創建/確認了 {len(created_users)} 個用戶")
        return created_users
        
    except Exception as e:
        print(f"❌ 創建用戶時發生錯誤: {e}")
        raise


async def create_custom_users(usernames: list[str]):
    """創建自定義用戶"""
    print(f"🚀 開始創建自定義用戶: {', '.join(usernames)}")
    
    try:
        session = await create_database_session()
        
        created_users = []
        for username in usernames:
            user = await create_user(session, username)
            created_users.append(user)
        
        await session.close()
        
        print(f"\n🎉 完成！共創建了 {len(created_users)} 個用戶")
        return created_users
        
    except Exception as e:
        print(f"❌ 創建用戶時發生錯誤: {e}")
        raise


async def list_all_users():
    """列出所有用戶"""
    print("📋 查詢所有用戶...")
    
    try:
        session = await create_database_session()
        
        from sqlalchemy import select
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        if not users:
            print("📭 沒有找到任何用戶")
        else:
            print(f"👥 找到 {len(users)} 個用戶:")
            for user in users:
                print(f"   • {user.username} (ID: {user.id}, UUID: {user.user_id})")
        
        await session.close()
        return users
        
    except Exception as e:
        print(f"❌ 查詢用戶時發生錯誤: {e}")
        raise


def print_usage():
    """顯示使用說明"""
    print("📖 使用說明:")
    print("   python scripts/create_users.py                    # 創建預設測試用戶")
    print("   python scripts/create_users.py --list             # 列出所有用戶")
    print("   python scripts/create_users.py user1 user2        # 創建自定義用戶")
    print("   python scripts/create_users.py --help             # 顯示此說明")


async def main():
    """主函數"""
    print("=" * 50)
    print("👥 用戶創建工具")
    print("=" * 50)
    
    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        print_usage()
        return
    
    if "--list" in args:
        await list_all_users()
        return
    
    if args:
        # 創建自定義用戶
        await create_custom_users(args)
    else:
        # 創建預設用戶
        await create_default_users()
    
    print("\n📋 當前所有用戶:")
    await list_all_users()


if __name__ == "__main__":
    asyncio.run(main())
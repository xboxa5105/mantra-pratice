import asyncio
import sys
import uuid
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from dependency.setting import get_settings
from model.user import User

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

settings = get_settings()
DATABASE_URL = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"

DEFAULT_USERS = [
    {"username": "test_user_1", "user_id": "550e8400-e29b-41d4-a716-446655440001"},
    {"username": "test_user_2", "user_id": "550e8400-e29b-41d4-a716-446655440002"},
]


async def create_database_session() -> AsyncSession:
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True,
        pool_recycle=1500,
        pool_size=1,
        max_overflow=1,
    )

    async_session = async_sessionmaker(bind=engine)
    return async_session()


async def user_exists(session: AsyncSession, username: str) -> bool:
    from sqlalchemy import select

    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none() is not None


async def create_user(session: AsyncSession, username: str, user_id: str = None) -> User:
    if await user_exists(session, username):
        print(f"   User '{username}' already exists, skipping creation")
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one()

    new_user = User(username=username, user_id=uuid.UUID(user_id) if user_id else uuid.uuid4())

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    print(f"   User '{username}' created successfully")
    print(f"   ID: {new_user.id}")
    print(f"   User ID: {new_user.user_id}")
    print(f"   Created at: {new_user.created_at}")

    return new_user


async def create_default_users():
    print("  Start creating test users...")

    try:
        session = await create_database_session()

        created_users = []
        for user_data in DEFAULT_USERS:
            user = await create_user(session, user_data["username"], user_data["user_id"])
            created_users.append(user)

        await session.close()

        print(f"\n🎉 Done! {len(created_users)} users created/verified")
        return created_users

    except Exception as e:
        print(f"  Error occurred while creating users: {e}")
        raise


async def create_custom_users(usernames: list[str]):
    print(f"  Start creating custom users: {', '.join(usernames)}")

    try:
        session = await create_database_session()

        created_users = []
        for username in usernames:
            user = await create_user(session, username)
            created_users.append(user)

        await session.close()

        print(f"\n  Done! {len(created_users)} users created")
        return created_users

    except Exception as e:
        print(f"  Error occurred while creating users: {e}")
        raise


async def list_all_users():
    print("  Querying all users...")

    try:
        session = await create_database_session()

        from sqlalchemy import select

        result = await session.execute(select(User))
        users = result.scalars().all()

        if not users:
            print("  No users found")
        else:
            print(f"  Found {len(users)} users:")
            for user in users:
                print(f"   • {user.username} (ID: {user.id}, UUID: {user.user_id})")

        await session.close()
        return users

    except Exception as e:
        print(f"  Error occurred while querying users: {e}")
        raise


def print_usage():
    print("  Usage:")
    print("   python scripts/create_users.py                    # Create default test users")
    print("   python scripts/create_users.py --list             # List all users")
    print("   python scripts/create_users.py user1 user2        # Create custom users")
    print("   python scripts/create_users.py --help             # Show this help message")


async def main():
    print("=" * 50)
    print("  User Creation Tool")
    print("=" * 50)

    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print_usage()
        return

    if "--list" in args:
        await list_all_users()
        return

    if args:
        await create_custom_users(args)
    else:
        await create_default_users()

    print("\n  Current users:")
    await list_all_users()


if __name__ == "__main__":
    asyncio.run(main())

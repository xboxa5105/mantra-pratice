#!/bin/bash

# Alembic Migration 便利腳本

set -e

echo "🔧 Alembic Migration 工具"
echo "=========================="

# 檢查是否在正確的目錄
if [ ! -f "pyproject.toml" ]; then
    echo "❌ 請在專案根目錄執行此腳本"
    exit 1
fi

# 函數：顯示使用說明
show_usage() {
    echo "📖 使用說明:"
    echo "   ./scripts/migrate.sh setup           # 設定 Alembic"
    echo "   ./scripts/migrate.sh create [msg]    # 創建新的 migration"
    echo "   ./scripts/migrate.sh upgrade         # 執行 migration"
    echo "   ./scripts/migrate.sh downgrade       # 回滾一個 migration"
    echo "   ./scripts/migrate.sh history         # 查看 migration 歷史"
    echo "   ./scripts/migrate.sh current         # 查看當前 migration"
    echo "   ./scripts/migrate.sh help            # 顯示此說明"
}

# 檢查參數
if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

case "$1" in
    "setup")
        echo "🚀 設定 Alembic..."
        python scripts/setup_alembic.py
        ;;
    "create")
        if [ -z "$2" ]; then
            echo "❌ 請提供 migration 描述"
            echo "   例如: ./scripts/migrate.sh create 'Add user table'"
            exit 1
        fi
        echo "📝 創建新的 migration: $2"
        alembic revision --autogenerate -m "$2"
        ;;
    "upgrade")
        echo "⬆️  執行 migration..."
        alembic upgrade head
        ;;
    "downgrade")
        echo "⬇️  回滾 migration..."
        alembic downgrade -1
        ;;
    "history")
        echo "📋 Migration 歷史:"
        alembic history
        ;;
    "current")
        echo "📍 當前 migration:"
        alembic current
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        echo "❌ 未知的命令: $1"
        show_usage
        exit 1
        ;;
esac
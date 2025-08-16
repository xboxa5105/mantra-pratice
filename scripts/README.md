# Scripts 目錄

這個目錄包含了專案的各種實用腳本。

## 📁 檔案說明

### Migration 相關
- `setup_alembic.py` - Alembic 設定和初始化腳本
- `migrate.sh` - Migration 便利腳本

### 用戶管理相關
- `create_users.py` - 自動創建測試用戶的腳本
- `users.sh` - 用戶管理便利腳本

## 🚀 快速開始

### 1. 設定 Alembic Migration

```bash
# 初始化 Alembic 配置
./scripts/migrate.sh setup

# 創建第一個 migration
./scripts/migrate.sh create "Initial migration"

# 執行 migration
./scripts/migrate.sh upgrade
```

### 2. 創建測試用戶

```bash
# 創建預設的兩個測試用戶
./scripts/users.sh create

# 創建自定義用戶
./scripts/users.sh create alice bob charlie

# 列出所有用戶
./scripts/users.sh list
```

## 📖 詳細使用說明

### Migration 腳本 (`migrate.sh`)

```bash
./scripts/migrate.sh setup           # 設定 Alembic
./scripts/migrate.sh create [msg]    # 創建新的 migration
./scripts/migrate.sh upgrade         # 執行 migration
./scripts/migrate.sh downgrade       # 回滾一個 migration
./scripts/migrate.sh history         # 查看 migration 歷史
./scripts/migrate.sh current         # 查看當前 migration
./scripts/migrate.sh help            # 顯示說明
```

### 用戶管理腳本 (`users.sh`)

```bash
./scripts/users.sh create            # 創建預設測試用戶
./scripts/users.sh create user1      # 創建指定用戶
./scripts/users.sh list              # 列出所有用戶
./scripts/users.sh help              # 顯示說明
```

## 🔧 直接使用 Python 腳本

如果你偏好直接使用 Python 腳本：

```bash
# Alembic 設定
python scripts/setup_alembic.py

# 用戶管理
python scripts/create_users.py                    # 創建預設用戶
python scripts/create_users.py --list             # 列出所有用戶
python scripts/create_users.py alice bob          # 創建自定義用戶
python scripts/create_users.py --help             # 顯示說明
```

## 📋 預設測試用戶

腳本會創建以下兩個測試用戶：

1. **test_user_1**
   - Username: `test_user_1`
   - User ID: `550e8400-e29b-41d4-a716-446655440001`

2. **test_user_2**
   - Username: `test_user_2`
   - User ID: `550e8400-e29b-41d4-a716-446655440002`

## ⚠️ 注意事項

1. **資料庫連線**: 確保資料庫服務正在運行
2. **權限**: 腳本需要執行權限 (`chmod +x scripts/*.sh`)
3. **環境**: 在專案根目錄執行腳本
4. **依賴**: 確保已安裝 `alembic` 和相關依賴

## 🛠️ 故障排除

### 常見問題

1. **權限錯誤**
   ```bash
   chmod +x scripts/*.sh scripts/*.py
   ```

2. **資料庫連線失敗**
   - 檢查 `src/dependency/db.py` 中的資料庫 URL
   - 確保資料庫服務正在運行

3. **模組導入錯誤**
   - 確保在專案根目錄執行腳本
   - 檢查 Python path 設定

4. **Alembic 配置問題**
   - 重新執行 `./scripts/migrate.sh setup`
   - 檢查 `alembic.ini` 配置

## 📝 自定義配置

如需修改資料庫連線或預設用戶，請編輯相應的 Python 腳本：

- 資料庫 URL: 修改 `scripts/create_users.py` 中的 `DATABASE_URL`
- 預設用戶: 修改 `scripts/create_users.py` 中的 `DEFAULT_USERS`
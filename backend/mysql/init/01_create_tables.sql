-- データベースの作成（存在しない場合）
CREATE DATABASE IF NOT EXISTS lambdadb
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- データベースの選択
USE lambdadb;

-- デバイステーブルの作成
CREATE TABLE IF NOT EXISTS devices (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL COMMENT '機器名',
    manufacturer VARCHAR(255) NOT NULL COMMENT 'メーカー名',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_devices_name (name),
    INDEX idx_devices_manufacturer (manufacturer)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='機器管理用のテーブル'; 
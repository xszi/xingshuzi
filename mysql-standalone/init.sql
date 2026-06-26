-- 设置字符集
SET NAMES utf8mb4;

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS xingshuzi DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE xingshuzi;

-- 用户表
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `role` varchar(20) DEFAULT 'user',
  `status` varchar(20) DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 书籍表
CREATE TABLE IF NOT EXISTS `book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `author` varchar(100) DEFAULT NULL,
  `cover` varchar(500) DEFAULT NULL,
  `description` text,
  `price` decimal(10,2) DEFAULT NULL,
  `stock` int DEFAULT '0',
  `status` varchar(20) DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 课程表
CREATE TABLE IF NOT EXISTS `course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `teacher` varchar(100) DEFAULT NULL,
  `cover` varchar(500) DEFAULT NULL,
  `description` text,
  `price` decimal(10,2) DEFAULT NULL,
  `duration` int DEFAULT NULL COMMENT '课程时长(分钟)',
  `status` varchar(20) DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 音乐表
CREATE TABLE IF NOT EXISTS `music` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `artist` varchar(100) DEFAULT NULL,
  `cover` varchar(500) DEFAULT NULL,
  `audio_url` varchar(500) DEFAULT NULL,
  `duration` int DEFAULT NULL COMMENT '音乐时长(秒)',
  `status` varchar(20) DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 商品表
CREATE TABLE IF NOT EXISTS `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `cover` varchar(500) DEFAULT NULL,
  `description` text,
  `price` decimal(10,2) DEFAULT NULL,
  `stock` int DEFAULT '0',
  `category` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 轮播图表
CREATE TABLE IF NOT EXISTS `banner` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `image` varchar(500) NOT NULL,
  `link` varchar(500) DEFAULT NULL,
  `sort` int DEFAULT '0',
  `status` varchar(20) DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 小红书发布内容表（按日期 + 同学 + 时段）
CREATE TABLE IF NOT EXISTS `xhs_posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `post_date` date NOT NULL COMMENT '发布日期',
  `student` varchar(10) NOT NULL DEFAULT 'a' COMMENT '同学: a/b/c',
  `period` varchar(20) NOT NULL COMMENT '时段: morning/noon/evening/night',
  `title` varchar(200) DEFAULT NULL COMMENT '标题',
  `images` text COMMENT '配图(JSON数组)',
  `content` text COMMENT '文案',
  `product` text COMMENT '所挂商品(JSON数组，多选)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_date_student_period` (`post_date`, `student`, `period`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 兼容升级：若 xhs_posts 表已存在但缺少 student 字段 / 旧唯一键，则补齐
-- （CREATE TABLE IF NOT EXISTS 不会修改已存在的表，故用存储过程做幂等迁移）
DROP PROCEDURE IF EXISTS `migrate_xhs_posts_student`;
DELIMITER //
CREATE PROCEDURE `migrate_xhs_posts_student`()
BEGIN
  -- 1. 新增 student 列（不存在时）
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'xhs_posts'
      AND COLUMN_NAME = 'student'
  ) THEN
    ALTER TABLE `xhs_posts`
      ADD COLUMN `student` varchar(10) NOT NULL DEFAULT 'a' COMMENT '同学: a/b/c' AFTER `post_date`;
  END IF;

  -- 2. 删除旧唯一键 uq_date_period（存在时）
  IF EXISTS (
    SELECT 1 FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'xhs_posts'
      AND INDEX_NAME = 'uq_date_period'
  ) THEN
    ALTER TABLE `xhs_posts` DROP INDEX `uq_date_period`;
  END IF;

  -- 3. 新增唯一键 uq_date_student_period（不存在时）
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'xhs_posts'
      AND INDEX_NAME = 'uq_date_student_period'
  ) THEN
    ALTER TABLE `xhs_posts`
      ADD UNIQUE KEY `uq_date_student_period` (`post_date`, `student`, `period`);
  END IF;

  -- 4. 将 product 列从 varchar 扩为 text（多选 JSON 数组），仅当当前不是 text 时
  IF EXISTS (
    SELECT 1 FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'xhs_posts'
      AND COLUMN_NAME = 'product'
      AND DATA_TYPE <> 'text'
  ) THEN
    ALTER TABLE `xhs_posts`
      MODIFY COLUMN `product` text COMMENT '所挂商品(JSON数组，多选)';
  END IF;
END //
DELIMITER ;
CALL `migrate_xhs_posts_student`();
DROP PROCEDURE IF EXISTS `migrate_xhs_posts_student`;

-- 提示：管理员账号需要运行 init_admin.py 来创建


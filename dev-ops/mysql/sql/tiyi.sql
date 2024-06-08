/*
 Navicat Premium Data Transfer

 Source Server         : docker-compose
 Source Server Type    : MySQL
 Source Server Version : 80032
 Source Host           : 127.0.0.1:3306
 Source Schema         : tiyi

 Target Server Type    : MySQL
 Target Server Version : 80032
 File Encoding         : 65001

 Date: 08/06/2024 12:48:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP DATABASE IF EXISTS `tiyi`;
CREATE DATABASE `tiyi` default character set utf8mb4;
USE `tiyi`;

-- ----------------------------
-- Table structure for analysis_item
-- ----------------------------
DROP TABLE IF EXISTS `analysis_item`;
CREATE TABLE `analysis_item`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '音频分析项名称，如BPM、频谱等',
  `price` int NOT NULL DEFAULT 0 COMMENT '消耗音乐币数量',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `analysis_item_pk`(`name` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '音频分析项目' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of analysis_item
-- ----------------------------

-- ----------------------------
-- Table structure for audio
-- ----------------------------
DROP TABLE IF EXISTS `audio`;
CREATE TABLE `audio`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `audio_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '音频唯一id',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '音频原始名称',
  `extension` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '音频文件格式扩展名',
  `local_path` varchar(1023) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '音频文件的服务器本地存储路径',
  `url` varchar(1023) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '音频文件远程访问地址',
  `tags` varchar(1023) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '音频标签，如\"流行,乡村,摇滚,轻松\"',
  `cover` varchar(1023) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '音频封面url',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '上传的用户名',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `audio_pk`(`audio_id` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '音频表，保存用户上传的音频信息' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of audio
-- ----------------------------
INSERT INTO `audio` VALUES (1, '6608d3dab7714aea92fafe668e0b2ff4', 'Cheng Peng - 卡农 (铃声) - 副本', 'flac', 'D:\\Projects\\PyProjects\\tiyi-back\\files\\audios\\6608d3dab7714aea92fafe668e0b2ff4.flac', '\'\'', '流行,轻松,治愈', NULL, 'maskira', '2024-06-08 11:28:26', '2024-06-08 11:30:13');

-- ----------------------------
-- Table structure for audio_tags
-- ----------------------------
DROP TABLE IF EXISTS `audio_tags`;
CREATE TABLE `audio_tags`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '定义标签的用户名',
  `tags` varchar(1023) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '' COMMENT '用户定义的标签，如\"流行,乡村,轻松,治愈\"',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户自定义标签表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of audio_tags
-- ----------------------------
INSERT INTO `audio_tags` VALUES (1, 'maskira', '治愈', '2024-06-08 10:28:49', '2024-06-08 10:57:26');
INSERT INTO `audio_tags` VALUES (2, 'maska', '轻松', '2024-06-08 10:30:49', '2024-06-08 10:30:49');

-- ----------------------------
-- Table structure for order
-- ----------------------------
DROP TABLE IF EXISTS `order`;
CREATE TABLE `order`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
  `out_trade_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '订单号',
  `recharge_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '充值项标题',
  `amount` int NOT NULL COMMENT '音乐币数量',
  `price` double NOT NULL COMMENT '订单金额',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '订单表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of order
-- ----------------------------

-- ----------------------------
-- Table structure for pay_flow
-- ----------------------------
DROP TABLE IF EXISTS `pay_flow`;
CREATE TABLE `pay_flow`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `trade_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '交易凭证',
  `subject` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '交易名称',
  `trade_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '交易状态',
  `out_trade_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '商户订单号',
  `total_amount` double NOT NULL COMMENT '交易金额',
  `buyer_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '支付用户id',
  `gmt_payment` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '付款时间',
  `buyer_pay_amount` double NOT NULL COMMENT '付款金额',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '支付流水表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of pay_flow
-- ----------------------------

-- ----------------------------
-- Table structure for recharge_item
-- ----------------------------
DROP TABLE IF EXISTS `recharge_item`;
CREATE TABLE `recharge_item`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '充值项标题，如“1元100个音乐币，10元2000个音乐币”等',
  `amount` int NOT NULL COMMENT '音乐币数量',
  `price` double NOT NULL COMMENT '价格',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '充值项目表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of recharge_item
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名，唯一',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户密码，加密存储',
  `music_coin` int NULL DEFAULT 100 COMMENT '音乐币，新用户免费赠送100个',
  `avatar` varchar(1023) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户头像',
  `signature` varchar(1023) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '在签名中展现你的个性吧！' COMMENT '个性签名',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_pk`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'maskira', '$2b$12$H3aUAJ5N/qeGvzGjr1/xH.lDSnKanpTMqW8/1xdcniBu9.nCZTIKS', 100, NULL, '在签名中展现你的个性吧！', '2024-06-08 10:40:31', '2024-06-08 10:40:31');

SET FOREIGN_KEY_CHECKS = 1;

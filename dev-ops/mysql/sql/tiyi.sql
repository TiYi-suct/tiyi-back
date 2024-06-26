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

 Date: 10/06/2024 17:15:08
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
  `description` varchar(1023) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '音频分析项描述',
  `price` int NOT NULL DEFAULT 0 COMMENT '消耗音乐币数量',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `analysis_item_pk`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '音频分析项目' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of analysis_item
-- ----------------------------
INSERT INTO `analysis_item` VALUES (1, 'BPM', 'Beat Per Minute 是衡量音乐速度的标准单位。BPM 值越高，音乐的节奏越快，反之则越慢。它广泛应用于各种音乐类型和音乐制作软件中，以帮助音乐家和制作人控制和调整音乐的速度。', 0, '2024-06-08 14:43:56', '2024-06-08 14:43:56');
INSERT INTO `analysis_item` VALUES (2, '移调', '将一段音乐整体上升或下降几个音调，以便于演奏或演唱。移调通常用于乐器演奏者或歌手的方便，使他们能够演奏或演唱更舒适的音域。移调还可以改变音乐的情感表达和风格。', 5, '2024-06-08 14:44:22', '2024-06-08 14:44:22');
INSERT INTO `analysis_item` VALUES (3, '梅尔频谱图', '梅尔频谱图是一种音频信号的时频表示方法，其中频率轴经过梅尔标度变换，以反映人耳的听觉感知。它通过将频率轴划分为非线性间隔，更符合人类的听觉特性。梅尔频谱图在语音识别和音乐信号处理等领域中有着广泛的应用。', 3, '2024-06-08 22:37:08', '2024-06-08 22:37:08');
INSERT INTO `analysis_item` VALUES (4, '频谱图', '频谱图显示音频信号强度（功率）随频率和时间变化的图像。它通过将音频信号分解为不同频率成分并显示其随时间变化的强度来提供音频信号的详细分析。频谱图广泛应用于音频分析、音乐制作、声学研究等领域。', 5, '2024-06-09 17:55:16', '2024-06-09 17:55:16');
INSERT INTO `analysis_item` VALUES (5, 'MFCC', 'Mel-Frequency Cepstral Coefficients（梅尔频率倒谱系数）表示音频信号的短期功率谱包络。它通过模拟人耳对声音的感知来分析音频信号的特征。MFCC 是语音识别、音乐分类和音频分析中的重要特征参数，广泛应用于各种音频处理任务中。', 10, '2024-06-10 10:50:43', '2024-06-10 10:50:43');

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
  `description` varchar(1023) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '音频描述',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '上传的用户名',
  `confirmed` tinyint(1) NOT NULL DEFAULT 0 COMMENT '保留字段，用户是否确定保存这条音频记录',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `audio_pk`(`audio_id` ASC) USING BTREE,
  INDEX `idx_username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '音频表，保存用户上传的音频信息' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of audio
-- ----------------------------
INSERT INTO `audio` VALUES (1, '10e0e16c66d74b5d802db3c30aa41730', 'sample-15s', 'wav', './files/10e0e16c66d74b5d802db3c30aa41730.wav', 'http://tiyi.api.maskira.top/file/10e0e16c66d74b5d802db3c30aa41730.wav', '流行,轻松', NULL, NULL, 'mask', 0, '2024-06-10 16:42:03', '2024-06-10 16:42:03');
INSERT INTO `audio` VALUES (2, 'a94613d074ce41e487d0897a2f23918d', '卡农', 'flac', './files/a94613d074ce41e487d0897a2f23918d.flac', 'http://tiyi.api.maskira.top/file/a94613d074ce41e487d0897a2f23918d.flac', NULL, NULL, NULL, 'maskira', 0, '2024-06-10 16:42:03', '2024-06-10 16:42:03');
INSERT INTO `audio` VALUES (3, '58368ded826e4a0490bda7030a230200', '朴树-平凡之路', 'flac', './files/58368ded826e4a0490bda7030a230200.flac', 'http://tiyi.api.maskira.top/file/58368ded826e4a0490bda7030a230200.flac', NULL, NULL, NULL, 'mask', 0, '2024-06-10 16:56:14', '2024-06-10 16:56:14');
INSERT INTO `audio` VALUES (4, '2ef625823646459791f10f53c7218ed6', '陈慧琳-阁楼', 'mp3', './files/2ef625823646459791f10f53c7218ed6.mp3', 'http://tiyi.api.maskira.top/file/2ef625823646459791f10f53c7218ed6.mp3', NULL, NULL, NULL, 'maskira', 0, '2024-06-10 16:56:14', '2024-06-10 16:56:14');
INSERT INTO `audio` VALUES (5, '1d97e4eb015449319df0b7240ca08d46', '周杰伦-稻香', 'mp3', './files/1d97e4eb015449319df0b7240ca08d46.mp3', 'http://tiyi.api.maskira.top/file/1d97e4eb015449319df0b7240ca08d46.mp3', '流行,治愈', NULL, NULL, 'maskira', 0, '2024-06-10 16:56:14', '2024-06-10 16:56:14');
INSERT INTO `audio` VALUES (6, '10e0e16c66d74b5d802db3c30aa41731', 'sample-1s', 'wav', './files/10e0e16c66d74b5d802db3c30aa41731.wav', 'http://tiyi.api.maskira.top/file/10e0e16c66d74b5d802db3c30aa41731.wav', '流行,轻松', NULL, NULL, 'maskira', 0, '2024-06-10 16:42:03', '2024-06-10 16:42:03');
INSERT INTO `audio` VALUES (7, '10e0e16c66d74b5d802db3c30aa41732', 'sample-2s', 'wav', './files/10e0e16c66d74b5d802db3c30aa41732.wav', 'http://tiyi.api.maskira.top/file/10e0e16c66d74b5d802db3c30aa41732.wav', '流行,轻松', NULL, NULL, 'maskira', 0, '2024-06-10 16:42:04', '2024-06-10 16:42:04');
INSERT INTO `audio` VALUES (8, '10e0e16c66d74b5d802db3c30aa41733', 'sample-3s', 'wav', './files/10e0e16c66d74b5d802db3c30aa41733.wav', 'http://tiyi.api.maskira.top/file/10e0e16c66d74b5d802db3c30aa41733.wav', '流行,轻松', NULL, NULL, 'maskira', 0, '2024-06-10 16:42:05', '2024-06-10 16:42:05');
INSERT INTO `audio` VALUES (9, '10e0e16c66d74b5d802db3c30aa41734', 'sample-4s', 'wav', './files/10e0e16c66d74b5d802db3c30aa41734.wav', 'http://tiyi.api.maskira.top/file/10e0e16c66d74b5d802db3c30aa41734.wav', '流行,轻松', NULL, NULL, 'maskira', 0, '2024-06-10 16:42:06', '2024-06-10 16:42:06');
INSERT INTO `audio` VALUES (10, '10e0e16c66d74b5d802db3c30aa41735', 'sample-5s', 'wav', './files/10e0e16c66d74b5d802db3c30aa41735.wav', 'http://tiyi.api.maskira.top/file/10e0e16c66d74b5d802db3c30aa41735.wav', '流行,轻松', NULL, NULL, 'maskira', 0, '2024-06-10 16:42:07', '2024-06-10 16:42:07');
INSERT INTO `audio` VALUES (11, '10e0e16c66d74b5d802db3c30aa41736', 'sample-6s', 'wav', './files/10e0e16c66d74b5d802db3c30aa41736.wav', 'http://tiyi.api.maskira.top/file/10e0e16c66d74b5d802db3c30aa41736.wav', '流行,轻松', NULL, NULL, 'maskira', 0, '2024-06-10 16:42:08', '2024-06-10 16:42:08');
INSERT INTO `audio` VALUES (12, '10e0e16c66d74b5d802db3c30aa41737', 'sample-7s', 'wav', './files/10e0e16c66d74b5d802db3c30aa41737.wav', 'http://tiyi.api.maskira.top/file/10e0e16c66d74b5d802db3c30aa41737.wav', '流行,轻松', NULL, NULL, 'maskira', 0, '2024-06-10 16:42:09', '2024-06-10 16:42:09');
INSERT INTO `audio` VALUES (13, '10e0e16c66d74b5d802db3c30aa41738', 'sample-8s', 'wav', './files/10e0e16c66d74b5d802db3c30aa41738.wav', 'http://tiyi.api.maskira.top/file/10e0e16c66d74b5d802db3c30aa41738.wav', '流行,轻松', NULL, NULL, 'maskira', 0, '2024-06-10 16:42:10', '2024-06-10 16:42:10');
INSERT INTO `audio` VALUES (14, '10e0e16c66d74b5d802db3c30aa41739', 'sample-9s', 'wav', './files/10e0e16c66d74b5d802db3c30aa41739.wav', 'http://tiyi.api.maskira.top/file/10e0e16c66d74b5d802db3c30aa41739.wav', '流行,轻松', NULL, NULL, 'maskira', 0, '2024-06-10 16:42:11', '2024-06-10 16:42:11');


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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户自定义标签表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of audio_tags
-- ----------------------------
INSERT INTO `audio_tags` VALUES (1, 'maskira', '治愈,流行,乡村,摇滚', '2024-06-08 10:28:49', '2024-06-08 10:57:26');
INSERT INTO `audio_tags` VALUES (3, 'mask', '治愈,轻松,摇滚,慢摇,流行', '2024-06-10 16:42:03', '2024-06-10 16:42:03');

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
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '订单表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of order
-- ----------------------------
INSERT INTO `order` VALUES (7, 'maskira', 'ORDER_20240608181722_7476135a58a', '5元1000个音乐币', 1000, 5, '2024-06-08 18:17:22', '2024-06-08 18:17:22');
INSERT INTO `order` VALUES (8, 'maskira', 'ORDER_20240608181755_878d4de70fc', '5元1000个音乐币', 1000, 5, '2024-06-08 18:17:55', '2024-06-08 18:17:55');
INSERT INTO `order` VALUES (9, 'maskira', 'ORDER_20240608181824_028eb05bc1e', '5元1000个音乐币', 1000, 5, '2024-06-08 18:18:24', '2024-06-08 18:18:24');
INSERT INTO `order` VALUES (10, 'mask', 'ORDER_20240608181947_3c1404256bb', '5元1000个音乐币', 1000, 5, '2024-06-08 18:19:48', '2024-06-08 18:19:48');

-- ----------------------------
-- Table structure for pay_flow
-- ----------------------------
DROP TABLE IF EXISTS `pay_flow`;
CREATE TABLE `pay_flow`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
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
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '支付流水表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of pay_flow
-- ----------------------------
INSERT INTO `pay_flow` VALUES (2, 'maskira', '2024060822001415260503344436', '5元1000个音乐币', 'TRADE_SUCCESS', 'ORDER_20240608181722_7476135a58a', 5, '2088722037015261', '2024-06-08 18:17:30', 5, '2024-06-08 18:15:16', '2024-06-08 18:15:16');
INSERT INTO `pay_flow` VALUES (3, 'maskira', '2024060822001415260503340517', '5元1000个音乐币', 'TRADE_SUCCESS', 'ORDER_20240608181755_878d4de70fc', 5, '2088722037015261', '2024-06-08 18:18:03', 5, '2024-06-08 18:15:16', '2024-06-08 18:15:16');
INSERT INTO `pay_flow` VALUES (4, 'maskira', '2024060822001415260503336313', '5元1000个音乐币', 'TRADE_SUCCESS', 'ORDER_20240608181824_028eb05bc1e', 5, '2088722037015261', '2024-06-08 18:18:32', 5, '2024-06-08 18:15:16', '2024-06-08 18:15:16');
INSERT INTO `pay_flow` VALUES (5, 'mask', '2024060822001415260503343243', '5元1000个音乐币', 'TRADE_SUCCESS', 'ORDER_20240608181947_3c1404256bb', 5, '2088722037015261', '2024-06-08 18:20:01', 5, '2024-06-08 18:15:16', '2024-06-08 18:15:16');

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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '充值项目表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of recharge_item
-- ----------------------------
INSERT INTO `recharge_item` VALUES (1, '1元100个音乐币', 100, 1, '2024-06-08 14:45:16', '2024-06-08 14:45:16');
INSERT INTO `recharge_item` VALUES (2, '5元1000个音乐币', 1000, 5, '2024-06-08 14:45:44', '2024-06-08 14:45:44');
INSERT INTO `recharge_item` VALUES (3, '10元5000个音乐币', 5000, 10, '2024-06-08 14:46:08', '2024-06-08 14:46:08');
INSERT INTO `recharge_item` VALUES (4, '15元10000个音乐币', 10000, 15, '2024-06-08 14:46:45', '2024-06-08 14:46:45');

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
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'maskira', '$2b$12$H3aUAJ5N/qeGvzGjr1/xH.lDSnKanpTMqW8/1xdcniBu9.nCZTIKS', 3100, NULL, '在签名中展现你的个性吧！', '2024-06-08 10:40:31', '2024-06-10 11:33:32');
INSERT INTO `user` VALUES (2, 'mask', '$2b$12$VE40Aw6wWNhCL.npBwkwguKD4omebPO10mtL1sHPzhkVOOrmR1iq6', 1100, NULL, '在签名中展现你的个性吧！', '2024-06-08 18:15:16', '2024-06-10 16:56:14');

SET FOREIGN_KEY_CHECKS = 1;

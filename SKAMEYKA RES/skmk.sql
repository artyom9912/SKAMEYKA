-- --------------------------------------------------------
-- Хост:                         127.0.0.1
-- Версия сервера:               8.0.16 - MySQL Community Server - GPL
-- Операционная система:         Win64
-- HeidiSQL Версия:              11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Дамп структуры базы данных skameyka
CREATE DATABASE IF NOT EXISTS `skameyka` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `skameyka`;

-- Дамп структуры для таблица skameyka.main_table
CREATE TABLE IF NOT EXISTS `main_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `TimeStamp` datetime NOT NULL,
  `UserId` int(11) NOT NULL,
  `ProjectId` int(11) NOT NULL,
  `HoursSpent` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `UserId_idx` (`UserId`),
  KEY `ProjectId_idx` (`ProjectId`),
  CONSTRAINT `ProjectId` FOREIGN KEY (`ProjectId`) REFERENCES `project_table` (`id`),
  CONSTRAINT `UserId` FOREIGN KEY (`UserId`) REFERENCES `user_table` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Таблица ежедневной отчетности';

-- Дамп данных таблицы skameyka.main_table: ~7 rows (приблизительно)
/*!40000 ALTER TABLE `main_table` DISABLE KEYS */;
INSERT INTO `main_table` (`id`, `TimeStamp`, `UserId`, `ProjectId`, `HoursSpent`) VALUES
	(1, '2020-03-06 16:20:00', 1, 2, 12),
	(2, '2020-03-06 16:20:00', 1, 1, 10),
	(3, '2019-04-22 00:00:00', 1, 1, 10),
	(4, '2019-04-23 00:00:00', 1, 1, 8),
	(5, '2019-04-24 00:00:00', 1, 1, 4),
	(6, '2019-04-25 00:00:00', 1, 1, 5),
	(7, '2019-04-26 00:00:00', 1, 1, 8);
/*!40000 ALTER TABLE `main_table` ENABLE KEYS */;

-- Дамп структуры для таблица skameyka.project_table
CREATE TABLE IF NOT EXISTS `project_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ProjectName` varchar(64) DEFAULT NULL,
  `ProjectCode` varchar(16) NOT NULL,
  `ProjectCustomer` varchar(45) DEFAULT NULL,
  `IsRelevant` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Таблица-перечень проектов и заказчиков';

-- Дамп данных таблицы skameyka.project_table: ~0 rows (приблизительно)
/*!40000 ALTER TABLE `project_table` DISABLE KEYS */;
INSERT INTO `project_table` (`id`, `ProjectName`, `ProjectCode`, `ProjectCustomer`, `IsRelevant`) VALUES
	(1, 'fgh', '2019-08-28', 'avv', 1),
	(2, 'asdas', '2020-03-06', '123', 1);
/*!40000 ALTER TABLE `project_table` ENABLE KEYS */;

-- Дамп структуры для таблица skameyka.user_table
CREATE TABLE IF NOT EXISTS `user_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `UserName` varchar(45) NOT NULL,
  `IsRelevant` tinyint(4) DEFAULT NULL,
  `isAdmin` tinyint(4) DEFAULT NULL,
  `Password` varchar(50) DEFAULT NULL,
  `Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='База сотрудников организации';

-- Дамп данных таблицы skameyka.user_table: ~2 rows (приблизительно)
/*!40000 ALTER TABLE `user_table` DISABLE KEYS */;
INSERT INTO `user_table` (`id`, `UserName`, `IsRelevant`, `isAdmin`, `Password`, `Name`) VALUES
	(1, 'artem', 1, 1, '123', 'Тюбаев Артём'),
	(2, 'Катя Ворожба', 1, NULL, NULL, NULL);
/*!40000 ALTER TABLE `user_table` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

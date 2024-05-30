-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.3.0 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para skameyka
CREATE DATABASE IF NOT EXISTS `skameyka` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `skameyka`;

-- Volcando estructura para tabla skameyka.main_table
CREATE TABLE IF NOT EXISTS `main_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `user_id` int NOT NULL,
  `project_id` int NOT NULL,
  `hours` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `UserId_idx` (`user_id`),
  KEY `ProjectId_idx` (`project_id`),
  CONSTRAINT `project_id` FOREIGN KEY (`project_id`) REFERENCES `project_table` (`id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user_table` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Таблица ежедневной отчетности';

-- Volcando datos para la tabla skameyka.main_table: ~27 rows (aproximadamente)
INSERT INTO `main_table` (`id`, `timestamp`, `user_id`, `project_id`, `hours`) VALUES
	(1, '2023-05-30 15:23:10', 1, 1, 4),
	(2, '2023-05-30 15:23:10', 1, 2, 4),
	(3, '2023-05-20 15:23:10', 1, 2, 2),
	(4, '2023-08-02 00:00:00', 3, 1, 6),
	(5, '2023-08-03 00:00:00', 3, 1, 5),
	(6, '2023-08-03 00:00:00', 2, 1, 6),
	(7, '2023-08-04 00:00:00', 2, 1, 2),
	(8, '2023-09-05 00:00:00', 3, 1, 4),
	(9, '2023-09-05 00:00:00', 3, 1, 6),
	(10, '2023-08-02 00:00:00', 1, 2, 5),
	(11, '2023-08-03 00:00:00', 3, 2, 2),
	(12, '2023-08-03 00:00:00', 2, 2, 1),
	(13, '2023-08-04 00:00:00', 2, 2, 2),
	(14, '2023-09-05 00:00:00', 3, 2, 1),
	(15, '2023-09-05 00:00:00', 3, 2, 2),
	(16, '2023-08-12 00:00:00', 3, 3, 6),
	(17, '2023-08-13 00:00:00', 3, 3, 5),
	(18, '2023-08-13 00:00:00', 2, 3, 6),
	(19, '2023-08-14 00:00:00', 2, 3, 2),
	(20, '2023-09-15 00:00:00', 3, 3, 4),
	(21, '2023-09-15 00:00:00', 3, 3, 6),
	(22, '2022-11-02 00:00:00', 1, 4, 4),
	(23, '2022-11-03 00:00:00', 3, 4, 1),
	(24, '2022-11-03 00:00:00', 2, 4, 1),
	(25, '2022-11-04 00:00:00', 2, 4, 1),
	(26, '2022-11-05 00:00:00', 3, 4, 1),
	(27, '2022-11-05 00:00:00', 3, 4, 5);

-- Volcando estructura para tabla skameyka.project_table
CREATE TABLE IF NOT EXISTS `project_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(64) DEFAULT NULL,
  `stage` varchar(16) DEFAULT NULL,
  `code` varchar(16) NOT NULL,
  `customer` varchar(45) DEFAULT NULL,
  `relevant` tinyint DEFAULT NULL,
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Таблица-перечень проектов и заказчиков';

-- Volcando datos para la tabla skameyka.project_table: ~4 rows (aproximadamente)
INSERT INTO `project_table` (`id`, `title`, `stage`, `code`, `customer`, `relevant`) VALUES
	(1, 'ЖК Аквамарин', 'ЭП', '2023_10', 'Борисов В.', 1),
	(2, 'Вилла Тайланд', 'ПД', '2023_12', 'Васильев А.', 1),
	(3, 'ЖК Пасифик', 'ПД', '2022_06', 'Эйлер А.', 1),
	(4, 'ДОМ Линейка', 'ЭП', '2022_05', 'Линейка С.', 0);

-- Volcando estructura para tabla skameyka.user_table
CREATE TABLE IF NOT EXISTS `user_table` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `relevant` tinyint DEFAULT NULL,
  `admin` tinyint DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `fullname` varchar(45) DEFAULT NULL,
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='База сотрудников организации';

-- Volcando datos para la tabla skameyka.user_table: ~3 rows (aproximadamente)
INSERT INTO `user_table` (`id`, `username`, `relevant`, `admin`, `password`, `fullname`) VALUES
	(1, 'artem', 1, 1, '123', 'Артём Тюбаев'),
	(2, 'evgen', 1, 1, '123', 'Бурлака Евгений'),
	(3, 'olga123', 1, 0, '123', 'Ольга Переделкина');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

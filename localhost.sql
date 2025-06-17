CREATE DATABASE IF NOT EXISTS `iot` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `iot`;

CREATE TABLE `users` (
  `id` int(5) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(30) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `sensors24` (
  `id` int(11) NOT NULL,
  `device` varchar(10) NOT NULL,
  `temperature` float DEFAULT NULL,
  `humidity` float DEFAULT NULL,
  `rain_status` int(2) DEFAULT NULL,
  `time` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `sensors24` (`id`, `device`, `temperature`, `humidity`, `rain_status`, `time`) VALUES
(1, 'A0131', 19.4, NULL, 1, 'Fri Jan  5 17:47:58 2024'),
(2, 'A0131', 21.3, NULL, 1, 'Fri Jan  5 17:53:07 2024'),
(3, 'A0131', 21, NULL, 1, 'Fri Jan  5 17:58:11 2024');

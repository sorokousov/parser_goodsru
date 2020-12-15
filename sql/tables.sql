CREATE TABLE `brands` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sku` bigint DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `links_and_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `categories` varchar(255) DEFAULT NULL,
  `links` varchar(500) DEFAULT NULL,
  `status` int DEFAULT '0',
  `date_start` datetime DEFAULT NULL,
  `date_end` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sku` bigint DEFAULT NULL,
  `price` double(9,2) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `id_brand` int DEFAULT NULL,
  `id_category` int DEFAULT NULL,
  `status` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `date_in` datetime DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `plus_comment` text,
  `minus_comment` text,
  `comment` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `specifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sku` bigint DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- food_advisor.DietChart definition

CREATE TABLE `DietChart` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `BMI` int NOT NULL,
  `Day` int NOT NULL,
  `Time` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `order` int NOT NULL,
  `DietFood` text NOT NULL,
  `IsActive` bit(1) NOT NULL DEFAULT b'1',
  `LastModified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- food_advisor.DietPlan definition

CREATE TABLE `DietPlan` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `UserAccess_ID` int NOT NULL,
  `UserDetails_ID` int NOT NULL,
  `DayNumber` int NOT NULL,
  `DietDate` datetime NOT NULL,
  `DietTime` varchar(45) NOT NULL,
  `DietOrder` int NOT NULL,
  `DietFood` text NOT NULL,
  `IsActive` bit(1) NOT NULL DEFAULT b'1',
  `LastModified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `FK_DietPlan_UserAccess_ID_idx` (`UserAccess_ID`),
  KEY `FK_DietPlan_UserDetails_ID_idx` (`UserDetails_ID`),
  CONSTRAINT `FK_DietPlan_UserAccess_ID` FOREIGN KEY (`UserAccess_ID`) REFERENCES `UserAccess` (`UserAccess_ID`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `FK_DietPlan_UserDetails_ID` FOREIGN KEY (`UserDetails_ID`) REFERENCES `UserDetails` (`ID`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- food_advisor.RevokeSession definition

CREATE TABLE `RevokeSession` (
  `ID` bigint NOT NULL AUTO_INCREMENT,
  `Session_ID` varchar(255) NOT NULL,
  `Type` varchar(45) NOT NULL,
  `Token` text,
  `RevokedOn` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `FK_RevokeSession_Session_ID_idx` (`Session_ID`),
  CONSTRAINT `FK_RevokeSession_Session_ID` FOREIGN KEY (`Session_ID`) REFERENCES `UserSession` (`Session_ID`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- food_advisor.UserAccess definition

CREATE TABLE `UserAccess` (
  `UserAccess_ID` int NOT NULL AUTO_INCREMENT,
  `FullName` varchar(255) NOT NULL,
  `Email_ID` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `IsActive` varchar(1) NOT NULL DEFAULT 'N',
  `LastModifiedBy` varchar(255) NOT NULL DEFAULT 'SYSTEM',
  `LastModifiedDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`UserAccess_ID`),
  KEY `UserAccess_Email_ID_IDX` (`Email_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- food_advisor.UserDetails definition

CREATE TABLE `UserDetails` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `UserAccess_ID` int NOT NULL,
  `Age` int NOT NULL,
  `Gender` varchar(45) NOT NULL,
  `Height` int NOT NULL,
  `Weight` int NOT NULL,
  `MedicalCondition` text,
  `DailyActivity` text,
  `TargetDays` int DEFAULT NULL,
  `TargetBMI` int DEFAULT NULL,
  `BMI` decimal(3,1) NOT NULL,
  `DietStarts` datetime DEFAULT NULL,
  `DietEnds` datetime DEFAULT NULL,
  `IsActive` bit(1) NOT NULL DEFAULT b'1',
  `LastModified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `FK_UserDetails_UserAccess_ID_idx` (`UserAccess_ID`),
  CONSTRAINT `FK_UserDetails_UserAccess_ID` FOREIGN KEY (`UserAccess_ID`) REFERENCES `UserAccess` (`UserAccess_ID`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- food_advisor.UserSession definition

CREATE TABLE `UserSession` (
  `Session_ID` varchar(255) NOT NULL,
  `UserAccess_ID` int NOT NULL,
  `AccessToken` text,
  `RefreshToken` text,
  `SessionBegin` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `SessionEnd` datetime DEFAULT NULL,
  `IsActive` bit(1) NOT NULL DEFAULT b'1',
  `IsLogOut` bit(1) NOT NULL DEFAULT b'0',
  `CreatedOn` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `LastModified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Session_ID`),
  KEY `FK_UserSession_UserAccess_ID_idx` (`UserAccess_ID`),
  CONSTRAINT `FK_UserSession_UserAccess_ID` FOREIGN KEY (`UserAccess_ID`) REFERENCES `UserAccess` (`UserAccess_ID`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



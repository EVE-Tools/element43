-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 18, 2012 at 06:31 PM
-- Server version: 5.5.24
-- PHP Version: 5.3.10-1ubuntu3.2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `eve_aim`
--

DELIMITER $$
--
-- Procedures
--
DROP PROCEDURE IF EXISTS `Median`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `Median`( tbl CHAR(64), col CHAR(64), OUT res DOUBLE )
BEGIN 
  DECLARE arg CHAR(64); 
  SET @sql = CONCAT( 'SELECT ((COUNT(*))/2) INTO @c FROM ', tbl ); 
  PREPARE stmt FROM @sql; 
  EXECUTE stmt; 
  DROP PREPARE stmt; 
  SET @a = CONVERT(FLOOR(@c), SIGNED); 
  IF @a = @c THEN  
    BEGIN 
      SET @a = @a-1; 
      SET @b = 2; 
      SET arg = CONCAT( 'AVG(', col, ')' ); 
    END; 
  ELSE 
    BEGIN 
      SET @b = 1; 
      SET arg = col; 
    END; 
  END IF; 
  SET @sql = CONCAT('SELECT ', arg, ' INTO @res FROM (SELECT ', col, ' FROM ', tbl,  
                    ' ORDER BY ', col, ' LIMIT ?,?) as tmp'); 
  PREPARE stmt FROM @sql; 
  EXECUTE stmt USING @a, @b; 
  DROP PREPARE stmt; 
  SET res=@res; 
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `emdrJsonmessages`
--

DROP TABLE IF EXISTS `emdrJsonmessages`;
CREATE TABLE IF NOT EXISTS `emdrJsonmessages` (
  `msgKey` char(36) COLLATE latin1_general_ci NOT NULL,
  `msgReceived` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `msgType` varchar(16) COLLATE latin1_general_ci DEFAULT NULL,
  `message` mediumblob,
  PRIMARY KEY (`msgKey`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci ROW_FORMAT=COMPRESSED;

-- --------------------------------------------------------

--
-- Table structure for table `emdrStats`
--

DROP TABLE IF EXISTS `emdrStats`;
CREATE TABLE IF NOT EXISTS `emdrStats` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `statusType` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0=no data, 1=insert, 2=update, 3=too old, 4=history',
  `statusCount` int(11) NOT NULL DEFAULT '0',
  `messageTimestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `statusType` (`statusType`,`messageTimestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=2346 ;

-- --------------------------------------------------------

--
-- Table structure for table `emdrStatsWorking`
--

DROP TABLE IF EXISTS `emdrStatsWorking`;
CREATE TABLE IF NOT EXISTS `emdrStatsWorking` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `statusType` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0=no data, 1=insert, 2=update, 3=too old, 4=history',
  PRIMARY KEY (`id`),
  KEY `statusType` (`statusType`)
) ENGINE=MEMORY  DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci AUTO_INCREMENT=9864 ;

-- --------------------------------------------------------

--
-- Table structure for table `historicalData`
--

DROP TABLE IF EXISTS `historicalData`;
CREATE TABLE IF NOT EXISTS `historicalData` (
  `uniqueKey` varchar(36) COLLATE latin1_general_ci NOT NULL,
  `regionID` int(11) NOT NULL,
  `typeID` int(11) NOT NULL,
  `historyData` mediumblob NOT NULL,
  PRIMARY KEY (`uniqueKey`),
  UNIQUE KEY `typeID_regionID` (`typeID`,`regionID`),
  KEY `typeID` (`typeID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci ROW_FORMAT=COMPRESSED;

-- --------------------------------------------------------

--
-- Table structure for table `marketData`
--

DROP TABLE IF EXISTS `marketData`;
CREATE TABLE IF NOT EXISTS `marketData` (
  `generatedAt` datetime DEFAULT NULL,
  `regionID` mediumint(8) unsigned NOT NULL,
  `typeID` int(11) NOT NULL,
  `price` double NOT NULL,
  `volumeRemaining` int(10) unsigned NOT NULL,
  `volumeEntered` int(10) NOT NULL,
  `minimumVolume` int(10) unsigned NOT NULL,
  `range` smallint(6) NOT NULL,
  `orderID` int(10) unsigned NOT NULL,
  `bid` tinyint(1) NOT NULL,
  `issueDate` datetime NOT NULL,
  `duration` smallint(6) NOT NULL,
  `stationID` int(9) unsigned NOT NULL,
  `solarSystemID` int(9) unsigned NOT NULL,
  `suspicious` char(1) COLLATE latin1_general_ci NOT NULL DEFAULT '?',
  `msgKey` varchar(36) COLLATE latin1_general_ci DEFAULT NULL,
  `ipHash` varchar(48) COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`orderID`),
  KEY `typeID` (`typeID`),
  KEY `typeID_regionID` (`typeID`,`regionID`),
  KEY `typeID_solarSystemID` (`typeID`,`solarSystemID`),
  KEY `typeID_stationID` (`typeID`,`stationID`),
  KEY `typeid_stationid_bid_price_volumeremaining` (`typeID`,`stationID`,`bid`,`price`,`volumeRemaining`),
  KEY `regionID` (`regionID`),
  KEY `generatedAt` (`generatedAt`),
  KEY `typeID_stationID_bid` (`typeID`,`stationID`,`bid`),
  KEY `typeID_regionID_bid` (`typeID`,`regionID`,`bid`),
  KEY `typeID_solarSystemID_bid` (`typeID`,`solarSystemID`,`bid`),
  KEY `typeID_suspicious` (`typeID`,`suspicious`),
  KEY `ipHash` (`ipHash`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `marketDataWarehouse`
--

DROP TABLE IF EXISTS `marketDataWarehouse`;
CREATE TABLE IF NOT EXISTS `marketDataWarehouse` (
  `generatedAt` datetime DEFAULT NULL,
  `regionID` mediumint(8) unsigned NOT NULL,
  `typeID` int(11) NOT NULL,
  `price` double NOT NULL,
  `volumeEntered` int(10) NOT NULL,
  `range` smallint(6) NOT NULL,
  `orderID` int(10) unsigned NOT NULL,
  `bid` tinyint(1) NOT NULL,
  `issueDate` datetime NOT NULL,
  `duration` smallint(6) NOT NULL,
  `stationID` int(9) unsigned NOT NULL,
  `solarSystemID` int(9) unsigned NOT NULL,
  `suspicious` char(1) COLLATE latin1_general_ci NOT NULL DEFAULT '?',
  `completeTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ipHash` varchar(48) COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`orderID`),
  KEY `typeID` (`typeID`),
  KEY `typeID_regionID` (`typeID`,`regionID`),
  KEY `typeID_solarSystemID` (`typeID`,`solarSystemID`),
  KEY `typeID_stationID` (`typeID`,`stationID`),
  KEY `typeid_stationid_bid_price_volumeremaining` (`typeID`,`stationID`,`bid`,`price`),
  KEY `regionID` (`regionID`),
  KEY `generatedAt` (`generatedAt`),
  KEY `typeID_stationID_bid` (`typeID`,`stationID`,`bid`),
  KEY `typeID_regionID_bid` (`typeID`,`regionID`,`bid`),
  KEY `typeID_solarSystemID_bid` (`typeID`,`solarSystemID`,`bid`),
  KEY `typeID_suspicious` (`typeID`,`suspicious`),
  KEY `ipHash` (`ipHash`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `seenOrders`
--

DROP TABLE IF EXISTS `seenOrders`;
CREATE TABLE IF NOT EXISTS `seenOrders` (
  `orderID` bigint(20) unsigned NOT NULL,
  `typeID` int(10) unsigned NOT NULL,
  `regionID` int(10) unsigned NOT NULL,
  `bid` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`orderID`),
  KEY `typeID_regionID` (`typeID`,`regionID`)
) ENGINE=MEMORY DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `seenOrdersWorking`
--

DROP TABLE IF EXISTS `seenOrdersWorking`;
CREATE TABLE IF NOT EXISTS `seenOrdersWorking` (
  `orderID` bigint(20) unsigned NOT NULL,
  `typeID` int(10) unsigned NOT NULL,
  `regionID` int(10) unsigned NOT NULL,
  `bid` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`orderID`),
  KEY `typeID_regionID` (`typeID`,`regionID`)
) ENGINE=MEMORY DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;


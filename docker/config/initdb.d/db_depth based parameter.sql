CREATE TABLE `drillingparameter` (
  `Well` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `Depth` float(10, 2) DEFAULT NULL,
  `TVD` float(10, 2) DEFAULT NULL,
  `Inclination` float(10, 2) DEFAULT NULL,
  `Azimuth` float(10, 2) DEFAULT NULL,
  `Elevation` float(10, 2) DEFAULT NULL,
  `Vertical_Section` float(10, 2) DEFAULT NULL,
  `Northing` float(10, 2) DEFAULT NULL,
  `Easting` float(10, 2) DEFAULT NULL
)
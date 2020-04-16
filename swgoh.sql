DROP TABLE IF EXISTS `guild`;
CREATE TABLE `guild` (
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	name VARCHAR(50),
	nb_member INT
);

DROP TABLE IF EXISTS `player`;
CREATE TABLE `player` (
	allyCode INT PRIMARY KEY NOT NULL,
	name VARCHAR(50),
	rank INT,
	fleet_rank INT,
	guild_name VARCHAR(50),
	/* guild organisation -- we divided our guild into 6 squadron to watch player developpement ( optional) */
	squadron VARCHAR(50),
	/* leader of a squadron */
	leader_squadron BOOLEAN
);

DROP TABLE IF EXISTS `unit`;
CREATE TABLE `unit` (
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	name VARCHAR(50),
	allyCode INT,
	gear INT,
	star INT,
	power INT,
	relic INT,
	NameID VARCHAR(50),
	img_link VARCHAR(70)
);

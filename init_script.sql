DROP TABLE IF EXISTS main.regions;
CREATE TABLE IF NOT EXISTS main.regions
(id INTEGER PRIMARY KEY AUTOINCREMENT, region varchar(255) not null);

DROP TABLE IF EXISTS main.cities;
CREATE TABLE IF NOT EXISTS main.cities
(id INTEGER PRIMARY KEY AUTOINCREMENT, city varchar(255) not null, region int not null,
FOREIGN KEY (region) REFERENCES regions (id) ON DELETE CASCADE ON UPDATE NO ACTION);

DROP TABLE IF EXISTS main.comments;
CREATE TABLE IF NOT EXISTS main.comments
(id INTEGER PRIMARY KEY AUTOINCREMENT ,  surname varchar(20) not null,
name varchar(20) not null, patronymic varchar(20),city int,
phone varchar(16), mail varchar(32), comment text(1024) not null,
FOREIGN KEY (city) REFERENCES cities (id) ON DELETE CASCADE ON UPDATE NO ACTION);

INSERT INTO main.regions(region) VALUES ("Краснодарский край"),
  ("Ростовская область"), ("Ставропольский край");

INSERT INTO main.cities(city, region) VALUES ("Краснодар", 1),
  ("Кропоткин", 1), ("Славянск", 1),
  ("Ростов", 2), ("Шахты", 2), ("Батайск", 2),
  ("Ставрополь", 3), ("Пятигорск", 3), ("Кисловодск", 3);
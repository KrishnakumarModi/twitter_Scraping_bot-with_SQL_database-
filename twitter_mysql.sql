CREATE DATABASE twitter_Database;

USE twitter_Database;

CREATE TABLE twitter_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Bio VARCHAR(300),
    Followers varchar(300),
    Following VARCHAR(300),
    Location VARCHAR(300),
    Website VARCHAR(300) 
);

select * from twitter_data ;



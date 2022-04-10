CREATE TABLE devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(30) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE sensor_data (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    device_id INT,
    location VARCHAR(30),
    temperature VARCHAR(10),
    humidity VARCHAR(10),
    pressure VARCHAR(10),
    reading_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(id)
);

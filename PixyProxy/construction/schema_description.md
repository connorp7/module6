SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    prompt TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT images_U1 UNIQUE (guid),
    INDEX images_I1 (guid)
);

CREATE TABLE roster (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guid VARCHAR(255) NOT NULL,
    user VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    class_key VARCHAR(255) NOT NULL,
    CONSTRAINT roster_U1 UNIQUE (user),
    CONSTRAINT roster_U2 UNIQUE (guid),
    INDEX roster_I1 (user),
    INDEX roster_I2 (guid)
);
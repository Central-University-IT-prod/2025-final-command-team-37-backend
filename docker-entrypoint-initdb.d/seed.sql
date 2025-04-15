-- Создание расширения и необходимых типов
CREATE
EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE userrole AS ENUM ('USER', 'ADMIN');
CREATE TYPE workplacestatus AS ENUM ('FREE', 'BOOKED', 'INACTIVE');
CREATE TYPE bookingstatus AS ENUM ('WAITING', 'PROCESSING', 'FINISHED');

-- Создание таблиц
CREATE TABLE IF NOT EXISTS users
(
    id
    BIGINT
    PRIMARY
    KEY,
    first_name
    VARCHAR
    NOT
    NULL,
    last_name
    VARCHAR,
    username
    VARCHAR
    NOT
    NULL,
    photo_url
    VARCHAR,
    balance
    INT
    NOT
    NULL
    DEFAULT
    0,
    role
    userrole
    NOT
    NULL,
    created_at
    TIMESTAMP
    NOT
    NULL
    DEFAULT
    CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS coworkings
(
    id
    UUID
    PRIMARY
    KEY
    DEFAULT
    uuid_generate_v4
(
),
    name VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    photo_url VARCHAR NOT NULL,
    cover_url VARCHAR NOT NULL,
    description VARCHAR,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE IF NOT EXISTS coworking_tariffs
(
    id
    UUID
    PRIMARY
    KEY
    DEFAULT
    uuid_generate_v4
(
),
    coworking_id UUID NOT NULL,
    name VARCHAR NOT NULL,
    color VARCHAR NOT NULL,
    price_per_hour INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY
(
    coworking_id
) REFERENCES coworkings
(
    id
) ON DELETE CASCADE
    );

CREATE TABLE IF NOT EXISTS workplaces
(
    id
    UUID
    PRIMARY
    KEY
    DEFAULT
    uuid_generate_v4
(
),
    coworking_id UUID NOT NULL,
    tariff_id UUID NOT NULL,
    number INT NOT NULL,
    name VARCHAR NOT NULL,
    status workplacestatus NOT NULL DEFAULT 'FREE',
    tags VARCHAR [] NULL,
    x_cor FLOAT NOT NULL,
    y_cor FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY
(
    coworking_id
) REFERENCES coworkings
(
    id
) ON DELETE CASCADE,
    FOREIGN KEY
(
    tariff_id
) REFERENCES coworking_tariffs
(
    id
)
  ON DELETE CASCADE
    );

CREATE TABLE IF NOT EXISTS bookings
(
    id
    UUID
    PRIMARY
    KEY
    DEFAULT
    uuid_generate_v4
(
),
    user_id BIGINT NOT NULL,
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NOT NULL,
    total_price INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY
(
    user_id
) REFERENCES users
(
    id
) ON DELETE CASCADE
    );

CREATE TABLE IF NOT EXISTS booking_workplaces
(
    booking_id
    UUID
    NOT
    NULL,
    workplace_id
    UUID
    NOT
    NULL,
    PRIMARY
    KEY
(
    booking_id,
    workplace_id
),
    FOREIGN KEY
(
    booking_id
) REFERENCES bookings
(
    id
) ON DELETE CASCADE,
    FOREIGN KEY
(
    workplace_id
) REFERENCES workplaces
(
    id
)
  ON DELETE CASCADE
    );

----------------------------------------------------
-- Вставка данных для "Основной коворкинг", тарифов и рабочих мест
----------------------------------------------------

-- Вставка коворкинга
INSERT INTO coworkings (id, name, address, photo_url, cover_url, description, created_at)
VALUES ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b',
        'Основной коворкинг',
        'Московская область, Богородский район, южнее 1км. д. Жилино',
        'https://prod-team-37-ajc3mefd.REDACTED/api/v1/cdn/file/b4413cd2-adaa-4109-b777-cab979f4a324.jpg',
        'https://prod-team-37-ajc3mefd.REDACTED/api/v1/cdn/file/c209542e-4704-4afd-bfa0-c3a1daea2e48.jpg',
        'Основной коворкинг PROD',
        '2025-03-04T04:02:10.896726'::timestamp);

-- Вставка тарифов для "Основной коворкинг"
INSERT INTO coworking_tariffs (id, coworking_id, name, color, price_per_hour, created_at)
VALUES ('8c7acd4a-cd5f-42b5-8d50-256ed4a23e22',
        '1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b',
        'ВИП',
        '#FFD700',
        100,
        '2025-03-04T04:02:10Z'::timestamp),
       ('cf3839df-7f18-4628-892d-4095ce7e8365',
        '1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b',
        'СТАНДАРТ',
        '#C0C0C0',
        80,
        '2025-03-04T04:02:10Z'::timestamp);

-- Вставка рабочих мест для "Основной коворкинг"
-- Все рабочие места будут использовать тариф с id '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22'
INSERT INTO workplaces (coworking_id, tariff_id, number, name, tags, x_cor, y_cor)
VALUES ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 1, 'Новое место',
        ARRAY[]::VARCHAR[], 44.67691744290865, 45.25184019671996),
       ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 2, 'Новое место',
        ARRAY[]::VARCHAR[], 48.36922513521635, 46.610074492135915),
       ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 3, 'Новое место',
        ARRAY[]::VARCHAR[], 46.21537898137019, 48.7228833961163),
       ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 4, 'Новое место',
        ARRAY[]::VARCHAR[], 41.59999436598557, 46.15732972699726),
       ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 5, 'Новое место',
        ARRAY[]::VARCHAR[], 55.13845590444711, 44.648180509868425),
       ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 6, 'Новое место',
        ARRAY[]::VARCHAR[], 55.13845590444711, 47.96830878755188),
       ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 7, 'Новое место',
        ARRAY[]::VARCHAR[], 58.21537898137019, 38.913413484778815),
       ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 8, 'Новое место',
        ARRAY[]::VARCHAR[], 71.75384051983174, 40.12073285848189),
       ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 9, 'Новое место',
        ARRAY[]::VARCHAR[], 71.75384051983174, 43.28994621445246),
       ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 10, 'Новое место',
        ARRAY[]::VARCHAR[], 36.06153282752404, 39.36615824991747),
       ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 11, 'Новое место',
        ARRAY[]::VARCHAR[], 35.13845590444711, 42.23354176246227),
       ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 12, 'Новое место',
        ARRAY[]::VARCHAR[], 29.907686673677887, 41.9317119190365),
       ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 13, 'Новое место',
        ARRAY[]::VARCHAR[], 58.14701004245681, 53.08264485929338),
       ('1dd2551d-bc9e-4c90-9eff-f9e7a68fb29b', '8c7acd4a-cd5f-42b5-8d50-256ed4a23e22', 14, 'Новое место',
        ARRAY[]::VARCHAR[], 25.782663067181073, 50.1346407626942);

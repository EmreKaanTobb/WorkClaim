CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT NOT NULL,
    username VARCHAR(50) NOT NULL,
    password_hash TEXT NOT NULL,
    role INTEGER NOT NULL,

    CONSTRAINT pk_users
        PRIMARY KEY (user_id),

    CONSTRAINT uq_users_username
        UNIQUE (username),

    CONSTRAINT chk_users_role
        CHECK (role IN (1, 2, 3)),

    CONSTRAINT chk_users_username_length
        CHECK (LENGTH(TRIM(username)) BETWEEN 5 AND 50),

    CONSTRAINT chk_users_password_hash_not_blank
        CHECK (LENGTH(TRIM(password_hash)) > 0),

    CONSTRAINT chk_users_user_id_range
        CHECK (user_id BETWEEN 10000000000 AND 99999999999)
);


CREATE TABLE IF NOT EXISTS facilities (
    facility_id INTEGER GENERATED ALWAYS AS IDENTITY,
    
    facility_type VARCHAR(50) NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0),

    has_screen BOOLEAN NOT NULL DEFAULT FALSE,
    has_sound_system BOOLEAN NOT NULL DEFAULT FALSE,
    has_whiteboard BOOLEAN NOT NULL DEFAULT FALSE,
    has_air_conditioning BOOLEAN NOT NULL DEFAULT FALSE,
    has_projector BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT pk_facilities
        PRIMARY KEY (facility_id)
);


CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INTEGER GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    facility_id INTEGER NOT NULL,
    reservation_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'reserved',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_reservations
        PRIMARY KEY (reservation_id),

    CONSTRAINT chk_reservations_time
        CHECK (end_time > start_time),

    CONSTRAINT fk_reservations_user
        FOREIGN KEY (user_id)
        REFERENCES users (user_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_reservations_facility
        FOREIGN KEY (facility_id)
        REFERENCES facilities (facility_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


CREATE TABLE IF NOT EXISTS notify (
    user_id BIGINT NOT NULL,
    reservation_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_notify
        PRIMARY KEY (user_id, reservation_id),

    CONSTRAINT fk_notify_user
        FOREIGN KEY (user_id)
        REFERENCES users (user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_notify_reservation
        FOREIGN KEY (reservation_id)
        REFERENCES reservations (reservation_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
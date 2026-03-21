import pytest
from Workclaim_Database import Database


@pytest.fixture(scope="module")
def db():
    database = Database()
    yield database
    database.close_connection()


@pytest.fixture(autouse=True)
def reset_database(db):
    """
    Her testten önce veritabanını temizler ve başlangıç verilerini yeniden yükler.
    """
    db.cursor.execute("TRUNCATE TABLE notify, reservations, facilities, users RESTART IDENTITY CASCADE;")
    db.db.commit()

    db.cursor.execute("""
        INSERT INTO facilities (
            facility_type, capacity, has_screen, has_sound_system,
            has_whiteboard, has_air_conditioning, has_projector
        ) VALUES
        ('Toplanti Odasi', 10, TRUE, FALSE, TRUE, TRUE, TRUE),
        ('Sinif', 30, TRUE, TRUE, TRUE, TRUE, TRUE),
        ('Laboratuvar', 20, TRUE, TRUE, FALSE, TRUE, TRUE),
        ('Konferans Salonu', 100, TRUE, TRUE, TRUE, TRUE, TRUE);
    """)

    db.cursor.execute("""
        INSERT INTO reservations (user_id, facility_id, date, start_time, end_time, status) VALUES
        (NULL, 1, '2026-03-25', '09:00', '10:00', 'empty'),
        (NULL, 1, '2026-03-25', '10:00', '11:00', 'empty'),
        (NULL, 2, '2026-03-25', '13:00', '14:00', 'empty'),
        (NULL, 3, '2026-03-26', '15:00', '16:00', 'empty'),
        (NULL, 4, '2026-03-27', '09:00', '10:00', 'empty');
    """)
    db.db.commit()


@pytest.fixture
def test_users():
    return {
        "student_id": 22212345678,
        "teacher_id": 33312345678,
        "admin_id": 44412345678,
        "student_username": "ogrenci1",
        "teacher_username": "ogretmen1",
        "admin_username": "yonetim1",
        "password": "123456"
    }


def create_test_users(db, users):
    db.register_user(users["student_id"], users["student_username"], users["password"])
    db.register_user(users["teacher_id"], users["teacher_username"], users["password"])
    db.register_user(users["admin_id"], users["admin_username"], users["password"])


# ---------------------------
# USER TESTLERI
# ---------------------------

def test_register_user_success(db, test_users):
    result = db.register_user(
        test_users["student_id"],
        test_users["student_username"],
        test_users["password"]
    )
    assert result == "Kullanıcı sisteme eklendi."


def test_register_user_duplicate(db, test_users):
    db.register_user(
        test_users["student_id"],
        test_users["student_username"],
        test_users["password"]
    )

    result = db.register_user(
        test_users["student_id"],
        "baska_ad",
        test_users["password"]
    )

    assert result == "Bu kullanıcı zaten mevcut, ya yeni bir kullanıcı adı seçin ya da giriş yapın."


def test_login_user_success(db, test_users):
    db.register_user(
        test_users["student_id"],
        test_users["student_username"],
        test_users["password"]
    )

    assert db.login_user(test_users["student_id"], test_users["password"]) is True


def test_login_user_wrong_password(db, test_users):
    db.register_user(
        test_users["student_id"],
        test_users["student_username"],
        test_users["password"]
    )

    assert db.login_user(test_users["student_id"], "yanlis") is False


def test_login_user_invalid_id(db, test_users):
    assert db.login_user(123, test_users["password"]) is False


def test_get_user(db, test_users):
    db.register_user(
        test_users["student_id"],
        test_users["student_username"],
        test_users["password"]
    )

    user = db.get_user(test_users["student_id"])

    assert user is not None
    assert user[0] == test_users["student_id"]
    assert user[1] == test_users["student_username"]
    assert user[2] == 1


# ---------------------------
# FACILITY TESTLERI
# ---------------------------

def test_filter_facilities_by_type(db):
    result = db.filter_facilities(facility_type="Toplanti Odasi")

    assert len(result) == 1
    assert result[0][1] == "Toplanti Odasi"


def test_filter_facilities_by_capacity(db):
    result = db.filter_facilities(capacity=20)

    assert len(result) == 3


def test_filter_facilities_by_features(db):
    result = db.filter_facilities(has_projector=True, has_air_conditioning=True)

    assert len(result) >= 1


# ---------------------------
# RESERVATION TESTLERI
# ---------------------------

def test_reserve_empty_slot(db, test_users):
    create_test_users(db, test_users)

    result = db.reserve(test_users["student_id"], 1)
    reservation = db.get_reservation_info(1)

    assert result == "Rezervasyon başarıyla oluşturuldu."
    assert reservation is not None
    assert reservation["user_id"] == test_users["student_id"]
    assert reservation["status"] == "reserved"


def test_teacher_overrides_student(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["student_id"], 1)
    result = db.reserve(test_users["teacher_id"], 1)
    reservation = db.get_reservation_info(1)

    assert result == "Rezervasyon override edilerek kullanıcıya verildi. Eski kullanıcı için bildirim kaydı oluşturuldu."
    assert reservation["user_id"] == test_users["teacher_id"]


def test_student_cannot_override_teacher(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["teacher_id"], 1)
    result = db.reserve(test_users["student_id"], 1)

    assert result == "Bu rezervasyon daha yüksek veya eşit öncelikli bir kullanıcıda olduğu için alınamaz."


def test_admin_overrides_teacher(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["teacher_id"], 1)
    result = db.reserve(test_users["admin_id"], 1)
    reservation = db.get_reservation_info(1)

    assert result == "Rezervasyon override edilerek kullanıcıya verildi. Eski kullanıcı için bildirim kaydı oluşturuldu."
    assert reservation["user_id"] == test_users["admin_id"]


def test_get_reservations(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["student_id"], 1)
    reservations = db.get_reservations(test_users["student_id"])

    assert len(reservations) == 1
    assert reservations[0][0] == 1


def test_get_reservation(db):
    reservation = db.get_reservation(1)

    assert reservation is not None
    assert reservation[0] == 1


def test_cancel_reservation(db):
    result = db.cancel_reservation(2)
    reservation = db.get_reservation_info(2)

    assert result == "Rezervasyon başarıyla iptal edildi."
    assert reservation["status"] == "cancelled"


# ---------------------------
# NOTIFICATION TESTLERI
# ---------------------------

def test_bring_notifications_after_override(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["student_id"], 1)
    db.reserve(test_users["teacher_id"], 1)

    notifications = db.bring_notifications(test_users["student_id"])

    assert len(notifications) == 1
    assert notifications[0][0] == 1
    assert notifications[0][6] == test_users["teacher_id"]


def test_notifications_deleted_after_read(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["student_id"], 1)
    db.reserve(test_users["teacher_id"], 1)

    first_read = db.bring_notifications(test_users["student_id"])
    second_read = db.bring_notifications(test_users["student_id"])

    assert len(first_read) == 1
    assert second_read == []


# ---------------------------
# DELETE USER TESTLERI
# ---------------------------

def test_delete_user(db, test_users):
    create_test_users(db, test_users)

    result = db.delete_user(test_users["student_id"])
    user = db.get_user(test_users["student_id"])

    assert result == "Kullanıcı ve rezervasyonları başarıyla silindi."
    assert user is None
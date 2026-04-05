import pytest
from database_functions import Database


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
    db.cursor.execute("""
        TRUNCATE TABLE notify, reservations, facilities, users
        RESTART IDENTITY CASCADE;
    """)
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


def insert_empty_reservation_and_get_id(db, facility_id, date, start_time, end_time):
    db.cursor.execute("""
        INSERT INTO reservations (user_id, facility_id, date, start_time, end_time, status)
        VALUES (NULL, %s, %s, %s, %s, 'empty')
        RETURNING reservation_id
    """, (facility_id, date, start_time, end_time))
    reservation_id = db.cursor.fetchone()[0]
    db.db.commit()
    return reservation_id


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

    assert result == "Bu kullanıcı zaten mevcut, ya giriş yapın."


def test_register_user_invalid_id_length(db, test_users):
    result = db.register_user(123, test_users["student_username"], test_users["password"])
    assert result == "user_id 11 haneli sayısal olmalıdır."


def test_register_user_invalid_id_prefix(db, test_users):
    result = db.register_user(55512345678, test_users["student_username"], test_users["password"])
    assert result == "Geçersiz user_id formatı. (222 / 333 / 444 ile başlamalı)"


def test_register_user_empty_username(db, test_users):
    result = db.register_user(test_users["student_id"], "", test_users["password"])
    assert result == "Kullanıcı adı boş bırakılamaz."


def test_register_user_short_username(db, test_users):
    result = db.register_user(test_users["student_id"], "abc", test_users["password"])
    assert result == "Kullanıcı adı en az 5 karakter olmalıdır."


def test_register_user_empty_password(db, test_users):
    result = db.register_user(test_users["student_id"], test_users["student_username"], "")
    assert result == "Şifre boş bırakılamaz."


def test_register_user_short_password(db, test_users):
    result = db.register_user(test_users["student_id"], test_users["student_username"], "1234")
    assert result == "Şifre en az 5 karakter olmalıdır."


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


def test_update_password_success(db, test_users):
    db.register_user(
        test_users["student_id"],
        test_users["student_username"],
        test_users["password"]
    )

    result = db.update_password(test_users["student_id"], "yenisifre123")

    assert result == "Password updated successfully."
    assert db.login_user(test_users["student_id"], "yenisifre123") is True
    assert db.login_user(test_users["student_id"], test_users["password"]) is False


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


def test_filter_facilities_no_match(db):
    result = db.filter_facilities(facility_type="Stadyum")
    assert result == []


# ---------------------------
# RESERVATION LIMIT TESTLERI
# ---------------------------

def test_get_user_reservation_limit_student(db, test_users):
    create_test_users(db, test_users)

    limit_value = db.get_user_reservation_limit(test_users["student_id"])
    assert limit_value == 3


def test_get_user_reservation_limit_teacher(db, test_users):
    create_test_users(db, test_users)

    limit_value = db.get_user_reservation_limit(test_users["teacher_id"])
    assert limit_value == 5


def test_get_user_reservation_limit_admin(db, test_users):
    create_test_users(db, test_users)

    limit_value = db.get_user_reservation_limit(test_users["admin_id"])
    assert limit_value == 8


def test_get_user_reservation_limit_nonexistent_user(db):
    limit_value = db.get_user_reservation_limit(22299999999)
    assert limit_value is None


def test_get_active_reservation_count_initially_zero(db, test_users):
    create_test_users(db, test_users)

    active_count = db.get_active_reservation_count(test_users["student_id"])
    assert active_count == 0


def test_get_active_reservation_count_after_reservation(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["student_id"], 1)
    active_count = db.get_active_reservation_count(test_users["student_id"])

    assert active_count == 1


def test_has_reached_reservation_limit_false_initially(db, test_users):
    create_test_users(db, test_users)

    assert db.has_reached_reservation_limit(test_users["student_id"]) is False


def test_has_reached_reservation_limit_true_when_limit_filled(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["student_id"], 1)
    db.reserve(test_users["student_id"], 2)
    db.reserve(test_users["student_id"], 3)

    assert db.has_reached_reservation_limit(test_users["student_id"]) is True


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


def test_reserve_nonexistent_user(db):
    result = db.reserve(22299999999, 1)
    assert result == "Rezervasyon yapmaya çalışan kullanıcı bulunamadı."


def test_reserve_nonexistent_reservation_id(db, test_users):
    create_test_users(db, test_users)

    result = db.reserve(test_users["student_id"], 999)
    assert result == "Belirtilen reservation_id için rezervasyon kaydı bulunamadı."


def test_reservation_limit_blocks_new_reservation(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["student_id"], 1)
    db.reserve(test_users["student_id"], 2)
    db.reserve(test_users["student_id"], 3)

    new_reservation_id = insert_empty_reservation_and_get_id(
        db, 1, "2026-03-28", "10:00", "11:00"
    )

    result = db.reserve(test_users["student_id"], new_reservation_id)

    assert result == "Rezervasyon limitine ulaştınız. En fazla 3 aktif rezervasyon alabilirsiniz."


def test_teacher_overrides_student(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["student_id"], 1)
    result = db.reserve(test_users["teacher_id"], 1)
    reservation = db.get_reservation_info(1)

    assert result == "Rezervasyon override edilerek kullanıcıya verildi. Eski kullanıcı için bildirim kaydı oluşturuldu."
    assert reservation["user_id"] == test_users["teacher_id"]
    assert reservation["status"] == "reserved"


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


def test_cancel_reserved_reservation(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["student_id"], 2)
    result = db.cancel_reservation(2)
    reservation = db.get_reservation_info(2)

    assert result == "Rezervasyon başarıyla iptal edildi."
    assert reservation["status"] == "cancelled"
    assert reservation["user_id"] == test_users["student_id"]


def test_cancel_nonexistent_reservation(db):
    result = db.cancel_reservation(999)
    assert result == "İptal edilecek rezervasyon veritabanında bulunamadı."


def test_cancelled_reservation_reduces_active_count(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["student_id"], 1)
    assert db.get_active_reservation_count(test_users["student_id"]) == 1

    db.cancel_reservation(1)
    assert db.get_active_reservation_count(test_users["student_id"]) == 0
    assert db.has_reached_reservation_limit(test_users["student_id"]) is False


# ---------------------------
# NOTIFICATION TESTLERI
# ---------------------------

def test_notify_cancellation_manual(db, test_users):
    create_test_users(db, test_users)

    inserted = db.notify_cancellation(test_users["student_id"], 1)
    assert inserted is True

    notifications = db.bring_notifications(test_users["student_id"])
    assert len(notifications) == 1
    assert notifications[0][0] == 1


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
# FIND SLOT TESTLERI
# ---------------------------

def test_find_reservation_slot_success(db):
    reservation_id = db.find_reservation_slot(1, "2026-03-25", "09:00", "10:00")
    assert reservation_id == 1


def test_find_reservation_slot_not_found(db):
    reservation_id = db.find_reservation_slot(1, "2026-04-01", "09:00", "10:00")
    assert reservation_id is None


# ---------------------------
# OVERRIDE DETAILS TESTLERI
# ---------------------------

def test_get_override_details_for_empty_slot(db, test_users):
    create_test_users(db, test_users)

    result = db.get_override_details(test_users["teacher_id"], 1)

    assert result["can_override"] is False
    assert result["needs_confirmation"] is False
    assert result["message"] == "Bu slot doğrudan alınabilir."


def test_get_override_details_for_same_owner(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["student_id"], 1)
    result = db.get_override_details(test_users["student_id"], 1)

    assert result["can_override"] is False
    assert result["needs_confirmation"] is False
    assert result["message"] == "Bu rezervasyon zaten size ait."


def test_get_override_details_teacher_can_override_student(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["student_id"], 1)
    result = db.get_override_details(test_users["teacher_id"], 1)

    assert result["can_override"] is True
    assert result["needs_confirmation"] is True
    assert result["reservation_id"] == 1
    assert result["owner_user_id"] == test_users["student_id"]
    assert result["owner_username"] == test_users["student_username"]
    assert result["facility_id"] == 1


def test_get_override_details_student_cannot_override_teacher(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["teacher_id"], 1)
    result = db.get_override_details(test_users["student_id"], 1)

    assert result["can_override"] is False
    assert result["needs_confirmation"] is False
    assert result["message"] == "Bu rezervasyon daha yüksek veya eşit öncelikli bir kullanıcıda olduğu için alınamaz."


def test_get_override_details_nonexistent_user(db):
    result = db.get_override_details(22299999999, 1)

    assert result["can_override"] is False
    assert result["message"] == "Rezervasyon yapmaya çalışan kullanıcı bulunamadı."


def test_get_override_details_nonexistent_reservation(db, test_users):
    create_test_users(db, test_users)

    result = db.get_override_details(test_users["teacher_id"], 999)

    assert result["can_override"] is False
    assert result["message"] == "Belirtilen reservation_id için rezervasyon kaydı bulunamadı."


# ---------------------------
# DELETE USER TESTLERI
# ---------------------------

def test_delete_user(db, test_users):
    create_test_users(db, test_users)

    db.reserve(test_users["student_id"], 1)
    result = db.delete_user(test_users["student_id"])
    user = db.get_user(test_users["student_id"])
    reservation = db.get_reservation_info(1)

    assert result == "Kullanıcı ve rezervasyonları başarıyla silindi."
    assert user is None
    assert reservation["status"] == "cancelled"
    assert reservation["user_id"] is None


def test_delete_nonexistent_user(db):
    result = db.delete_user(22299999999)
    assert result == "Kullanıcı bulunamadı."
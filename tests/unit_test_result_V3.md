```text
============================================================================= test session starts =============================================================================
platform win32 -- Python 3.13.1, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\USEr\AppData\Local\Programs\Python\Python313\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\USEr\Desktop\copy_V5
collected 50 items

test_database_unit_V3.py::test_register_user_success PostgreSQL bağlantısı başarıyla kuruldu.
PASSED
test_database_unit_V3.py::test_register_user_duplicate PASSED
test_database_unit_V3.py::test_register_user_invalid_id_length PASSED
test_database_unit_V3.py::test_register_user_invalid_id_prefix PASSED
test_database_unit_V3.py::test_register_user_empty_username PASSED
test_database_unit_V3.py::test_register_user_short_username PASSED
test_database_unit_V3.py::test_register_user_empty_password PASSED
test_database_unit_V3.py::test_register_user_short_password PASSED
test_database_unit_V3.py::test_login_user_success PASSED
test_database_unit_V3.py::test_login_user_wrong_password PASSED
test_database_unit_V3.py::test_login_user_invalid_id PASSED
test_database_unit_V3.py::test_get_user PASSED
test_database_unit_V3.py::test_update_password_success PASSED
test_database_unit_V3.py::test_filter_facilities_by_type PASSED
test_database_unit_V3.py::test_filter_facilities_by_capacity PASSED
test_database_unit_V3.py::test_filter_facilities_by_features PASSED
test_database_unit_V3.py::test_filter_facilities_no_match PASSED
test_database_unit_V3.py::test_get_user_reservation_limit_student PASSED
test_database_unit_V3.py::test_get_user_reservation_limit_teacher PASSED
test_database_unit_V3.py::test_get_user_reservation_limit_admin PASSED
test_database_unit_V3.py::test_get_user_reservation_limit_nonexistent_user PASSED
test_database_unit_V3.py::test_get_active_reservation_count_initially_zero PASSED
test_database_unit_V3.py::test_get_active_reservation_count_after_reservation PASSED
test_database_unit_V3.py::test_has_reached_reservation_limit_false_initially PASSED
test_database_unit_V3.py::test_has_reached_reservation_limit_true_when_limit_filled PASSED
test_database_unit_V3.py::test_reserve_empty_slot PASSED
test_database_unit_V3.py::test_reserve_nonexistent_user PASSED
test_database_unit_V3.py::test_reserve_nonexistent_reservation_id PASSED
test_database_unit_V3.py::test_reservation_limit_blocks_new_reservation PASSED
test_database_unit_V3.py::test_teacher_overrides_student PASSED
test_database_unit_V3.py::test_student_cannot_override_teacher PASSED
test_database_unit_V3.py::test_admin_overrides_teacher PASSED
test_database_unit_V3.py::test_get_reservations PASSED
test_database_unit_V3.py::test_get_reservation PASSED
test_database_unit_V3.py::test_cancel_reserved_reservation PASSED
test_database_unit_V3.py::test_cancel_nonexistent_reservation PASSED
test_database_unit_V3.py::test_cancelled_reservation_reduces_active_count PASSED
test_database_unit_V3.py::test_notify_cancellation_manual PASSED
test_database_unit_V3.py::test_bring_notifications_after_override PASSED
test_database_unit_V3.py::test_notifications_deleted_after_read PASSED
test_database_unit_V3.py::test_find_reservation_slot_success PASSED
test_database_unit_V3.py::test_find_reservation_slot_not_found PASSED
test_database_unit_V3.py::test_get_override_details_for_empty_slot PASSED
test_database_unit_V3.py::test_get_override_details_for_same_owner PASSED
test_database_unit_V3.py::test_get_override_details_teacher_can_override_student PASSED
test_database_unit_V3.py::test_get_override_details_student_cannot_override_teacher PASSED
test_database_unit_V3.py::test_get_override_details_nonexistent_user PASSED
test_database_unit_V3.py::test_get_override_details_nonexistent_reservation PASSED
test_database_unit_V3.py::test_delete_user PASSED
test_database_unit_V3.py::test_delete_nonexistent_user PASSEDVeritabanı bağlantısı sona erdi


============================================================================= 50 passed in 20.73s =============================================================================

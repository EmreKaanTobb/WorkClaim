## Test Output

```bash
PS C:\Users\USEr\Desktop\Workclaim\V3_Connected> py -m pytest -v -s test_database_unit_V2.py
================================================================================================== test session starts ===================================================================================================
platform win32 -- Python 3.13.1, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\USEr\AppData\Local\Programs\Python\Python313\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\USEr\Desktop\Workclaim\V3_Connected
collected 28 items

test_database_unit_V2.py::test_register_user_success PostgreSQL bağlantısı başarıyla kuruldu.
PASSED
test_database_unit_V2.py::test_register_user_duplicate PASSED
test_database_unit_V2.py::test_login_user_success PASSED
test_database_unit_V2.py::test_login_user_wrong_password PASSED
test_database_unit_V2.py::test_login_user_invalid_id PASSED
test_database_unit_V2.py::test_get_user PASSED
test_database_unit_V2.py::test_filter_facilities_by_type PASSED
test_database_unit_V2.py::test_filter_facilities_by_capacity PASSED
test_database_unit_V2.py::test_filter_facilities_by_features PASSED
test_database_unit_V2.py::test_get_user_reservation_limit_student PASSED
test_database_unit_V2.py::test_get_user_reservation_limit_teacher PASSED
test_database_unit_V2.py::test_get_user_reservation_limit_admin PASSED
test_database_unit_V2.py::test_get_active_reservation_count_initially_zero PASSED
test_database_unit_V2.py::test_get_active_reservation_count_after_reservation PASSED
test_database_unit_V2.py::test_has_reached_reservation_limit_false_initially PASSED
test_database_unit_V2.py::test_has_reached_reservation_limit_true_when_limit_filled PASSED
test_database_unit_V2.py::test_reserve_empty_slot PASSED
test_database_unit_V2.py::test_reservation_limit_blocks_new_reservation PASSED
test_database_unit_V2.py::test_teacher_overrides_student PASSED
test_database_unit_V2.py::test_student_cannot_override_teacher PASSED
test_database_unit_V2.py::test_admin_overrides_teacher PASSED
test_database_unit_V2.py::test_get_reservations PASSED
test_database_unit_V2.py::test_get_reservation PASSED
test_database_unit_V2.py::test_cancel_reservation PASSED
test_database_unit_V2.py::test_cancelled_reservation_reduces_active_count PASSED
test_database_unit_V2.py::test_bring_notifications_after_override PASSED
test_database_unit_V2.py::test_notifications_deleted_after_read PASSED
test_database_unit_V2.py::test_delete_user PASSEDVeritabanı bağlantısı sona erdi

================================================================================================== 28 passed in 13.89s ===================================================================================================
Test conducted on 3/03/2026.

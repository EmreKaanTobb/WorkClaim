import psycopg
import traceback
import bcrypt
import psycopg.rows


class Database:
    _instance = None

    ''' Burada database bağlantısını Singleton kuruyoruz.'''
    ''' Kullanıcı arayüzündeki fonksiyonlar bu sınıfın bir objesini çağırmalı.'''
    ''' Bu sınıfın fonksiyonlarının döndürdüğü değerler kullanılacak.'''
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_connection()
        return cls._instance


    def _init_connection(self):
        try:
            self.db = psycopg.connect(
                host="localhost",
                user="postgres",
                password="workclaim123",
                dbname="workclaim",
                port=5432
            )
            self.cursor = self.db.cursor()
            print("PostgreSQL bağlantısı başarıyla kuruldu.")
        except Exception as e:
            print(f"Veritabanı bağlantısı başarısız. Hata mesajı: {e}")
            self.db = None
            self.cursor = None


        """user_id'den kullanıcı rolü belirleniyor.Şimdilik placeholder bir kriter koydum."""
    def register_user(self, user_id, username, password):
        try:
            user_id_str = str(user_id)

            # user_id format kontrolü
            if len(user_id_str) != 11 or not user_id_str.isdigit():
                return "user_id 11 haneli sayısal olmalıdır."

            # username kontrolü
            if username is None or not str(username).strip():
                return "Kullanıcı adı boş bırakılamaz."
            if len(username.strip()) < 5:
                return "Kullanıcı adı en az 5 karakter olmalıdır."

            # password kontrolü
            if password is None or not str(password).strip():
                return "Şifre boş bırakılamaz."
            if len(password) < 5:
                return "Şifre en az 5 karakter olmalıdır."

            username = username.strip()

            # user_id kontrolü (veritabanında var mı)
            check_query = "SELECT COUNT(*) FROM users WHERE user_id = %s"
            self.cursor.execute(check_query, (user_id,))
            user_exists = self.cursor.fetchone()[0] > 0

            if user_exists:
                return "Bu kullanıcı zaten mevcut, ya giriş yapın."

            # rol belirleme
            if user_id_str.startswith("222"):
                role = 1  # öğrenci
            elif user_id_str.startswith("333"):
                role = 2  # öğretmen
            elif user_id_str.startswith("444"):
                role = 3  # yönetim
            else:
                return "Geçersiz user_id formatı. (222 / 333 / 444 ile başlamalı)"

            # şifre hashleme
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            # kullanıcı ekleme
            query = """
                INSERT INTO users (user_id, username, password, role)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (user_id, username, hashed_password, role))
            self.db.commit()

            if self.cursor.rowcount > 0:
                return "Kullanıcı sisteme eklendi."
            return "Kullanıcı sisteme eklenemedi."


        except psycopg.Error as err:
            self.db.rollback()
            print(f"Veritabanı hatası: {err}")
            traceback.print_exc()
            return "Veritabanı operasyonu esnasında hata oluştu!"



    """user_id ve şifre bu kısımda kontrol ediliyor."""
    """user_id mevcutsa hashli şifre veritabanından çekiliyor."""
    """Parametrede verilen password hash ediliyor, eğer hashli password ile uyuyorsa True, uymuyorsa false dönüyor."""
    def login_user(self, user_id, password):
        try:
            
            # user_id format kontrolü
            user_id_str = str(user_id)

            if len(user_id_str) != 11 or not user_id_str.isdigit():
                return False

            check_query = "SELECT password FROM users WHERE user_id = %s"
            self.cursor.execute(check_query, (user_id,))
            result = self.cursor.fetchone()

            if result is None:
                return False

            stored_hash_password = result[0]

            if bcrypt.checkpw(password.encode("utf-8"), stored_hash_password.encode("utf-8")):
                return True
            else:
                return False


        except psycopg.Error as err:
            print(f"Veritabanı hatası oluştu. Hata mesajı: {err}")
            traceback.print_exc()
            return False


        except Exception as e:
            print(f"Beklenmeyen bir durum oluştu.Hata mesajı: {e}")
            traceback.print_exc()
            return False



    """Uygulama kapatılırken veritabanı bağlantısını sonlandırır."""
    def close_connection(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
            print("Veritabanı bağlantısı sona erdi")
        except Exception as e:
            print(f"Bağlantı kapatılırken hata oluştu.Hata mesajı: {e}")




    """Kullanıcının sahip olduğu bütün rezervasyonları döndürür."""
    def get_reservations(self, user_id):
        try:
            check_query = """
                SELECT reservation_id, facility_id, date, start_time, end_time, status
                FROM reservations
                WHERE user_id = %s
                ORDER BY date DESC
            """
            self.cursor.execute(check_query, (user_id,))
            rows = self.cursor.fetchall()
            
            
            return rows

        except psycopg.Error as err:
            print(f"Reservasyon döndürme işlemi sırasında hata oluştu. Hata Mesajı: {err}")
            traceback.print_exc()
            return []





    """reservation_id ile belirtilmiş rezervasyonu veritabanından döndürür.""" 
    def get_reservation(self, reservation_id):
        try:
            check_query = """
                SELECT reservation_id, user_id, facility_id, date, start_time, end_time, status
                FROM reservations
                WHERE reservation_id = %s
            """
            self.cursor.execute(check_query, (reservation_id,))
            rows = self.cursor.fetchone()
            
            
            return rows


        except psycopg.Error as err:
            print(f"Reservasyon döndürme işlemi sırasında hata oluştu. Hata Mesajı: {err}")
            traceback.print_exc()
            return None




    """Kullanıcının reservation_id ile belirtilmiş rezervasyonunu iptal eder."""
    def cancel_reservation(self, reservation_id):
        try:
            query = """
                UPDATE reservations
                SET status = %s
                WHERE reservation_id = %s
            """
            self.cursor.execute(query, ("cancelled", reservation_id))
            self.db.commit()


            if self.cursor.rowcount > 0:
                return "Rezervasyon başarıyla iptal edildi."
            else:
                return "İptal edilecek rezervasyon veritabanında bulunamadı."


        except psycopg.Error as err:
            self.db.rollback()
            print(f"Rezervasyon iptal edilirken hata oluştu. Hata mesajı: {err}")
            traceback.print_exc()
            return "Rezervasyon iptal işlemi sırasında hata oluştu!"
        
        
        
        
    """Kullanıcının hesabını veritabanından kaldırır ve tüm randevularının status değerini "cancelled" olarak günceller"""
    def delete_user(self, user_id):
        try:
            # kullacının mevcut olup olmadığı kontrol edilir
            self.cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            if self.cursor.fetchone() is None:
                return "Kullanıcı bulunamadı."

            # kullanıcı rezervasyonları "cancelled" olarak işaretleni
            self.cursor.execute("""
                UPDATE reservations
                SET status = %s
                WHERE user_id = %s
            """, ("cancelled", user_id))
            
            
            # kullanıcıyı sil
            self.cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            
            
            self.db.commit()
            return "Kullanıcı ve rezervasyonları başarıyla silindi."


        except psycopg.Error as err:
            self.db.rollback()
            print(f"Hata: {err}")
            traceback.print_exc()
            return "Hesap silme işlemi esnasında hata oluştu!"
        

    def update_password(self, user_id, new_password):
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt).decode('utf-8')
            self.cursor.execute("UPDATE users SET password = %s WHERE user_id = %s", (hashed_password, user_id))
            self.db.commit()
            return "Password updated successfully."
        except Exception as e:
            return f"Error: {e}"
        
        
        
    """Veritabanından "user_id ile belirtilmiş kullanıcı döndürür."""
    def get_user(self, user_id):
        try:
            query = """
                SELECT user_id, username, role
                FROM users
                WHERE user_id = %s
            """
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchone()

        except psycopg.Error as err:
            print(f"Veritabanı hatası oluştu. Hata mesajı: {err}")
            traceback.print_exc()
            return None

        except Exception as e:
            print(f"Beklenmeyen bir durum oluştu. Hata mesajı: {e}")
            traceback.print_exc()
            return None



    """Veritabanında parametrede verilen filtrelere uygun rezervasyonları döndürür.""" 
    def filter_facilities(self, facility_type=None, capacity=None, has_screen=None,
                      has_sound_system=None, has_whiteboard=None,
                      has_air_conditioning=None, has_projector=None):
        
        # bu kısımda 1=1 yazmamızın sebebi query'e filtrelerin varlığına bağlı olarak
        # seçim kriterlerini append etmek.Tüm filtreleri doldurma zorunda olmama opsiyonu olarak koydum.
        try:
            query = """
                SELECT facility_id, facility_type, capacity, has_screen, has_sound_system,
                    has_whiteboard, has_air_conditioning, has_projector
                FROM facilities
                WHERE 1=1
            """
            params = []

            if facility_type is not None:
                query += " AND facility_type = %s"
                params.append(facility_type)

            if capacity is not None:
                query += " AND capacity >= %s"
                params.append(capacity)

            if has_screen is not None:
                query += " AND has_screen = %s"
                params.append(has_screen)

            if has_sound_system is not None:
                query += " AND has_sound_system = %s"
                params.append(has_sound_system)

            if has_whiteboard is not None:
                query += " AND has_whiteboard = %s"
                params.append(has_whiteboard)

            if has_air_conditioning is not None:
                query += " AND has_air_conditioning = %s"
                params.append(has_air_conditioning)

            if has_projector is not None:
                query += " AND has_projector = %s"
                params.append(has_projector)

            self.cursor.execute(query, tuple(params))
            return self.cursor.fetchall()

        except psycopg.Error as err:
            print(f"Randevu getirme işlemi sırasında hata oluştu. Hata mesajı: {err}")
            traceback.print_exc()
            return []

        except Exception as e:
            print(f"Randevuların getirilmesi esnasında hata oluştu.Hata mesajı: {e}")
            traceback.print_exc()
            return []  


    """Kullanıcının rolüne göre sahip olduğu maksimum rezervasyon limitini döndürür."""
    def get_user_reservation_limit(self, user_id):
        try:
            role_query = "SELECT role FROM users WHERE user_id = %s"
            self.cursor.execute(role_query, (user_id,))
            result = self.cursor.fetchone()

            if result is None:
                return None

            role = result[0]

            # rol 1 = öğrenci, rol 2 = öğretmen, rol 3 = yönetim
            if role == 1:
                return 3
            elif role == 2:
                return 5
            elif role == 3:
                return 8
            else:
                return None

        except psycopg.Error as err:
            print(f"Kullanıcı rezervasyon limiti alınırken hata oluştu. Hata mesajı: {err}")
            traceback.print_exc()
            return None

        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu. Hata mesajı: {e}")
            traceback.print_exc()
            return None


    """Kullanıcının aktif durumdaki rezervasyon sayısını döndürür."""
    def get_active_reservation_count(self, user_id):
        try:
            query = """
                SELECT COUNT(*)
                FROM reservations
                WHERE user_id = %s
                  AND status = %s
            """
            self.cursor.execute(query, (user_id, "reserved"))
            result = self.cursor.fetchone()

            if result is None:
                return 0

            return result[0]

        except psycopg.Error as err:
            print(f"Aktif rezervasyon sayısı alınırken hata oluştu. Hata mesajı: {err}")
            traceback.print_exc()
            return 0

        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu. Hata mesajı: {e}")
            traceback.print_exc()
            return 0


    """Kullanıcının rezervasyon limitine ulaşıp ulaşmadığını kontrol eder."""
    def has_reached_reservation_limit(self, user_id):
        try:
            reservation_limit = self.get_user_reservation_limit(user_id)

            if reservation_limit is None:
                return False

            active_count = self.get_active_reservation_count(user_id)

            return active_count >= reservation_limit

        except Exception as e:
            print(f"Rezervasyon limiti kontrol edilirken hata oluştu. Hata mesajı: {e}")
            traceback.print_exc()
            return False


    """Veritabanından rezervasyon alma fonksiyon"""
    def reserve(self, user_id, reservation_id):
        try:
            # Rezervasyonu almak isteyen kullanıcının rolünü çekiyoruz.
            role_query = "SELECT role FROM users WHERE user_id = %s"
            self.cursor.execute(role_query, (user_id,))
            requester = self.cursor.fetchone()

            if requester is None:
                return "Rezervasyon yapmaya çalışan kullanıcı bulunamadı."

            requester_role = requester[0]

            # Kullanıcı rezervasyon limitine ulaştıysa yeni rezervasyon alamaz.
            if self.has_reached_reservation_limit(user_id):
                reservation_limit = self.get_user_reservation_limit(user_id)
                return f"Rezervasyon limitine ulaştınız. En fazla {reservation_limit} aktif rezervasyon alabilirsiniz."


            # Race condition oluşmaması için ilgili rezervasyon satırını kilitliyoruz.
            reservation_query = """
                SELECT reservation_id, user_id, status
                FROM reservations
                WHERE reservation_id = %s
                FOR UPDATE
            """
            self.cursor.execute(reservation_query, (reservation_id,))
            reservation = self.cursor.fetchone()


            # İstenen reservation_id veritabanında yoksa işlem iptal edilir.
            if reservation is None:
                return "Belirtilen reservation_id için rezervasyon kaydı bulunamadı."

            _, current_user_id, current_status = reservation


            # Slot boşsa ya da daha önce iptal edildiyse kullanıcı rezervasyonu direkt alabilir.
            if current_status in ("empty", "cancelled"):
                update_query = """
                    UPDATE reservations
                    SET user_id = %s,
                        status = %s
                    WHERE reservation_id = %s
                """
                self.cursor.execute(update_query, (user_id, "reserved", reservation_id))
                self.db.commit()
                return "Rezervasyon başarıyla oluşturuldu."


            # Buraya geldiysek rezervasyon hali hazırda doludur.
            # Mevcut rezervasyon sahibinin rolünü çekiyor
            current_user_query = "SELECT role FROM users WHERE user_id = %s"
            self.cursor.execute(current_user_query, (current_user_id,))
            current_user = self.cursor.fetchone()

            if current_user is None:
                self.db.rollback()
                return "Mevcut rezervasyon sahibinin kullanıcı bilgisi bulunamadı."

            current_user_role = current_user[0]


            # Yeni kullanıcının rolü daha büyükse override yapabilir.
            if requester_role > current_user_role:
                override_query = """
                    UPDATE reservations
                    SET user_id = %s,
                        status = %s
                    WHERE reservation_id = %s
                """
                
                self.cursor.execute(override_query, (user_id, "reserved", reservation_id))
                
                
                # Eski rezervasyon sahibini haberdar etmek için notify tablosuna kayıt eklenir.
                self.notify_cancellation(current_user_id, reservation_id)
                
                
                self.db.commit()
                return "Rezervasyon override edilerek kullanıcıya verildi. Eski kullanıcı için bildirim kaydı oluşturuldu."

            self.db.rollback()
            return "Bu rezervasyon daha yüksek veya eşit öncelikli bir kullanıcıda olduğu için alınamaz."

        except psycopg.Error as err:
            self.db.rollback()
            print(f"Rezervasyon işlemi sırasında veritabanı hatası oluştu. Hata mesajı: {err}")
            traceback.print_exc()
            return "Rezervasyon işlemi sırasında hata oluştu."

        except Exception as e:
            self.db.rollback()
            print(f"İşlem sırasında beklenmeyen bir hata oluştu. Hata mesajı: {e}")
            traceback.print_exc()
            return "Beklenmeyen bir hata oluştu."



    """Override edilen kullanıcı için notify tablosuna kayıt ekler."""
    """Burada notify adında yeni bir database tablosuna ihtiyaç duyacağız."""
    """Dokümanlarda database tabloları kısmına bu tablo da eklenecek."""
    def notify_cancellation(self, user_id, reservation_id):
        try:
            query = """
                INSERT INTO notify (user_id, reservation_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """
            self.cursor.execute(query, (user_id, reservation_id))
            return self.cursor.rowcount > 0

        except psycopg.Error as err:
            print(f"İptal bildirimi eklenirken hata oluştu: {err}")
            traceback.print_exc()
            raise




    """Veritabanından reservation_id ile belirtilmiş rezervasyonu döndürür."""
    def get_reservation_info(self, reservation_id):
        try:
            with self.db.cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute("""
                    SELECT reservation_id, user_id, facility_id,
                           date, start_time, end_time, status
                    FROM reservations
                    WHERE reservation_id = %s
                """, (reservation_id,))
                return cur.fetchone()

        except psycopg.Error as err:
            print(f"Hata: {err}")
            traceback.print_exc()
            return None


    """Kullanıcıya ait bildirimleri döndürür ve notify tablosundan siler."""
    """Login olduğunda override edilen randevuların kullanıcıya görünmesi için bu fonksiyon kullanılıyor."""
    def bring_notifications(self, user_id):
        try:
            # Login yapan kullanıcıya ait notify kayıtlarını alıyoruz.
            query = """
                SELECT
                    n.reservation_id,
                    r.facility_id,
                    r.date,
                    r.start_time,
                    r.end_time,
                    r.status,
                    r.user_id AS overrider_user_id,
                    u.username AS overrider_username
                FROM notify n
                JOIN reservations r
                    ON n.reservation_id = r.reservation_id
                LEFT JOIN users u
                    ON r.user_id = u.user_id
                WHERE n.user_id = %s
                ORDER BY r.date DESC, r.start_time DESC
            """
            self.cursor.execute(query, (user_id,))
            notifications = self.cursor.fetchall()


            # Bildirimleri okuduktan sonra notify tablosundan siliyoruz.
            # Yeniden login yaptığımız zaman geçmişte override edilmiş randevular silindiği için bir daha yeniden gözükmüyor.
            delete_query = "DELETE FROM notify WHERE user_id = %s"
            self.cursor.execute(delete_query, (user_id,))
            self.db.commit()

            return notifications

        except psycopg.Error as err:
            self.db.rollback()
            print(f"Bildirimler getirilirken hata oluştu: {err}")
            traceback.print_exc()
            return []

        except Exception as e:
            self.db.rollback()
            print(f"Beklenmeyen bir hata oluştu: {e}")
            traceback.print_exc()
            return []


    """Uygun facility ID'ye sahip rezervasyon sistemde mevcut mu diye bakıyoruz."""
    def find_reservation_slot(self, facility_id, date, start_time, end_time):
        try:
            query = """
                SELECT reservation_id
                FROM reservations
                WHERE facility_id = %s
                  AND date = %s::date
                  AND start_time = %s::time
                  AND end_time = %s::time
                LIMIT 1
            """
            self.cursor.execute(query, (facility_id, date, start_time, end_time))
            row = self.cursor.fetchone()

            if row is None:
                return None
            return row[0]

        except psycopg.Error as err:
            print(f"Reservation slot aranırken hata oluştu: {err}")
            traceback.print_exc()
            return None
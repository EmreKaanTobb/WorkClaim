import psycopg
import traceback
import time
from datetime import datetime


'''Bu kodu veritabanında tarihi geçmiş randevuları otomatik olarak silmek için kullanıyoruz.'''
'''Bu haliyle 30 dakikada bir veritabanından zamanı geçmiş randevuları kaldırıyoruz.'''
def cleanup_expired_reservations():
    conn = None
    cursor = None

    try:
        conn = psycopg.connect(
            host="127.0.0.1",
            user="postgres",
            password="workclaim123",
            dbname="workclaim",
            port=5432
        )
        cursor = conn.cursor()

        delete_query = """
            DELETE FROM reservations
            WHERE (date, end_time) <= (%s::date, %s::time)
        """

        now = datetime.now()
        cursor.execute(delete_query, (now.date(), now.time()))
        deleted_count = cursor.rowcount
        conn.commit()

        print(f"[{now}] {deleted_count} adet tarihi geçmiş rezervasyon silindi.")

    except psycopg.Error as err:
        if conn:
            conn.rollback()
        print(f"Veritabanı hatası oluştu: {err}")
        traceback.print_exc()

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Beklenmeyen hata oluştu: {e}")
        traceback.print_exc()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def run_periodic_cleanup():
    print("Tarihi geçmiş rezervasyon temizleme servisi başlatıldı.")

    '''Bu kısımdan veritabanı check işlemini kısaltabiliriz veya uzatabiliriz.'''
    '''Ctrl 'C yapılmadığı sürece bu kod arka planda çalışacak.'''
    while True:
        cleanup_expired_reservations()
        print("Bir sonraki temizlik 30 dakika sonra çalışacak.\n")
        time.sleep(30 * 60)  # 30 dakika


if __name__ == "__main__":
    run_periodic_cleanup()
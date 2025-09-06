
import threading
import time
import requests

print('Target domain:')
TARGET = input()
THREADS = 1000       # 동시 스레드 수 (과도하게 높이지 말 것)
RPS_PER_THREAD = 100   # 스레드당 초당 1요청 => 총 RPS = THREADS * RPS_PER_THREAD
DURATION_SEC = 3000     # 테스트 최대 5분

def worker(tid):
    interval = 1.0 / RPS_PER_THREAD
    end = time.time() + DURATION_SEC
    while time.time() < end:
        start = time.time()
        try:
            r = requests.get(TARGET, timeout=3)
            print(f"[T{tid}] {r.status_code} {r.elapsed.total_seconds():.3f}s")
        except Exception as e:
            print(f"[T{tid}] ERR {e}")
        # RPS 유지 (sleep로 간격 확보)
        elapsed = time.time() - start
        to_sleep = max(0, interval - elapsed)
        time.sleep(to_sleep)

def main():
    threads = []
    for i in range(THREADS):
        t = threading.Thread(target=worker, args=(i,), daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
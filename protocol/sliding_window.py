import time
import random

def run_sliding_window(file_data, loss_rate, latency, window_size, progress_callback):
    chunks = [file_data[i:i+1024] for i in range(0, len(file_data), 1024)]
    total = len(chunks)
    base = 0
    next_seq_num = 0
    retransmissions = 0
    
    while base < total:
        # 1. BÜTÜN PƏNCƏRƏNİ BİRDƏN GÖNDƏR (Heç bir gözləmə olmadan)
        while next_seq_num < base + window_size and next_seq_num < total:
            next_seq_num += 1
        
        # 2. Şəbəkə gecikməsini (Latency) pəncərə başına cəmi 1 dəfə tətbiq et
        if latency > 0:
            time.sleep(latency / 1000) 

        # 3. ACK simulyasiyası
        if random.random() * 100 > loss_rate:
            # Uğurlu halda bazanı pəncərə qədər sürüşdür (Sürət üçün)
            old_base = base
            base = next_seq_num 
            # Qrafiki pəncərə bitəndə 1 dəfə yeniləyirik (Bu proqramı çox sürətləndirir)
            progress_callback(base, total, f"Packets {old_base}-{base-1} ACKed", False)
        else:
            # İtki varsa başa qayıt
            retransmissions += 1
            next_seq_num = base 
            progress_callback(base, total, "Loss detected! Retransmitting window...", True)
            
    return retransmissions
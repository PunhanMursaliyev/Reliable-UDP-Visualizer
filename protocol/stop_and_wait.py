import time
from protocol.core import Packet, network_layer_send

def run_stop_and_wait(file_data, loss_rate, latency, progress_callback):
    """
    Nağızadə Elşən müəllimin istədiyi Stop-and-Wait protokolu.
    """
    # Faylı 1024 baytlıq hissələrə bölürük (Chunking)
    chunks = [file_data[i:i+1024] for i in range(0, len(file_data), 1024)]
    total = len(chunks)
    retransmissions = 0
    
    for i, chunk in enumerate(chunks):
        packet = Packet(i, chunk).pack()
        acked = False
        
        while not acked:
            # Paketi göndəririk (İtki və gecikmə simulyasiyası ilə)
            success = network_layer_send(packet, loss_rate, latency)
            
            if success:
                # Paket uğurla çatdısa, ACK gəldiyini fərz edirik
                progress_callback(i + 1, total, f"Paket {i} uğurla göndərildi və ACK alındı.", False)
                acked = True
            else:
                # Paket itdisə (Loss)
                retransmissions += 1
                progress_callback(i, total, f"Paket {i} İTDİ! Yenidən göndərilir...", True)
                time.sleep(0.1) # Timeout gözləməsi
                
    return retransmissions
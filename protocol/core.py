import struct
import random
import time

class Packet:
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data

    def pack(self):
        # 'I' unsigned int (4 byte) ardıcıllıq nömrəsi üçün istifadə olunur
        return struct.pack('I', self.seq_num) + self.data

    @staticmethod
    def unpack(binary_data):
        if len(binary_data) < 4: return None, None
        seq_num = struct.unpack('I', binary_data[:4])[0]
        data = binary_data[4:]
        return seq_num, data

def network_layer_send(packet_bytes, loss_rate, latency):
    """Süni itki və gecikmə tətbiq edən funksiya"""
    if random.random() < (loss_rate / 100):
        return False # Paket itdi (simulyasiya)
    
    if latency > 0:
        time.sleep(latency / 1000) # Gecikməni saniyəyə çeviririk
        
    return True # Paket uğurla göndərildi
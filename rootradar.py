import os
import glob
import time

# Renkler
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def print_banner():
    print(f"""{CYAN}
    ____  ____  ____  ______   ____  ___    ____  ___    ____ 
   / __ \/ __ \/ __ \/_  __/  / __ \/   |  / __ \/   |  / __ \\
  / /_/ / / / / / / / / /    / /_/ / /| | / / / / /| | / /_/ /
 / _, _/ /_/ / /_/ / / /    / _, _/ ___ |/ /_/ / ___ |/ _, _/ 
/_/ |_|\____/\____/ /_/    /_/ |_/_/  |_/_____/_/  |_/_/ |_|  
    Linux Persistence Scanner v1.0
    {RESET}""")

def check_bashrc():
    print(f"{YELLOW}[*] Kullanıcı başlangıç dosyaları (.bashrc / .profile) taranıyor...{RESET}")
    home_dir = os.path.expanduser("~")
    
    # Taranacak potansiyel dosyalar
    targets = [".bashrc", ".bash_profile", ".zshrc", ".profile"]
    
    found_suspicious = False
    
    for target in targets:
        path = os.path.join(home_dir, target)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    lines = f.readlines()
                    # Genellikle sona eklenir, son 10 satırı kontrol et
                    last_lines = lines[-10:] if len(lines) > 10 else lines
                    
                    for i, line in enumerate(last_lines):
                        # Şüpheli anahtar kelimeler (Eğitim amaçlı basit imzalar)
                        suspicious_keywords = ["python", "bash -i", "nc -e", "/tmp/", "curl", "wget"]
                        for keyword in suspicious_keywords:
                            if keyword in line and not line.strip().startswith("#"):
                                print(f"{RED}[!] ŞÜPHELİ SATIR BULUNDU ({target}): {line.strip()}{RESET}")
                                found_suspicious = True
            except Exception as e:
                print(f"[!] Dosya okunamadı {path}: {e}")

    if not found_suspicious:
        print(f"{GREEN}[+] Başlangıç dosyaları temiz görünüyor.{RESET}")

def check_systemd():
    print(f"\n{YELLOW}[*] Systemd servisleri taranıyor...{RESET}")
    # Servis dosyalarının olduğu dizin
    service_path = "/etc/systemd/system/"
    
    if not os.access(service_path, os.R_OK):
        print(f"{RED}[!] Erişim Hatası: Servisleri taramak için ROOT yetkisi gerekir.{RESET}")
        return

    services = glob.glob(os.path.join(service_path, "*.service"))
    suspicious_count = 0

    for service in services:
        try:
            # Son 24 saatte değiştirilmiş servisleri bul
            file_stats = os.stat(service)
            mod_time = file_stats.st_mtime
            current_time = time.time()
            
            # 1 gün = 86400 saniye
            if (current_time - mod_time) < 86400:
                print(f"{RED}[!] DİKKAT: Son 24 saatte değiştirilmiş servis: {service}{RESET}")
                
                # İçeriğini oku ve ExecStart'ı kontrol et
                with open(service, "r") as f:
                    content = f.read()
                    if "/tmp/" in content or "/home/" in content:
                        print(f"    -> {RED}Şüpheli yol içeriyor (ExecStart){RESET}")
                suspicious_count += 1
        except Exception:
            pass
            
    if suspicious_count == 0:
        print(f"{GREEN}[+] Son 24 saatte değiştirilen servis bulunamadı.{RESET}")

def check_cron():
    print(f"\n{YELLOW}[*] Cron (Zamanlanmış Görevler) taranıyor...{RESET}")
    # Kullanıcının crontab'ını kontrol et
    try:
        # os.popen ile crontab çıktısını al
        cron_output = os.popen("crontab -l 2>/dev/null").read()
        if cron_output:
            print(f"{RED}[!] Kullanıcı Crontab'ında aktif görevler var:{RESET}")
            print(cron_output)
        else:
            print(f"{GREEN}[+] Kullanıcı Crontab'ı boş.{RESET}")
    except Exception as e:
        print(f"[!] Cron kontrol hatası: {e}")

    # Sistem geneli cron dosyaları
    system_cron = glob.glob("/etc/cron.*/*")
    # Burada detaylı analiz yapılabilir ama şimdilik sadece varlıklarını belirtiyoruz
    # print(f"[*] Sistem cron dizinlerinde {len(system_cron)} dosya var.")

def main():
    print_banner()
    check_bashrc()
    check_systemd()
    check_cron()
    print(f"\n{CYAN}[*] Tarama Tamamlandı.{RESET}")

if __name__ == "__main__":
    main()

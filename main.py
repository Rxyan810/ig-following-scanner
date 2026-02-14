#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IG Following Gender Detector 🔥🥵⚡
"""

import instaloader
import pandas as pd
import time
import random
import os
import sys
from datetime import datetime

# Tambahin path biar bisa import config dari folder atas
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============= BANNER =============
BANNER = """
\033[1;31m
┌─────────────────────────────────────┐
│     IG FOLLOWING SCANNER v2.1       │
│         GITHUB EDITION 🔥           │
│         BY: TUAN RAGIL 🥵⚡         │
└─────────────────────────────────────┘
\033[0m
"""

# ============= MAIN CLASS =============
class IGFollowingScanner:
    def __init__(self, username, password, target, limit=300):
        self.username = username
        self.password = password
        self.target = target
        self.limit = limit
        self.L = None
        self.follow_list = []
        
    def setup_loader(self, use_proxy=False, proxy_http=None, proxy_https=None):
        """Inisialisasi Instaloader"""
        self.L = instaloader.Instaloader(
            max_connection_attempts=10,
            request_timeout=180,
            sleep=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        if use_proxy and proxy_http and proxy_https:
            os.environ['HTTP_PROXY'] = proxy_http
            os.environ['HTTPS_PROXY'] = proxy_https
            print("[✓] Proxy diaktifkan")
    
    def login(self):
        """Login ke Instagram"""
        try:
            print(f"[•] Login sebagai {self.username}...")
            self.L.login(self.username, self.password)
            print("[✓] Login berhasil! 🔥")
            return True
        except instaloader.exceptions.BadCredentialsException:
            print("\n❌ LOGIN GAGAL! Cek username/password lu!")
            return False
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            print("\n❌ AKUN LU PAKE 2FA! Matiin dulu atau pake akun dummy!")
            return False
        except Exception as e:
            print(f"\n❌ Login error: {e}")
            return False
    
    def scrape_following(self):
        """Ambil data following target"""
        try:
            print(f"[•] Ambil data profil @{self.target}...")
            profile = instaloader.Profile.from_username(self.L.context, self.target)
            total_following = profile.followees
            print(f"[!] Total following: {total_following} akun")
            
            # Tentukan batas ambil
            actual_limit = self.limit if self.limit > 0 else total_following
            if actual_limit > total_following:
                actual_limit = total_following
                
            print(f"[!] Akan diambil: {actual_limit} akun")
            print("[!] Sabar, ini lagi scraping... 🥵\n")
            
            count = 0
            for followee in profile.get_followees():
                if count >= actual_limit:
                    break
                    
                count += 1
                print(f"[{count}/{actual_limit}] Processing: @{followee.username}...")
                
                # Ambil info dasar
                try:
                    user_info = {
                        'username': followee.username,
                        'full_name': followee.full_name,
                        'bio': followee.biography[:100] if hasattr(followee, 'biography') and followee.biography else "",
                        'follower_count': followee.followers if hasattr(followee, 'followers') else 0,
                        'following_count': followee.followees if hasattr(followee, 'followees') else 0,
                        'post_count': followee.mediacount if hasattr(followee, 'mediacount') else 0,
                        'is_private': followee.is_private if hasattr(followee, 'is_private') else False,
                        'is_verified': followee.is_verified if hasattr(followee, 'is_verified') else False,
                        'external_url': 'yes' if hasattr(followee, 'external_url') and followee.external_url else 'no'
                    }
                    
                    self.follow_list.append(user_info)
                except Exception as e:
                    print(f"  ⚠️ Error ambil data: {str(e)[:50]}")
                    # Tetap simpan data minimal
                    self.follow_list.append({
                        'username': followee.username,
                        'full_name': followee.full_name,
                        'bio': "",
                        'follower_count': 0,
                        'following_count': 0,
                        'post_count': 0,
                        'is_private': True,
                        'is_verified': False,
                        'external_url': 'no'
                    })
                
                # Delay biar gak kena rate limit
                time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))
            
            print(f"\n[✓] Selesai! Mendapatkan {len(self.follow_list)} following! 🔥")
            return True
            
        except instaloader.exceptions.ProfileNotExistsException:
            print(f"\n❌ Profil @{self.target} gak ada! Salah ketik?")
            return False
        except instaloader.exceptions.PrivateProfileNotFollowedException:
            print(f"\n❌ Profil @{self.target} private dan lu gak di-follow balik!")
            return False
        except Exception as e:
            print(f"\n❌ Scrape error: {e}")
            return False
    
    def analyze_gender(self):
        """Analisis gender"""
        print("\n[⚡] MENGANALISIS KANDUNGAN CEWE...")
        
        results = []
        for user in self.follow_list:
            score = 0
            reasons = []
            
            full_name = user['full_name'].lower()
            username = user['username'].lower()
            bio = user['bio'].lower()
            
            # Deteksi cewe
            if any(x in full_name for x in ['putri', 'dewi', 'ayu', 'sari', 'wati', 'ningsih', 
                                           'indah', 'cindy', 'jessica', 'angel', 'natasha']):
                score += 3
                reasons.append("Nama feminin")
            
            if any(x in username for x in ['putri', 'dewi', 'ayu', 'sari', 'cindy', 'jess', 
                                          'angel', 'princess', 'queen', 'sweet', 'beauty']):
                score += 3
                reasons.append("Username feminin")
            
            if any(x in bio for x in ['👸', '👑', '🌸', '🌺', '💅', '💄', '👗', '👠', 
                                     '💕', '💖', '🎀', '✨', '🦋']):
                score += 2
                reasons.append("Emoji feminin")
            
            if any(x in bio for x in ['makeup', 'fashion', 'beauty', 'skincare', 'mommy', 
                                     'bunda', 'perempuan', 'wanita', 'girl', 'woman']):
                score += 3
                reasons.append("Kata feminin")
            
            if user['follower_count'] > 500 and user['following_count'] < 300:
                score += 1
                reasons.append("Ratio follower/following khas cewe populer")
            
            if user['is_private']:
                score += 1
                reasons.append("Akun private")
            
            if user['is_verified']:
                score += 1
                reasons.append("Akun verified")
            
            if user['external_url'] == 'yes':
                score += 1
                reasons.append("Ada link di bio")
            
            # Filter cowo
            if any(x in full_name for x in ['muhammad', 'ahmad', 'rizky', 'fajar', 'pratama',
                                           'maulana', 'firmansyah', 'hidayat', 'abdul', 'budi',
                                           'agus', 'toni', 'heru', 'joko', 'eko', 'yanto']):
                score = 0
                reasons = ["🔴 TERDETEKSI COWO"]
            elif any(x in username for x in ['official', 'store', 'toko', 'shop', 'corp',
                                            'company', 'fc', 'club', 'team']):
                score = 0
                reasons = ["🔴 AKUN BISNIS/ORGANISASI"]
            
            results.append({
                'username': user['username'],
                'full_name': user['full_name'],
                'score_cewe': score,
                'reasons': ', '.join(reasons) if reasons else 'Tidak terdeteksi',
                'bio': user['bio'][:100],
                'is_private': user['is_private'],
                'followers': user['follower_count'],
                'following': user['following_count'],
                'posts': user['post_count']
            })
        
        return pd.DataFrame(results)
    
    def save_report(self, df):
        """Simpan hasil ke Excel"""
        # Filter berdasarkan skor
        kemungkinan_cewe = df[df['score_cewe'] >= 4].sort_values('score_cewe', ascending=False)
        kemungkinan_cowo = df[df['score_cewe'] == 0].sort_values('score_cewe', ascending=False)
        abu_abu = df[(df['score_cewe'] > 0) & (df['score_cewe'] < 4)]
        
        # Buat folder outputs kalo belum ada
        os.makedirs('outputs', exist_ok=True)
        
        # Nama file dengan timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"outputs/following_analysis_{self.target}_{timestamp}.xlsx"
        
        try:
            # Simpan ke Excel
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                kemungkinan_cewe.to_excel(writer, sheet_name='Kemungkinan_Cewe', index=False)
                kemungkinan_cowo.to_excel(writer, sheet_name='Kemungkinan_Cowo', index=False)
                abu_abu.to_excel(writer, sheet_name='Abu_Abu_Cek_Manual', index=False)
                df.to_excel(writer, sheet_name='Semua_Data', index=False)
            
            print(f"\n✅ LAPORAN DISIMPAN: {filename} 🔥🥵")
        except Exception as e:
            print(f"\n❌ Gagal simpan Excel: {e}")
            # Fallback ke CSV
            csv_file = filename.replace('.xlsx', '.csv')
            df.to_csv(csv_file, index=False)
            print(f"✅ Disimpan sebagai CSV: {csv_file}")
        
        # Tampilkan ringkasan
        print("\n" + "="*70)
        print("🔥 RINGKASAN HASIL 🔥")
        print("="*70)
        print(f"🎯 Target: @{self.target}")
        print(f"📊 Total dianalisis: {len(df)} akun")
        print(f"💃 Kemungkinan CEWE (skor ≥4): {len(kemungkinan_cewe)}")
        print(f"🧑 Kemungkinan COWO (skor 0): {len(kemungkinan_cowo)}")
        print(f"❓ Abu-abu (skor 1-3): {len(abu_abu)}")
        print("="*70)
        
        return filename

def main():
    """Main function"""
    # Import config dari file
    try:
        import config
    except ImportError:
        print("\n❌ File config.py gak ditemukan!")
        print("➜ Buat dulu file config.py di folder utama!\n")
        return
    
    # Ambil konfigurasi
    USERNAME_ANDA = config.USERNAME_ANDA
    PASSWORD_ANDA = config.PASSWORD_ANDA
    TARGET_USERNAME = config.TARGET_USERNAME
    BATAS_FOLLOWING = config.BATAS_FOLLOWING
    USE_PROXY = config.USE_PROXY
    PROXY_HTTP = config.PROXY_HTTP
    PROXY_HTTPS = config.PROXY_HTTPS
    
    # Set delay global
    global DELAY_MIN, DELAY_MAX
    DELAY_MIN = config.DELAY_MIN
    DELAY_MAX = config.DELAY_MAX
    
    # Validasi config
    if USERNAME_ANDA == "isi_dengan_username_dummy_lu" or PASSWORD_ANDA == "isi_dengan_password_dummy_lu":
        print("\n❌ LU BELOM ISI KONFIGURASI, BANGSAT!")
        print("➜ Edit dulu file config.py pake data akun dummy lu!\n")
        return
    
    # Tampilkan banner
    print(BANNER)
    
    # Jalankan scanner
    scanner = IGFollowingScanner(USERNAME_ANDA, PASSWORD_ANDA, TARGET_USERNAME, BATAS_FOLLOWING)
    scanner.setup_loader(USE_PROXY, PROXY_HTTP, PROXY_HTTPS)
    
    if not scanner.login():
        return
    
    if not scanner.scrape_following():
        return
    
    df = scanner.analyze_gender()
    scanner.save_report(df)
    
    print("\n✨ Selesai! Cek folder outputs buat laporan lengkap! 🔥🥵\n")

# ============= JALANKAN PROGRAM =============
if __name__ == "__main__":
    # Set default delay
    DELAY_MIN = 1.5
    DELAY_MAX = 3.0
    main()
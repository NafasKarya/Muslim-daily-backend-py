import requests
from typing import Optional, List

# --- Import entitas dan interface dari domain layer ---
from src.domain.al_quran.entities import Surah, Ayah, SurahDetail, Tafsir, TafsirDetail
from src.domain.al_quran.repositories import AlQuranRepository

class EQuranRepository(AlQuranRepository):
    """
    Implementasi konkret dari AlQuranRepository yang mengambil data
    dari API publik https://equran.id/api/v2.
    """
    BASE_URL = "https://equran.id/api/v2"

    def get_all_surahs(self) -> Optional[List[Surah]]:
        """
        Mengambil daftar ringkas semua surah dari equran.id API.
        """
        print("[REPO-EQURAN] Mengambil daftar semua surah...")
        try:
            response = requests.get(f"{self.BASE_URL}/surat", timeout=20)
            response.raise_for_status()
            api_data = response.json()

            if api_data.get("code") != 200 or not api_data.get("data"):
                print("[REPO-EQURAN-ERROR] API tidak mengembalikan data surah yang valid.")
                return None

            surahs_list = []
            for surah_data in api_data["data"]:
                surah_entry = Surah(
                    number=surah_data["nomor"],
                    name=surah_data["nama"],
                    englishName=surah_data["namaLatin"],
                    englishNameTranslation=surah_data["arti"],
                    numberOfAyahs=surah_data["jumlahAyat"],
                    revelationType=surah_data["tempatTurun"].title()
                )
                surahs_list.append(surah_entry)
            
            print(f"[REPO-EQURAN] Berhasil mendapatkan {len(surahs_list)} surah.")
            return surahs_list

        except requests.RequestException as e:
            print(f"[REPO-EQURAN-ERROR] Gagal menghubungi equran.id API: {e}")
            return None
        except (KeyError, ValueError) as e:
            print(f"[REPO-EQURAN-ERROR] Gagal mem-parsing response daftar surah: {e}")
            return None

    def get_surah_by_number(self, surah_number: int) -> Optional[SurahDetail]:
        """
        Mengambil detail surah (termasuk terjemahan Indonesia) dari equran.id API.
        """
        print(f"[REPO-EQURAN] Mengambil detail untuk surah nomor {surah_number}...")
        try:
            url = f"{self.BASE_URL}/surat/{surah_number}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            api_data = response.json()

            if api_data.get("code") != 200 or not api_data.get("data"):
                print(f"[REPO-EQURAN-ERROR] API tidak mengembalikan data detail untuk surah {surah_number}.")
                return None

            surah_data = api_data["data"]
            ayahs_list = []
            for ayah_data in surah_data.get("ayat", []):
                ayah_entry = Ayah(
                    numberInSurah=ayah_data["nomorAyat"],
                    text=ayah_data["teksArab"],
                    translation=ayah_data["teksIndonesia"],
                    audio=ayah_data.get("audio", {}).get("05")
                )
                ayahs_list.append(ayah_entry)
                
            surah_detail_entry = SurahDetail(
                number=surah_data["nomor"],
                name=surah_data["nama"],
                englishName=surah_data["namaLatin"],
                englishNameTranslation=surah_data["arti"],
                numberOfAyahs=surah_data["jumlahAyat"],
                revelationType=surah_data["tempatTurun"].title(),
                ayahs=ayahs_list
            )
            
            print(f"[REPO-EQURAN] Berhasil mendapatkan detail surah {surah_number} dengan {len(ayahs_list)} ayat.")
            return surah_detail_entry

        except requests.RequestException as e:
            print(f"[REPO-EQURAN-ERROR] Gagal menghubungi equran.id API: {e}")
            return None
        except (KeyError, ValueError, IndexError) as e:
            print(f"[REPO-EQURAN-ERROR] Gagal mem-parsing response detail surah: {e}")
            return None

    def get_tafsir_by_surah_number(self, surah_number: int) -> Optional[TafsirDetail]:
        """
        Mengambil detail tafsir surah dari equran.id API.
        """
        print(f"[REPO-EQURAN] Mengambil tafsir untuk surah nomor {surah_number}...")
        try:
            url = f"{self.BASE_URL}/tafsir/{surah_number}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            api_data = response.json()

            if api_data.get("code") != 200 or not api_data.get("data"):
                print(f"[REPO-EQURAN-ERROR] API tidak mengembalikan data tafsir untuk surah {surah_number}.")
                return None

            data = api_data["data"]
            
            # Ubah setiap item di list 'tafsir' dari API menjadi objek entitas 'Tafsir'
            tafsir_list = [
                Tafsir(ayat=t["ayat"], teks=t["teks"]) 
                for t in data.get("tafsir", [])
            ]
            
            # Buat objek entitas TafsirDetail dengan data yang sudah di-parsing
            return TafsirDetail(
                nomor=data["nomor"],
                nama=data["nama"],
                namaLatin=data["namaLatin"],
                jumlahAyat=data["jumlahAyat"],
                tafsir=tafsir_list
            )
        except requests.RequestException as e:
            print(f"[REPO-EQURAN-ERROR] Gagal menghubungi API tafsir: {e}")
            return None
        except (KeyError, ValueError, IndexError) as e:
            print(f"[REPO-EQURAN-ERROR] Gagal mem-parsing response tafsir: {e}")
            return None

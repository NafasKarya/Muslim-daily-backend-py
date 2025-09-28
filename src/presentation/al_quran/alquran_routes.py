from fastapi import APIRouter, Depends, HTTPException
from typing import List

# --- Import service, entitas, dan dependency injector khusus Al-Quran ---
from src.application.al_quran.services import AlQuranService
from src.domain.al_quran.entities import Surah, SurahDetail, Ayah, TafsirDetail
from src.dependencies import get_quran_service

router = APIRouter()

@router.get("/surahs", response_model=List[Surah], summary="Dapatkan Daftar Semua Surah")
def get_all_surahs(
    service: AlQuranService = Depends(get_quran_service)
):
    """
    Mengambil daftar ringkas dari semua 114 surah dalam Al-Quran.
    
    Endpoint ini efisien untuk menampilkan halaman utama fitur Al-Quran.
    
    Contoh request: `GET /api/quran/surahs`
    """
    surahs_list = service.get_all_surahs()
    
    if not surahs_list:
        raise HTTPException(
            status_code=404, 
            detail="Daftar surah tidak dapat ditemukan atau gagal dimuat."
        )
    
    return surahs_list

@router.get("/surahs/{surah_number}", response_model=SurahDetail, summary="Dapatkan Detail Surah Berdasarkan Nomor")
def get_surah_detail(
    surah_number: int,
    service: AlQuranService = Depends(get_quran_service)
):
    """
    Mengambil detail lengkap dari satu surah berdasarkan nomornya,
    termasuk semua ayat dan informasinya.
    
    Gunakan endpoint ini ketika pengguna memilih salah satu surah dari daftar.
    
    Contoh request: `GET /api/quran/surahs/1` (Untuk Al-Fatihah)
    """
    surah_detail = service.get_surah_detail(surah_number=surah_number)
    
    if not surah_detail:
        raise HTTPException(
            status_code=404,
            detail=f"Surah dengan nomor {surah_number} tidak ditemukan. Nomor harus antara 1-114."
        )
        
    return surah_detail

@router.get("/surahs/{surah_number}/ayahs/{ayah_number}", response_model=Ayah, summary="Dapatkan Ayat Spesifik")
def get_specific_ayah(
    surah_number: int,
    ayah_number: int,
    service: AlQuranService = Depends(get_quran_service)
):
    """
    Mengambil data satu ayat spesifik dari sebuah surah.
    
    Contoh request: `GET /api/quran/surahs/2/ayahs/255` (Untuk Ayat Kursi)
    """
    ayah = service.get_specific_ayah(surah_number, ayah_number)
    
    if not ayah:
        raise HTTPException(
            status_code=404,
            detail=f"Ayat {ayah_number} tidak ditemukan di surah {surah_number}."
        )
    
    return ayah

@router.get("/tafsir/{surah_number}", response_model=TafsirDetail, summary="Dapatkan Tafsir Surah")
def get_tafsir(
    surah_number: int,
    service: AlQuranService = Depends(get_quran_service)
):
    """
    Mengambil data tafsir lengkap (Kemenag) untuk satu surah penuh.
    
    Contoh request: `GET /api/quran/tafsir/18` (Untuk Tafsir Surah Al-Kahf)
    """
    tafsir_detail = service.get_tafsir(surah_number)
    
    if not tafsir_detail:
        raise HTTPException(
            status_code=404,
            detail=f"Tafsir untuk surah {surah_number} tidak ditemukan."
        )
    
    return tafsir_detail

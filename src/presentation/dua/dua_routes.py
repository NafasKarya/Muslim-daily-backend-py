from fastapi import APIRouter, Depends, HTTPException
from typing import List

# --- Import service, entitas, dan dependency injector khusus Dua ---
from src.application.dua.services import DuaService
from src.domain.dua.entities import Dua, DuaDetail
from src.dependencies import get_dua_service

router = APIRouter()

@router.get("/duas", response_model=List[Dua], summary="Dapatkan Daftar Semua Dua")
def get_all_duas(
    service: DuaService = Depends(get_dua_service)
):
    """
    Mengambil daftar ringkas dari semua doa.
    
    Endpoint ini efisien untuk menampilkan halaman utama fitur doa/dua.
    Contoh request: `GET /api/dua/duas`
    """
    duas_list = service.get_all_duas()
    
    if not duas_list:
        raise HTTPException(
            status_code=404, 
            detail="Daftar dua tidak dapat ditemukan atau gagal dimuat."
        )
    return duas_list

@router.get("/duas/{dua_id}", response_model=DuaDetail, summary="Dapatkan Detail Dua Berdasarkan ID")
def get_dua_detail(
    dua_id: int,
    service: DuaService = Depends(get_dua_service)
):
    """
    Mengambil detail lengkap dari satu doa berdasarkan ID-nya,
    termasuk semua versi teks dan informasinya.
    
    Contoh request: `GET /api/dua/duas/1`
    """
    dua_detail = service.get_dua_detail(dua_id=dua_id)
    
    if not dua_detail:
        raise HTTPException(
            status_code=404,
            detail=f"Dua dengan ID {dua_id} tidak ditemukan."
        )
    return dua_detail

@router.get("/duas/category/{category_id}", response_model=List[Dua], summary="Dapatkan Semua Dua Berdasarkan Kategori")
def get_duas_by_category(
    category_id: str,   # <--- Ubah jadi str, bukan int!
    service: DuaService = Depends(get_dua_service)
):
    """
    Mengambil semua dua berdasarkan kategori (pakai nama kategori, bukan ID numerik).
    Contoh request: `GET /api/dua/duas/category/Adab`
    """
    duas_list = service.get_duas_by_category(category_id=category_id)
    if not duas_list:
        raise HTTPException(
            status_code=404,
            detail=f"Tidak ditemukan dua untuk kategori '{category_id}'."
        )
    return duas_list

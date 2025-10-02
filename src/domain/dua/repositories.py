# src/domain/dua/repositories.py

from abc import ABC, abstractmethod
from typing import Optional, List

# --- Path import baru, spesifik untuk entitas Dua ---
from src.domain.dua.entities import Dua, DuaDetail

class DuaRepository(ABC):
    """
    Mendefinisikan kontrak (interface) untuk mendapatkan data doa/dua.

    Lapisan aplikasi (services) akan bergantung pada abstraksi ini,
    bukan pada implementasi konkret (misal: dari API mana data diambil).
    Ini memungkinkan kita untuk menukar sumber data di masa depan tanpa
    mengubah logika bisnis di service.
    """

    @abstractmethod
    def get_all_duas(self) -> Optional[List[Dua]]:
        """
        Mengambil daftar ringkas semua doa.
        """
        pass

    @abstractmethod
    def get_dua_by_id(self, dua_id: int) -> Optional[DuaDetail]:
        """
        Mengambil detail lengkap sebuah doa berdasarkan ID-nya,
        termasuk semua versi teks di dalamnya.
        """
        pass

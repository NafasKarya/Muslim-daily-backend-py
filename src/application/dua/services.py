from typing import Optional, List

# --- Import dari domain dua ---
from src.domain.dua.entities import Dua, DuaDetail
from src.domain.dua.repositories import DuaRepository

class DuaService:
    """
    Application service yang mengatur use case terkait doa/dua.
    """

    def __init__(self, repository: DuaRepository):
        self._repository = repository

    def get_all_duas(self) -> Optional[List[Dua]]:
        """
        Use case: Mendapatkan daftar semua doa.
        """
        return self._repository.get_all_duas()

    def get_dua_detail(self, dua_id: int) -> Optional[DuaDetail]:
        """
        Use case: Mendapatkan detail sebuah doa berdasarkan ID-nya.

        Args:
            dua_id (int): ID doa.

        Returns:
            Optional[DuaDetail]: Objek detail doa jika ditemukan, jika tidak None.
        """
        return self._repository.get_dua_by_id(dua_id)

    def get_duas_by_category(self, category_id: int) -> Optional[List[Dua]]:
        """
        Use case: Mendapatkan semua doa pada kategori tertentu.

        Args:
            category_id (int): ID kategori.

        Returns:
            Optional[List[Dua]]: List doa sesuai kategori, None kalau tidak ada.
        """
        return self._repository.get_duas_by_category(category_id)

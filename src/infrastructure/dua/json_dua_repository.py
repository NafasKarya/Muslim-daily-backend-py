import os
import json
from typing import Optional, List

# --- Import entitas dan interface dari domain layer ---
from src.domain.dua.entities import Dua, DuaDetail, DuaText
from src.domain.dua.repositories import DuaRepository

class JSONDuaRepository(DuaRepository):
    """
    Implementasi konkret dari DuaRepository yang mengambil data
    dari file JSON lokal: src/infrastructure/dua/data/dua.json.
    """

    DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "dua.json")

    def _load_data(self):
        print(f"[REPO-DUA] Membaca file JSON data dua di: {self.DATA_PATH}")
        try:
            with open(self.DATA_PATH, encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"[REPO-DUA-ERROR] Gagal membaca file {self.DATA_PATH}: {e}")
            return None

    def get_all_duas(self) -> Optional[List[Dua]]:
        """
        Mengambil daftar ringkas semua doa dari file JSON.
        """
        data = self._load_data()
        if not data:
            return None

        try:
            dua_list = []
            for dua_data in data.get("duas", []):
                dua = Dua(
                    id=dua_data["id"],
                    title=dua_data["title"],
                    category=dua_data.get("category", ""),
                    reference=dua_data.get("reference")
                )
                dua_list.append(dua)
            print(f"[REPO-DUA] Berhasil dapat {len(dua_list)} dua.")
            return dua_list
        except (KeyError, ValueError) as e:
            print(f"[REPO-DUA-ERROR] Gagal parsing daftar dua: {e}")
            return None

    def get_dua_by_id(self, dua_id: int) -> Optional[DuaDetail]:
        """
        Mengambil detail lengkap sebuah doa berdasarkan ID dari file JSON.
        """
        data = self._load_data()
        if not data:
            return None

        try:
            for dua_data in data.get("duas", []):
                if dua_data["id"] == dua_id:
                    # --- Convert texts ke list of DuaText (biar ga warning pydantic) ---
                    texts = [
                        DuaText(
                            language=text_item["language"],
                            text=text_item["text"]
                        )
                        for text_item in dua_data.get("texts", [])
                    ]
                    return DuaDetail(
                        id=dua_data["id"],
                        title=dua_data["title"],
                        category=dua_data.get("category", ""),
                        reference=dua_data.get("reference"),
                        texts=texts,
                        hikmah=dua_data.get("hikmah") if "hikmah" in dua_data else None,
                        inspirasi=dua_data.get("inspirasi") if "inspirasi" in dua_data else None  # <-- GANTI jadi inspirasi
                    )
            print(f"[REPO-DUA] Dua ID {dua_id} tidak ditemukan.")
            return None
        except (KeyError, ValueError) as e:
            print(f"[REPO-DUA-ERROR] Gagal parsing detail dua: {e}")
            return None

    def get_duas_by_category(self, category_id: int) -> Optional[List[Dua]]:
        """
        Mengambil semua dua berdasarkan kategori (pakai nama kategori sebagai ID).
        Contoh: /duas/category/Adab
        """
        data = self._load_data()
        if not data:
            return None

        try:
            category_name = str(category_id)
            dua_list = []
            for dua_data in data.get("duas", []):
                if dua_data.get("category", "").lower() == category_name.lower():
                    dua = Dua(
                        id=dua_data["id"],
                        title=dua_data["title"],
                        category=dua_data.get("category", ""),
                        reference=dua_data.get("reference")
                    )
                    dua_list.append(dua)
            return dua_list if dua_list else None
        except Exception as e:
            print(f"[REPO-DUA-ERROR] Gagal filter kategori: {e}")
            return None

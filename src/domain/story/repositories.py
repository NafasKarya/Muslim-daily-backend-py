from abc import ABC, abstractmethod
from typing import Optional, List

# --- Import entitas Story yang baru ---
from src.domain.story.entities import (
    Story,
    StoryDetail,
)

class StoryRepository(ABC):
    """
    Mendefinisikan kontrak (interface) untuk mendapatkan data story dari kitab klasik/fantasi/mitos.

    Lapisan aplikasi (services) akan bergantung pada abstraksi ini,
    bukan pada implementasi konkret (API, DB, JSON, dst).
    """

    @abstractmethod
    def get_all_stories(self) -> Optional[List[Story]]:
        """
        Mengambil daftar ringkasan semua story.
        """
        pass

    @abstractmethod
    def get_story_by_id(self, story_id: int) -> Optional[StoryDetail]:
        """
        Mengambil detail lengkap story berdasarkan ID.
        """
        pass

    @abstractmethod
    def get_stories_by_kitab(self, kitab_id: int) -> Optional[List[Story]]:
        """
        Mengambil semua story dari kitab tertentu (misal: Qazwini, Al-Mas'udi, dst).
        """
        pass

    @abstractmethod
    def get_stories_by_category(self, category_id: int) -> Optional[List[Story]]:
        """
        Mengambil semua story berdasarkan kategori tertentu (fantasi, misteri, perang, dll).
        """
        pass

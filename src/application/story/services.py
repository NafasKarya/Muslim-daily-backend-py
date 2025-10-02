from typing import Optional, List

# --- Import dari domain stories ---
from src.domain.story.entities import Story, StoryDetail
from src.domain.story.repositories import StoryRepository

class StoryService:
    """
    Application service untuk use case terkait story dari kitab klasik/fantasi/mitos.
    """

    def __init__(self, repository: StoryRepository):
        self._repository = repository

    def get_all_stories(self) -> Optional[List[Story]]:
        """
        Use case: Mendapatkan daftar semua cerita dari kitab klasik.

        Returns:
            Optional[List[Story]]: Daftar story, None kalau kosong.
        """
        return self._repository.get_all_stories()

    def get_story_detail(self, story_id: int) -> Optional[StoryDetail]:
        """
        Use case: Mendapatkan detail story berdasarkan ID.

        Args:
            story_id (int): ID story.

        Returns:
            Optional[StoryDetail]: Objek detail cerita, None kalau tidak ditemukan.
        """
        return self._repository.get_story_by_id(story_id)

    def get_stories_by_kitab(self, kitab_id: int) -> Optional[List[Story]]:
        """
        Use case: Mendapatkan semua story dari kitab tertentu (misal: Qazwini, Al-Dimashqi, dll).

        Args:
            kitab_id (int): Nama atau ID kitab (pakai str lebih aman).

        Returns:
            Optional[List[Story]]: List story dari kitab tsb, None kalau gak ada.
        """
        return self._repository.get_stories_by_kitab(kitab_id)

    def get_stories_by_category(self, category_id: int) -> Optional[List[Story]]:
        """
        Use case: Mendapatkan story berdasarkan kategori tertentu
        (misal: makhluk aneh, misteri laut, perang, dsb).

        Args:
            category_id (int): Nama atau ID kategori (pakai str lebih aman).

        Returns:
            Optional[List[Story]]: List story per kategori, None kalau gak ada.
        """
        return self._repository.get_stories_by_category(category_id)

import os
import json
from typing import Optional, List

# --- Import entitas dan interface dari domain layer ---
from src.domain.story.entities import Story, StoryDetail, StoryText
from src.domain.story.repositories import StoryRepository

class JSONStoryRepository(StoryRepository):
    """
    Implementasi konkret StoryRepository yang mengambil data
    dari file JSON lokal: src/infrastructure/story/data/story.json
    """

    DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "story.json")

    def _load_data(self):
        print(f"[REPO-STORY] Membaca file JSON data story di: {self.DATA_PATH}")
        try:
            with open(self.DATA_PATH, encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"[REPO-STORY-ERROR] Gagal membaca file {self.DATA_PATH}: {e}")
            return None

    def get_all_stories(self) -> Optional[List[Story]]:
        """
        Mengambil daftar ringkasan semua story dari file JSON.
        """
        data = self._load_data()
        if not data:
            return None

        try:
            stories = []
            # data bisa list (bukan dict), jadi akses langsung
            for story_data in data:
                story = Story(
                    id=story_data["id"],
                    title=story_data["title"],
                    kitab=story_data.get("kitab", ""),
                    category=story_data.get("category", ""),
                    reference=story_data.get("reference")
                )
                stories.append(story)
            print(f"[REPO-STORY] Berhasil dapat {len(stories)} story.")
            return stories
        except (KeyError, ValueError) as e:
            print(f"[REPO-STORY-ERROR] Gagal parsing daftar story: {e}")
            return None

    def get_story_by_id(self, story_id: int) -> Optional[StoryDetail]:
        """
        Mengambil detail lengkap sebuah story berdasarkan ID dari file JSON.
        """
        data = self._load_data()
        if not data:
            return None

        try:
            for story_data in data:
                if story_data["id"] == story_id:
                    texts = [
                        StoryText(
                            language=text_item["language"],
                            text=text_item["text"]
                        )
                        for text_item in story_data.get("texts", [])
                    ]
                    return StoryDetail(
                        id=story_data["id"],
                        title=story_data["title"],
                        kitab=story_data.get("kitab", ""),
                        category=story_data.get("category", ""),
                        reference=story_data.get("reference"),
                        texts=texts
                    )
            print(f"[REPO-STORY] Story ID {story_id} tidak ditemukan.")
            return None
        except (KeyError, ValueError) as e:
            print(f"[REPO-STORY-ERROR] Gagal parsing detail story: {e}")
            return None

    def get_stories_by_kitab(self, kitab_id: int) -> Optional[List[Story]]:
        """
        Mengambil semua story dari kitab tertentu (pakai nama kitab sebagai ID).
        """
        data = self._load_data()
        if not data:
            return None

        try:
            kitab_name = str(kitab_id)
            stories = []
            for story_data in data:
                if story_data.get("kitab", "").lower() == kitab_name.lower():
                    story = Story(
                        id=story_data["id"],
                        title=story_data["title"],
                        kitab=story_data.get("kitab", ""),
                        category=story_data.get("category", ""),
                        reference=story_data.get("reference")
                    )
                    stories.append(story)
            return stories if stories else None
        except Exception as e:
            print(f"[REPO-STORY-ERROR] Gagal filter kitab: {e}")
            return None

    def get_stories_by_category(self, category_id: int) -> Optional[List[Story]]:
        """
        Mengambil semua story berdasarkan kategori (pakai nama kategori sebagai ID).
        """
        data = self._load_data()
        if not data:
            return None

        try:
            category_name = str(category_id)
            stories = []
            for story_data in data:
                if story_data.get("category", "").lower() == category_name.lower():
                    story = Story(
                        id=story_data["id"],
                        title=story_data["title"],
                        kitab=story_data.get("kitab", ""),
                        category=story_data.get("category", ""),
                        reference=story_data.get("reference")
                    )
                    stories.append(story)
            return stories if stories else None
        except Exception as e:
            print(f"[REPO-STORY-ERROR] Gagal filter kategori: {e}")
            return None

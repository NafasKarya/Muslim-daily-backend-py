from fastapi import APIRouter, Depends, HTTPException
from typing import List

# --- Import service, entitas, dan dependency injector khusus Story ---
from src.application.story.services import StoryService
from src.domain.story.entities import Story, StoryDetail
from src.dependencies import get_story_service

router = APIRouter()

@router.get(
    "/stories",
    response_model=List[Story],
    summary="Dapatkan Daftar Semua Story"
)
def get_all_stories(
    service: StoryService = Depends(get_story_service)
):
    """
    Mengambil daftar ringkas dari semua story.
    Contoh request: `GET /api/story/stories`
    """
    stories = service.get_all_stories()
    if not stories:
        raise HTTPException(
            status_code=404,
            detail="Daftar stories tidak dapat ditemukan atau gagal dimuat."
        )
    return stories

@router.get(
    "/stories/{story_id}",
    response_model=StoryDetail,
    summary="Dapatkan Detail Story Berdasarkan ID"
)
def get_story_detail(
    story_id: int,
    service: StoryService = Depends(get_story_service)
):
    """
    Mengambil detail lengkap dari satu story berdasarkan ID.
    Contoh request: `GET /api/story/stories/1`
    """
    story_detail = service.get_story_detail(story_id=story_id)
    if not story_detail:
        raise HTTPException(
            status_code=404,
            detail=f"Story dengan ID {story_id} tidak ditemukan."
        )
    return story_detail

@router.get(
    "/stories/kitab/{kitab_id}",
    response_model=List[Story],
    summary="Dapatkan Semua Story Berdasarkan Nama Kitab"
)
def get_stories_by_kitab(
    kitab_id: str,   # Nama kitab, bukan int!
    service: StoryService = Depends(get_story_service)
):
    """
    Mengambil semua story berdasarkan nama kitab.
    Contoh request: `GET /api/story/stories/kitab/Ajaib%20al-Makhluqat`
    """
    stories = service.get_stories_by_kitab(kitab_id=kitab_id)
    if not stories:
        raise HTTPException(
            status_code=404,
            detail=f"Tidak ditemukan stories untuk kitab '{kitab_id}'."
        )
    return stories

@router.get(
    "/stories/category/{category_id}",
    response_model=List[Story],
    summary="Dapatkan Semua Story Berdasarkan Kategori"
)
def get_stories_by_category(
    category_id: str,   # Nama kategori
    service: StoryService = Depends(get_story_service)
):
    """
    Mengambil semua story berdasarkan kategori (fantasi, makhluk, dsb).
    Contoh request: `GET /api/story/stories/category/Makhluk%20Aneh`
    """
    stories = service.get_stories_by_category(category_id=category_id)
    if not stories:
        raise HTTPException(
            status_code=404,
            detail=f"Tidak ditemukan stories untuk kategori '{category_id}'."
        )
    return stories

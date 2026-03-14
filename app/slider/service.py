from prisma import Prisma
from typing import List, Optional
from .schemas import SliderCreate, SliderUpdate

async def create_slider(db: Prisma, data: SliderCreate):
    return await db.slider.create(
        data={
            "image_url": data.image_url,
            "title": data.title,
            "link_url": data.link_url,
            "is_active": data.is_active,
        }
    )

async def get_all_sliders(db: Prisma, active_only: bool = False):
    where = {}
    if active_only:
        where["is_active"] = True
    return await db.slider.find_many(where=where, order={"created_at": "desc"})

async def get_slider_by_id(db: Prisma, slider_id: int):
    return await db.slider.find_first(where={"id": slider_id})

async def update_slider(db: Prisma, slider_id: int, data: SliderUpdate):
    update_data = {k: v for k, v in data.dict(exclude_unset=True).items() if v is not None}
    return await db.slider.update(
        where={"id": slider_id},
        data=update_data
    )

async def delete_slider(db: Prisma, slider_id: int):
    return await db.slider.delete(where={"id": slider_id})

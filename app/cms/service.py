from app.db import db
from . import schemas

async def get_page_by_slug(slug: str):
    page = await db.cmspage.find_unique(where={"slug": slug})
    # If it doesn't exist, create a draft placeholder
    if not page:
        title = slug.replace("-", " ").title()
        page = await db.cmspage.create(
            data={
                "slug": slug,
                "title": title,
                "content": f"Default content for {title}"
            }
        )
    return page

async def update_page_content(slug: str, data: schemas.CmsPageUpdate):
    page = await db.cmspage.update(
        where={"slug": slug},
        data={"content": data.content}
    )
    return page

from typing import List
from app.db import db
from . import schemas
from fastapi import HTTPException, status

class ProductSectionService:
    async def get_home_sections(self) -> List[schemas.HomeSectionResponse]:
        sections = await db.productsection.find_many(
            where={"is_active": True},
            order={"order_index": "asc"},
            include={
                "products": {
                    "include": {
                        "product": {
                            "include": {
                                "variations": True,
                                "category": True
                            }
                        }
                    }
                }
            }
        )
        
        response = []
        for section in sections:
            # Sort by order_index and take 4 in Python as a workaround for nested query issues
            sorted_section_products = sorted(section.products, key=lambda x: x.order_index) if section.products else []
            products = [sp.product for sp in sorted_section_products if sp.product][:4]
            
            response.append({
                "id": section.id,
                "name": section.name,
                "products": products
            })
        return response

    async def get_all_sections(self):
        sections = await db.productsection.find_many(
            order={"order_index": "asc"},
            include={
                "products": {
                    "include": {
                        "product": {
                            "include": {
                                "variations": True,
                                "category": True
                            }
                        }
                    }
                }
            }
        )
        
        # Sort nested products in Python to avoid prisma FieldNotFoundError
        for section in sections:
            if section.products:
                section.products.sort(key=lambda x: x.order_index)
                
        return sections

    async def create_section(self, data: schemas.ProductSectionCreate):
        return await db.productsection.create(
            data={
                "name": data.name,
                "order_index": data.order_index,
                "is_active": data.is_active
            }
        )

    async def update_section(self, section_id: int, data: schemas.ProductSectionUpdate):
        update_data = data.dict(exclude_unset=True)
        return await db.productsection.update(
            where={"id": section_id},
            data=update_data
        )

    async def delete_section(self, section_id: int):
        await db.productsection.delete(where={"id": section_id})
        return {"message": "Section deleted"}

    async def assign_product_to_section(self, section_id: int, product_id: int, order_index: int = 0):
        return await db.sectionproduct.upsert(
            where={
                "section_id_product_id": {
                    "section_id": section_id,
                    "product_id": product_id
                }
            },
            data={
                "create": {
                    "section_id": section_id,
                    "product_id": product_id,
                    "order_index": order_index
                },
                "update": {
                    "order_index": order_index
                }
            }
        )

    async def remove_product_from_section(self, section_id: int, product_id: int):
        await db.sectionproduct.delete(
            where={
                "section_id_product_id": {
                    "section_id": section_id,
                    "product_id": product_id
                }
            }
        )
        return {"message": "Product removed from section"}

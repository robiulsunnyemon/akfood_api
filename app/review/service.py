from prisma import Prisma
from .schemas import ReviewCreate
from fastapi import HTTPException

async def create_review(db: Prisma, user_id: int, review_data: ReviewCreate):
    # Check if order exists and belongs to user
    order = await db.order.find_unique(
        where={"id": review_data.order_id},
        include={"review": True}
    )
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only review your own orders")
    
    if order.status != "DELIVERED":
        raise HTTPException(status_code=400, detail="You can only review delivered orders")
    
    if order.review:
        raise HTTPException(status_code=400, detail="You have already reviewed this order")
    
    # Create review
    new_review = await db.review.create(
        data={
            "user_id": user_id,
            "order_id": review_data.order_id,
            "rating": review_data.rating,
            "comment": review_data.comment
        }
    )

    # 3. Update Average Ratings for all items in the order
    order_items = await db.orderitem.find_many(where={"order_id": review_data.order_id})
    user_rating = float(review_data.rating)

    for item in order_items:
        if item.product_id:
            # Update Product Rating
            product = await db.product.find_unique(where={"id": item.product_id})
            if product:
                current_count = product.review_count
                current_avg = product.rating
                
                new_count = current_count + 1
                # Weight old rating by previous count, add new rating, divide by new count
                # If count is 0, old_avg (5.0) is ignored by multiplying with 0
                new_avg = ((current_avg * current_count) + user_rating) / new_count
                
                await db.product.update(
                    where={"id": item.product_id},
                    data={
                        "rating": new_avg,
                        "review_count": new_count
                    }
                )

        if item.party_menu_id:
            # Update PartyMenu Rating
            menu = await db.partymenu.find_unique(where={"id": item.party_menu_id})
            if menu:
                current_count = menu.review_count
                current_avg = menu.rating
                
                new_count = current_count + 1
                new_avg = ((current_avg * current_count) + user_rating) / new_count
                
                await db.partymenu.update(
                    where={"id": item.party_menu_id},
                    data={
                        "rating": new_avg,
                        "review_count": new_count
                    }
                )
    
    return new_review

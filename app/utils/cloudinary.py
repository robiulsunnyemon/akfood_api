import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Configure Cloudinary
if settings.cloudinary_cloud_name and settings.cloudinary_api_key and settings.cloudinary_api_secret:
    cloudinary.config(
        cloud_name=settings.cloudinary_cloud_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret
    )
else:
    logger.warning("Cloudinary config is missing in environment variables!")

async def upload_image(file: UploadFile, folder: str = "akfood/profiles") -> str:
    """
    Uploads an image to Cloudinary and returns the secure URL.
    Validates file type to ensure it's an image.
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="File provided is not an image."
        )
    
    try:
        # Cloudinary uploader doesn't strictly support async UploadFile reading out of the box
        # We read the file contents synchronously since it supports file objects
        contents = await file.read()
        
        result = cloudinary.uploader.upload(
            contents,
            folder=folder,
            resource_type="image",
            overwrite=True
        )
        
        # Return the secure URL from Cloudinary response
        return result.get("secure_url")
    
    except Exception as e:
        logger.error(f"Error uploading image to Cloudinary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not upload the image. Please try again later."
        )

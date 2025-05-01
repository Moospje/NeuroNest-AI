import os
import logging
import uuid
import shutil
import mimetypes
from typing import Dict, List, Any, Optional, BinaryIO, Union
from datetime import datetime
import aiofiles
from fastapi import UploadFile
import PyPDF2
from PIL import Image
import io
from app.core.config import settings
from app.models.file import FileInfo, FileAnalysisResult
from app.services.firebase_service import firebase_service

logger = logging.getLogger(__name__)

async def save_upload_file(
    upload_file: UploadFile,
    user_id: str,
    destination_dir: Optional[str] = None
) -> FileInfo:
    """
    Save an uploaded file to disk and return file info
    """
    # Generate a unique filename
    file_id = str(uuid.uuid4())
    original_filename = upload_file.filename
    filename = f"{file_id}_{original_filename}"
    
    # Determine the destination directory
    if not destination_dir:
        destination_dir = settings.UPLOAD_DIR
    
    # Create the directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)
    
    # Full path to save the file
    file_path = os.path.join(destination_dir, filename)
    
    # Save the file
    try:
        # Read the file content
        content = await upload_file.read()
        
        # Write the content to the destination file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Get content type
        content_type = upload_file.content_type or mimetypes.guess_type(original_filename)[0] or "application/octet-stream"
        
        # Create and return file info
        file_info = FileInfo(
            id=file_id,
            filename=filename,
            original_filename=original_filename,
            content_type=content_type,
            size=file_size,
            user_id=user_id,
            url=f"/static/uploads/{filename}",
            created_at=datetime.utcnow()
        )
        
        return file_info
    except Exception as e:
        logger.error(f"Error saving uploaded file: {e}")
        # Clean up if file was partially written
        if os.path.exists(file_path):
            os.remove(file_path)
        raise

async def get_file_info(file_id: str) -> Optional[FileInfo]:
    """
    Get file info from the database or file system
    """
    # This is a placeholder. In a real implementation, you would fetch this from a database.
    # For now, we'll just look for the file in the uploads directory
    
    try:
        # List all files in the uploads directory
        for filename in os.listdir(settings.UPLOAD_DIR):
            # Check if the filename starts with the file_id
            if filename.startswith(f"{file_id}_"):
                # Extract the original filename
                original_filename = filename[len(file_id) + 1:]
                
                # Get the full path
                file_path = os.path.join(settings.UPLOAD_DIR, filename)
                
                # Get file size
                file_size = os.path.getsize(file_path)
                
                # Get content type
                content_type = mimetypes.guess_type(original_filename)[0] or "application/octet-stream"
                
                # Create and return file info
                return FileInfo(
                    id=file_id,
                    filename=filename,
                    original_filename=original_filename,
                    content_type=content_type,
                    size=file_size,
                    user_id="unknown",  # This would come from a database in a real implementation
                    url=f"/static/uploads/{filename}",
                    created_at=datetime.fromtimestamp(os.path.getctime(file_path))
                )
        
        # File not found
        return None
    except Exception as e:
        logger.error(f"Error getting file info: {e}")
        return None

async def delete_file(file_id: str) -> bool:
    """
    Delete a file from disk
    """
    try:
        # List all files in the uploads directory
        for filename in os.listdir(settings.UPLOAD_DIR):
            # Check if the filename starts with the file_id
            if filename.startswith(f"{file_id}_"):
                # Get the full path
                file_path = os.path.join(settings.UPLOAD_DIR, filename)
                
                # Delete the file
                os.remove(file_path)
                
                return True
        
        # File not found
        return False
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return False

async def extract_text_from_file(file_path: str) -> Optional[str]:
    """
    Extract text from a file based on its content type
    """
    try:
        # Get the content type
        content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        
        # Extract text based on content type
        if content_type == "application/pdf":
            return await extract_text_from_pdf(file_path)
        elif content_type.startswith("image/"):
            return await extract_text_from_image(file_path)
        elif content_type.startswith("text/"):
            return await extract_text_from_text_file(file_path)
        else:
            logger.warning(f"Unsupported content type for text extraction: {content_type}")
            return f"[File content could not be extracted: {content_type}]"
    except Exception as e:
        logger.error(f"Error extracting text from file: {e}")
        return None

async def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file
    """
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return f"[Error extracting text from PDF: {str(e)}]"

async def extract_text_from_image(file_path: str) -> str:
    """
    Extract text from an image file
    """
    # This is a placeholder. In a real implementation, you would use OCR.
    # For now, we'll just return a placeholder message
    return "[Image content - OCR not implemented yet]"

async def extract_text_from_text_file(file_path: str) -> str:
    """
    Extract text from a text file
    """
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return await file.read()
    except Exception as e:
        logger.error(f"Error extracting text from text file: {e}")
        return f"[Error extracting text from file: {str(e)}]"

async def analyze_file(file_id: str) -> FileAnalysisResult:
    """
    Analyze a file and extract its content and metadata
    """
    try:
        # Get file info
        file_info = await get_file_info(file_id)
        if not file_info:
            return FileAnalysisResult(
                file_id=file_id,
                content_type="unknown",
                error="File not found"
            )
        
        # Get the full path
        file_path = os.path.join(settings.UPLOAD_DIR, file_info.filename)
        
        # Extract text
        text_content = await extract_text_from_file(file_path)
        
        # Get metadata
        metadata = {
            "filename": file_info.original_filename,
            "content_type": file_info.content_type,
            "size": file_info.size,
            "created_at": file_info.created_at.isoformat()
        }
        
        return FileAnalysisResult(
            file_id=file_id,
            content_type=file_info.content_type,
            text_content=text_content,
            metadata=metadata
        )
    except Exception as e:
        logger.error(f"Error analyzing file: {e}")
        return FileAnalysisResult(
            file_id=file_id,
            content_type="unknown",
            error=str(e)
        )

async def save_file(content: Union[str, bytes], filename: str, user_id: str = "system") -> FileInfo:
    """
    Save a file with the given content and filename
    
    Args:
        content: The content to save (string or bytes)
        filename: The filename to use
        user_id: The user ID to associate with the file
        
    Returns:
        FileInfo object with details about the saved file
    """
    try:
        # Generate a unique file ID
        file_id = str(uuid.uuid4())
        new_filename = f"{file_id}_{filename}"
        
        # Create the upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Full path to save the file
        file_path = os.path.join(settings.UPLOAD_DIR, new_filename)
        
        # Convert string content to bytes if needed
        if isinstance(content, str):
            file_content = content.encode('utf-8')
        else:
            file_content = content
        
        # Write the content to the file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Get content type
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        
        # Create file info
        file_info = FileInfo(
            id=file_id,
            filename=new_filename,
            original_filename=filename,
            content_type=content_type,
            size=file_size,
            user_id=user_id,
            url=f"/static/uploads/{new_filename}",
            created_at=datetime.utcnow()
        )
        
        # Store in Firebase if available
        if firebase_service.is_initialized():
            firebase_service.save_document(
                "files",
                {
                    "id": file_id,
                    "filename": new_filename,
                    "original_filename": filename,
                    "content_type": content_type,
                    "size": file_size,
                    "user_id": user_id,
                    "url": f"/static/uploads/{new_filename}",
                    "created_at": datetime.utcnow().isoformat()
                },
                file_id
            )
        
        return file_info
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise

async def read_file(file_id: str) -> Optional[bytes]:
    """
    Read a file's content by its ID
    
    Args:
        file_id: The ID of the file to read
        
    Returns:
        The file content as bytes, or None if the file was not found
    """
    try:
        # Get file info
        file_info = await get_file_info(file_id)
        if not file_info:
            return None
        
        # Get the full path
        file_path = os.path.join(settings.UPLOAD_DIR, file_info.filename)
        
        # Read and return the file content
        async with aiofiles.open(file_path, 'rb') as f:
            return await f.read()
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return None
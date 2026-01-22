"""
Database query functions for resume storage (stub implementation).
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ResumeRecord:
    """Mock resume record."""
    def __init__(self, user_id, content, filename="resume.pdf"):
        self.id = 1
        self.user_id = user_id
        self.content = content
        self.filename = filename
        self.created_at = datetime.now()


def save_resume(db, user_id: int, content: bytes, filename: str = "tailored_resume.pdf"):
    """
    Save a tailored resume to the database.

    Args:
        db: Database session
        user_id: User identifier
        content: Resume content as bytes
        filename: Name of the file

    Returns:
        ResumeRecord object
    """
    logger.info(f"Saving resume for user {user_id} (stub - not actually saved)")
    record = ResumeRecord(user_id=user_id, content=content, filename=filename)
    return record


def delete_resume(db, resume_id: int = None, list_only: bool = False):
    """
    Delete a resume or list all resumes.

    Args:
        db: Database session
        resume_id: ID of resume to delete
        list_only: If True, return list of all resumes instead

    Returns:
        List of resume records if list_only=True, else None
    """
    if list_only:
        logger.info("Listing resumes (stub - returning empty list)")
        return []

    if resume_id:
        logger.info(f"Deleting resume {resume_id} (stub - not actually deleted)")

    return None


def get_resume_history(db, user_id: int, limit: int = 10):
    """
    Get resume history for a user.

    Args:
        db: Database session
        user_id: User identifier
        limit: Maximum number of records to return

    Returns:
        List of resume records
    """
    logger.info(f"Getting resume history for user {user_id} (stub - returning empty list)")
    return []

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .models import Candidate, Resume, WorkExperience, Education, Application

class CandidateRepository:
    """
    Repository for managing candidate-related database operations.
    Provides an abstraction layer for CRUD operations on Candidate entities.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.

        :param session: SQLAlchemy database session
        """
        self._session = session

    def create_candidate(
        self, 
        first_name: str, 
        last_name: str, 
        email: str, 
        phone: Optional[str] = None, 
        address: Optional[str] = None
    ) -> Candidate:
        """
        Create a new candidate in the database, handling potential duplicates.

        :param first_name: Candidate's first name
        :param last_name: Candidate's last name
        :param email: Candidate's email address
        :param phone: Optional phone number
        :param address: Optional address
        :return: Created or existing Candidate object
        """
        # First, check if a candidate with this email already exists
        existing_candidate = self.get_candidate_by_email(email)
        
        if existing_candidate:
            # Update existing candidate's information
            existing_candidate.firstName = first_name
            existing_candidate.lastName = last_name
            existing_candidate.phone = phone or existing_candidate.phone
            existing_candidate.address = address or existing_candidate.address
            
            try:
                self._session.commit()
                return existing_candidate
            except Exception as e:
                self._session.rollback()
                print(f"Error updating existing candidate: {e}")
                raise

        # If no existing candidate, create a new one
        candidate = Candidate(
            firstName=first_name,
            lastName=last_name,
            email=email,
            phone=phone,
            address=address
        )
        
        try:
            self._session.add(candidate)
            self._session.commit()
            return candidate
        except IntegrityError:
            # If there's an integrity error (e.g., unique constraint), rollback and handle
            self._session.rollback()
            # Try to get the existing candidate again
            existing_candidate = self.get_candidate_by_email(email)
            if existing_candidate:
                return existing_candidate
            else:
                # If still can't find the candidate, re-raise the exception
                raise

    def get_candidate_by_email(self, email: str) -> Optional[Candidate]:
        """
        Retrieve a candidate by their email address.

        :param email: Candidate's email address
        :return: Candidate object or None if not found
        """
        try:
            return self._session.query(Candidate).filter_by(email=email).first()
        except Exception as e:
            print(f"Error retrieving candidate by email: {e}")
            return None

    # Rest of the methods remain the same as in the original file
    def add_resume(
        self, 
        candidate_id: int, 
        file_path: str, 
        file_type: str
    ) -> Resume:
        """
        Add a resume to a candidate's profile.

        :param candidate_id: ID of the candidate
        :param file_path: Path to the resume file
        :param file_type: MIME type or file extension
        :return: Created Resume object
        """
        from datetime import datetime

        resume = Resume(
            candidateId=candidate_id,
            filePath=file_path,
            fileType=file_type,
            uploadDate=datetime.utcnow()
        )
        self._session.add(resume)
        self._session.commit()
        return resume

    # ... (rest of the methods remain unchanged)
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

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
        Create a new candidate in the database.

        :param first_name: Candidate's first name
        :param last_name: Candidate's last name
        :param email: Candidate's email address
        :param phone: Optional phone number
        :param address: Optional address
        :return: Created Candidate object
        """
        candidate = Candidate(
            firstName=first_name,
            lastName=last_name,
            email=email,
            phone=phone,
            address=address
        )
        self._session.add(candidate)
        self._session.commit()
        return candidate

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

    def add_work_experience(
        self,
        candidate_id: int,
        company: str,
        position: str,
        start_date,
        end_date: Optional[datetime] = None,
        description: Optional[str] = None
    ) -> WorkExperience:
        """
        Add work experience to a candidate's profile.

        :param candidate_id: ID of the candidate
        :param company: Company name
        :param position: Job position
        :param start_date: Start date of employment
        :param end_date: Optional end date of employment
        :param description: Optional job description
        :return: Created WorkExperience object
        """
        work_exp = WorkExperience(
            candidateId=candidate_id,
            company=company,
            position=position,
            startDate=start_date,
            endDate=end_date,
            description=description
        )
        self._session.add(work_exp)
        self._session.commit()
        return work_exp

    def add_education(
        self,
        candidate_id: int,
        institution: str,
        title: str,
        start_date,
        end_date: Optional[datetime] = None
    ) -> Education:
        """
        Add educational background to a candidate's profile.

        :param candidate_id: ID of the candidate
        :param institution: Name of educational institution
        :param title: Degree or certification title
        :param start_date: Start date of education
        :param end_date: Optional end date of education
        :return: Created Education object
        """
        education = Education(
            candidateId=candidate_id,
            institution=institution,
            title=title,
            startDate=start_date,
            endDate=end_date
        )
        self._session.add(education)
        self._session.commit()
        return education

    def search_candidates(
        self, 
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None
    ) -> List[Candidate]:
        """
        Search for candidates based on various criteria.

        :param first_name: Optional first name filter
        :param last_name: Optional last name filter
        :param email: Optional email filter
        :param company: Optional company filter
        :return: List of matching Candidate objects
        """
        query = self._session.query(Candidate)
        
        if first_name:
            query = query.filter(Candidate.firstName.ilike(f'%{first_name}%'))
        
        if last_name:
            query = query.filter(Candidate.lastName.ilike(f'%{last_name}%'))
        
        if email:
            query = query.filter(Candidate.email.ilike(f'%{email}%'))
        
        if company:
            # Join with WorkExperience to filter by company
            query = query.join(WorkExperience).filter(WorkExperience.company.ilike(f'%{company}%'))
        
        return query.all()

    def create_application(
        self, 
        candidate_id: int, 
        position_id: int,
        interview_step_id: Optional[int] = None
    ) -> Application:
        """
        Create a job application for a candidate.

        :param candidate_id: ID of the candidate
        :param position_id: ID of the job position
        :param interview_step_id: Optional initial interview step
        :return: Created Application object
        """
        from datetime import datetime

        application = Application(
            candidateId=candidate_id,
            positionId=position_id,
            applicationDate=datetime.utcnow(),
            interviewStepId=interview_step_id
        )
        self._session.add(application)
        self._session.commit()
        return application

    def get_candidate_applications(self, candidate_id: int) -> List[Application]:
        """
        Retrieve all applications for a specific candidate.

        :param candidate_id: ID of the candidate
        :return: List of Application objects
        """
        return self._session.query(Application).filter_by(candidateId=candidate_id).all()
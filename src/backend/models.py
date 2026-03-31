from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Candidate(Base):
    """
    Represents a job candidate who can apply for positions within the system.
    Aligned with data-model.md Candidate specification.
    """
    __tablename__ = 'candidates'

    id = Column(Integer, primary_key=True)
    firstName = Column(String(100))
    lastName = Column(String(100))
    email = Column(String(255), unique=True)
    phone = Column(String(15))
    address = Column(String(100))
    score = Column(Integer, default=0)

    # Relationships
    educations = relationship("Education", back_populates="candidate")
    work_experiences = relationship("WorkExperience", back_populates="candidate")
    resumes = relationship("Resume", back_populates="candidate")
    applications = relationship("Application", back_populates="candidate")

class Education(Base):
    """
    Represents educational background information for candidates.
    Aligned with data-model.md Education specification.
    """
    __tablename__ = 'educations'

    id = Column(Integer, primary_key=True)
    institution = Column(String(100), nullable=False)
    title = Column(String(250), nullable=False)
    startDate = Column(DateTime, nullable=False)
    endDate = Column(DateTime, nullable=True)
    candidateId = Column(Integer, ForeignKey('candidates.id'))

    # Relationship
    candidate = relationship("Candidate", back_populates="educations")

class WorkExperience(Base):
    """
    Represents work history and professional experience for candidates.
    Aligned with data-model.md WorkExperience specification.
    """
    __tablename__ = 'work_experiences'

    id = Column(Integer, primary_key=True)
    company = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    description = Column(String(200), nullable=True)
    startDate = Column(DateTime, nullable=False)
    endDate = Column(DateTime, nullable=True)
    candidateId = Column(Integer, ForeignKey('candidates.id'))

    # Relationship
    candidate = relationship("Candidate", back_populates="work_experiences")

class Resume(Base):
    """
    Represents uploaded resume files associated with candidates.
    Aligned with data-model.md Resume specification.
    """
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True)
    filePath = Column(String(500), nullable=False)
    fileType = Column(String(50), nullable=False)
    uploadDate = Column(DateTime, nullable=False)
    candidateId = Column(Integer, ForeignKey('candidates.id'))

    # Relationship
    candidate = relationship("Candidate", back_populates="resumes")

class Application(Base):
    """
    Represents a candidate's application to a specific position.
    Aligned with data-model.md Application specification.
    """
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    applicationDate = Column(DateTime, nullable=False)
    currentInterviewStep = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    positionId = Column(Integer, ForeignKey('positions.id'))
    candidateId = Column(Integer, ForeignKey('candidates.id'))
    interviewStepId = Column(Integer, ForeignKey('interview_steps.id'))

    # Relationships
    position = relationship("Position", back_populates="applications")
    candidate = relationship("Candidate", back_populates="applications")
    interview_step = relationship("InterviewStep", back_populates="applications")
    interviews = relationship("Interview", back_populates="application")

class Position(Base):
    """
    Represents job positions available for application.
    Aligned with data-model.md Position specification.
    """
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    companyId = Column(Integer, ForeignKey('companies.id'), nullable=False)
    interviewFlowId = Column(Integer, ForeignKey('interview_flows.id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=False)
    status = Column(String(20), nullable=False, default='Draft')
    isVisible = Column(Boolean, default=False)
    location = Column(String, nullable=False)
    jobDescription = Column(String, nullable=False)
    requirements = Column(String, nullable=True)
    responsibilities = Column(String, nullable=True)
    salaryMin = Column(Float, nullable=True)
    salaryMax = Column(Float, nullable=True)
    employmentType = Column(String(50), nullable=True)
    benefits = Column(String, nullable=True)
    companyDescription = Column(String, nullable=True)
    applicationDeadline = Column(DateTime, nullable=True)
    contactInfo = Column(String, nullable=True)

    # Relationships
    company = relationship("Company", back_populates="positions")
    interview_flow = relationship("InterviewFlow", back_populates="positions")
    applications = relationship("Application", back_populates="position")

class Company(Base):
    """
    Represents companies that post job positions and employ staff.
    Aligned with data-model.md Company specification.
    """
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    # Relationships
    employees = relationship("Employee", back_populates="company")
    positions = relationship("Position", back_populates="company")

class Employee(Base):
    """
    Represents employees within companies who can conduct interviews.
    Aligned with data-model.md Employee specification.
    """
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)
    isActive = Column(Boolean, default=True)
    companyId = Column(Integer, ForeignKey('companies.id'))

    # Relationships
    company = relationship("Company", back_populates="employees")
    interviews = relationship("Interview", back_populates="employee")

class InterviewFlow(Base):
    """
    Represents a sequence of interview steps that define the hiring process.
    Aligned with data-model.md InterviewFlow specification.
    """
    __tablename__ = 'interview_flows'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=True)

    # Relationships
    interview_steps = relationship("InterviewStep", back_populates="interview_flow")
    positions = relationship("Position", back_populates="interview_flow")

class InterviewStep(Base):
    """
    Represents individual steps within an interview flow.
    Aligned with data-model.md InterviewStep specification.
    """
    __tablename__ = 'interview_steps'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    orderIndex = Column(Integer, nullable=False)
    interviewFlowId = Column(Integer, ForeignKey('interview_flows.id'))
    interviewTypeId = Column(Integer, ForeignKey('interview_types.id'))

    # Relationships
    interview_flow = relationship("InterviewFlow", back_populates="interview_steps")
    interview_type = relationship("InterviewType", back_populates="interview_steps")
    applications = relationship("Application", back_populates="interview_step")
    interviews = relationship("Interview", back_populates="interview_step")

class InterviewType(Base):
    """
    Defines different types of interviews that can be conducted.
    Aligned with data-model.md InterviewType specification.
    """
    __tablename__ = 'interview_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Relationships
    interview_steps = relationship("InterviewStep", back_populates="interview_type")

class Interview(Base):
    """
    Represents individual interview sessions conducted as part of an application.
    Aligned with data-model.md Interview specification.
    """
    __tablename__ = 'interviews'

    id = Column(Integer, primary_key=True)
    interviewDate = Column(DateTime, nullable=False)
    result = Column(String, nullable=True)
    score = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    applicationId = Column(Integer, ForeignKey('applications.id'))
    interviewStepId = Column(Integer, ForeignKey('interview_steps.id'))
    employeeId = Column(Integer, ForeignKey('employees.id'))

    # Relationships
    application = relationship("Application", back_populates="interviews")
    interview_step = relationship("InterviewStep", back_populates="interviews")
    employee = relationship("Employee", back_populates="interviews")
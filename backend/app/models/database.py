"""Database models for RxGenome."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, Integer, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Case(Base):
    __tablename__ = "cases"
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String(255), nullable=False)
    condition = Column(String(255), default="breast_cancer_risk")
    status = Column(String(50), default="created")  # created, uploading, processing, completed, error
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    uploads = relationship("Upload", back_populates="case", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="case", cascade="all, delete-orphan")
    pgx_findings = relationship("PGxFinding", back_populates="case", cascade="all, delete-orphan")
    summaries = relationship("Summary", back_populates="case", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="case", cascade="all, delete-orphan")
    report_fields = relationship("ReportField", back_populates="case", cascade="all, delete-orphan")


class Upload(Base):
    __tablename__ = "uploads"
    id = Column(String, primary_key=True, default=gen_uuid)
    case_id = Column(String, ForeignKey("cases.id"), nullable=False)
    upload_type = Column(String(50), nullable=False)  # genome, report, medication_label
    filename = Column(String(255), nullable=False)
    filepath = Column(String(512), nullable=False)
    mime_type = Column(String(100))
    file_size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="uploads")


class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(String, primary_key=True, default=gen_uuid)
    case_id = Column(String, ForeignKey("cases.id"), nullable=False)
    model_name = Column(String(100), default="xgboost")
    risk_score = Column(Float)
    risk_tier = Column(String(20))  # low, moderate, high
    accuracy = Column(Float)
    roc_auc = Column(Float)
    feature_importance = Column(JSON)  # top features with importances
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="predictions")


class Medication(Base):
    __tablename__ = "medications"
    id = Column(String, primary_key=True, default=gen_uuid)
    case_id = Column(String, ForeignKey("cases.id"), nullable=False)
    raw_name = Column(String(255))
    canonical_name = Column(String(255))
    source = Column(String(50))  # text_input, label_upload
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="medications")


class PGxFinding(Base):
    __tablename__ = "pgx_findings"
    id = Column(String, primary_key=True, default=gen_uuid)
    case_id = Column(String, ForeignKey("cases.id"), nullable=False)
    medication = Column(String(255))
    gene = Column(String(50))
    genotype = Column(String(50))
    phenotype = Column(String(100))
    caution_level = Column(String(20))
    summary = Column(Text)
    discussion_points = Column(JSON)
    evidence = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="pgx_findings")


class ReportField(Base):
    __tablename__ = "report_fields"
    id = Column(String, primary_key=True, default=gen_uuid)
    case_id = Column(String, ForeignKey("cases.id"), nullable=False)
    field_name = Column(String(255))
    field_value = Column(String(512))
    unit = Column(String(50))
    reference_range = Column(String(100))
    is_abnormal = Column(Integer, default=0)
    source = Column(String(50))  # pdf, screenshot
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="report_fields")


class Summary(Base):
    __tablename__ = "summaries"
    id = Column(String, primary_key=True, default=gen_uuid)
    case_id = Column(String, ForeignKey("cases.id"), nullable=False)
    summary_type = Column(String(50))  # patient, clinician, doctor_note
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="summaries")

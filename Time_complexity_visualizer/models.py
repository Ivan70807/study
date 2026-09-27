"""
ORM model for a saved analysis run.

Defined with SQLAlchemy's declarative base so the schema is plain
Python — no CREATE TABLE / raw SQL anywhere.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, JSON, String, Text

from database import Base


class AnalysisResult(Base):
    """One row per /save_analysis call: the full result of timing an
    algorithm across a range of input sizes, plus the chart that
    visualized it."""

    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    algo = Column(String(100), nullable=False)
    complexity = Column(String(50), nullable=False)
    n_min = Column(Integer, nullable=False)
    n_max = Column(Integer, nullable=False)
    step = Column(Integer, nullable=False)
    points = Column(JSON, nullable=False)  # list of {"n": ..., "time_seconds": ...}
    image_base64 = Column(Text, nullable=False)
    image_snapshot_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self, include_image=True):
        """Serialize this row to a plain dict for jsonify().

        include_image=False drops the (often large) base64 string —
        use that for list views so the payload stays small.
        """
        data = {
            "id": self.id,
            "algo": self.algo,
            "complexity": self.complexity,
            "n_min": self.n_min,
            "n_max": self.n_max,
            "step": self.step,
            "points": self.points,
            "image_snapshot_path": self.image_snapshot_path,
            "created_at": self.created_at.isoformat(),
        }
        if include_image:
            data["image_base64"] = self.image_base64
        return data

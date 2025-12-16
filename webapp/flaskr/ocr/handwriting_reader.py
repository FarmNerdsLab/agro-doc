"""
Definition for abstract HandwritingReader class
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Generic, TypeVar
from enum import Enum


class OCRType(Enum):
    """
    Enum for the type of OCR to use.
    """

    GOOGLE_CLOUD_VISION = "google_cloud_vision"
    PADDLE = "paddle"


@dataclass
class ReadText:
    """
    Wrapper for the text, confidence, and bounding boxes output returned by the
    OCR API call.

    Note: not all OCR APIs return bounding boxes, so this field is optional.
    """

    text: List[str]
    confidence: List[float]
    bounding_boxes: List[tuple[float, float, float, float]] | None

    def __len__(self) -> int:
        return len(self.text)


# Type variable for the OCR implementation
T = TypeVar('T', bound='HandwritingReader')


class HandwritingReader(ABC):
    """
    Abstract base class for handwriting readers.
    
    Implementations should override read_text() to return a ReadText object.
    """
    
    @abstractmethod
    def read_text(self, path: str) -> ReadText:
        """
        Uses OCR to extract text from an image file at the specified path.

        Args:
            path: a string representing the path to the image file.

        Returns:
            A ReadText object containing the extracted text, confidence scores,
            and bounding boxes.
        """
        pass


class HandwritingReaderFactory:
    """
    Factory class to create the appropriate HandwritingReader based on OCRType.
    """
    
    @staticmethod
    def create(ocr_type: OCRType) -> HandwritingReader:
        """
        Creates and returns the appropriate HandwritingReader implementation.
        
        Args:
            ocr_type: an OCRType enum value specifying the type of OCR to use.
            
        Returns:
            An instance of the appropriate HandwritingReader subclass.
        """
        if ocr_type == OCRType.GOOGLE_CLOUD_VISION:
            from .gcp_hw_reader import GoogleCloudVisionHR
            return GoogleCloudVisionHR()
        elif ocr_type == OCRType.PADDLE:
            from .paddle_hw_reader import PaddleHandwritingReader
            return PaddleHandwritingReader()
        else:
            raise ValueError(f"Unsupported OCR type: {ocr_type}")

# Tests
The tests in this directory follow the Pytest framework. 

## Tests for Handwritten Text Reader (HTR) Wrappers

This directory contains tests for the wrappers of the following HTR models:
- PaddleOCR PP-OCRv5_mobile_rec
- Google Cloud Vision OCR

### Test Cases
- happy path: returns images text in a list of strings
- invalid file input (i.e. not an image)
- image without any text returns empty list
- image with low confidence of text?

## Tests for LLM Wrappers

This directory also contains test for the wrappers of the following LLM models:
- transformers microsoft/Phi-3-mini-128k-instruct

**Testing for the LLM wrappers seems difficult to me because of their non-deterministic nature**
- I would look into setting seed
- Tests could perform simple benchmarking on my use-case of correcting words and turning it into JSON output

### Test Cases
- (HAPPY PATH) takes in well-translated text and puts it into JSON format
- (WORD CORRECTION + JSONIFY) Takes in mock image text in the form of a list of strings (hardcoded) with confidence scores; LLM outputs JSON formatted words and corrects mis-translated words with farm words
    - i.e. `("3 coke cumbers" , 0.6) -> "entry: {"crop" : "cucumbers", "quantity" : 3}`'
- (NO TEXT) Handles an empty list and does nothing


## Backend Tests

end-to-end pipeline test of connecting a client through Flask Pytest 
# Webapp Directory
[description place-holder]

## Trying Different OCRs
7 November 2025

I am exploring some new OCR frameworks to use to translate the raw handwritten text in images to not only (1) translate them directly but also (2) query an LLM to edit the text based on "expected" or "assumed" inputs.

For example, if I am uploading an image that has the word "cukes" but it's difficult for the OCR to pick up the letters, it my translate it as "cokes". However, with our understanding, we know that it's very unlikely to have the word "cokes" on a whiteboard, and much MORE likely to have so-called *farm-related* terms on the whiteboard. Therefore, we want to use an edit step using an LLM with the farm-context. Additionally, we could use an LLM to offer potential organizations of the text.


To summarize, a potential workflow is:

1. Upload an image of handwriting
2. Have an OCR model translate it
3. Pipe the text into an LLM that can use the farm-context
4. Pipe the 'corrected' text into JSON format or the Excel format

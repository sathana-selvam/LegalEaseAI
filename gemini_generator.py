import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiGenerator:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing. Please add it to the .env file."
            )

        genai.configure(api_key=GEMINI_API_KEY)

        self.model = genai.GenerativeModel(GEMINI_MODEL)

    def generate_document(
        self,
        document_type: str,
        user_details: dict
    ) -> str:

        details_text = "\n".join(
            f"{key}: {value}"
            for key, value in user_details.items()
            if value
        )

        prompt = f"""
You are LegalEase, an AI-powered legal documentation assistant.

Create a professional legal document based on the information supplied by
the user.

Document Type:
{document_type}

User Information:
{details_text}

Instructions:

1. Generate a complete and professional document.
2. Use clear legal language.
3. Add appropriate headings and numbered clauses.
4. Include parties, dates, responsibilities, payment terms where applicable,
   termination, confidentiality where applicable, dispute resolution,
   governing law and signatures where appropriate.
5. Do not invent important personal information.
6. Use [NOT PROVIDED] where an important field is missing.
7. Make the document easy for a normal user to understand.
8. Do not claim that the document guarantees legal validity.
9. Add a short note at the end:
   "This document is AI-generated and should be reviewed by a qualified
   legal professional before signing."

Return only the document text.
"""

        response = self.model.generate_content(prompt)

        if not response or not response.text:
            raise RuntimeError("Gemini did not return any document content.")

        return response.text.strip()
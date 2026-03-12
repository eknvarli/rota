from typing import Optional
from google import genai
from app.core.config import settings

class AIService:
    def __init__(self):
        if settings.GOOGLE_API_KEY:
            self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        else:
            self.client = None

    async def analyze_lead(self, lead_name: str, niche: str, details: str) -> str:
        prompt = f"""
        Analyze the needs of the following potential customer:
        Customer Name: {lead_name}
        Niche: {niche}
        Context/Details: {details}
        
        Identify their likely pain points and how an AI automation solution could help them.
        Be specific and professional. Respond in Turkish.
        """
        
        if self.client:
            # Using sync call for now, could use self.client.aio for async
            response = self.client.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt
            )
            return response.text
        
        return f"Simulated analysis for {lead_name} in {niche} niche (Set GOOGLE_API_KEY for real results)."

    async def generate_proposal(self, lead_name: str, analysis: str) -> str:
        prompt = f"""
        Generate a compelling business proposal for: {lead_name}
        Based on this analysis: {analysis}
        
        The proposal should be:
        1. Professional and personalized.
        2. Focused on value and ROI.
        3. Clear call to action.
        
        Format as a professional email/message in Turkish.
        """
        
        if self.client:
            response = self.client.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt
            )
            return response.text
            
        return f"Simulated proposal for {lead_name} based on analysis (Set GOOGLE_API_KEY for real results)."

ai_service = AIService()

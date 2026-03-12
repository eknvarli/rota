from typing import List, Dict
import httpx
from app.core.config import settings

from serpapi import GoogleSearch
from app.core.config import settings

class LeadService:
    async def find_leads(self, niche: str, location: str) -> List[Dict]:
        """
        Finds leads using SerpApi (Google Maps).
        """
        if not settings.SERP_API_KEY:
            # Return Mock Data if no API key
            return [
                {
                    "name": f"{niche} Center {location} (Mock)",
                    "website": f"https://example-{niche.lower()}.com",
                    "niche": niche,
                    "location": location,
                }
            ]
        
        params = {
            "engine": "google_maps",
            "q": f"{niche} in {location}",
            "api_key": settings.SERP_API_KEY
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            local_results = results.get("local_results", [])
            
            leads = []
            for res in local_results:
                leads.append({
                    "name": res.get("title"),
                    "website": res.get("website"),
                    "niche": niche,
                    "location": location,
                })
            return leads
        except Exception as e:
            print(f"SerpApi Error: {e}")
            return []

lead_service = LeadService()

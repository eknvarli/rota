from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.db.session import get_db
from app.models import User, Lead
from app.schemas.lead import LeadInDB, LeadCreate, LeadSearchParams, LeadUpdate
from app.services.lead_service import lead_service
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/search", response_model=List[LeadInDB])
async def search_leads(
    *,
    db: AsyncSession = Depends(get_db),
    params: LeadSearchParams,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    # Find leads
    found_leads = await lead_service.find_leads(params.niche, params.location)
    
    db_leads = []
    for lead_data in found_leads:
        # Check if already exists? (Optional for now)
        db_lead = Lead(
            **lead_data,
            details=params.details,
            status="found"
        )
        db.add(db_lead)
        db_leads.append(db_lead)
    
    await db.commit()
    for l in db_leads:
        await db.refresh(l)
    return db_leads

@router.get("/", response_model=List[LeadInDB])
async def list_leads(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    result = await db.execute(select(Lead))
    return result.scalars().all()

@router.post("/{lead_id}/analyze", response_model=LeadInDB)
async def analyze_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalars().first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    analysis = await ai_service.analyze_lead(lead.name, lead.niche, lead.details or "")
    lead.analysis = analysis
    lead.status = "analyzed"
    
    await db.commit()
    await db.refresh(lead)
    return lead

@router.post("/{lead_id}/generate-proposal", response_model=LeadInDB)
async def generate_proposal(
    lead_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalars().first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    if not lead.analysis:
        raise HTTPException(status_code=400, detail="Lead must be analyzed first")
    
    proposal = await ai_service.generate_proposal(lead.name, lead.analysis)
    lead.proposal_text = proposal
    lead.status = "proposal_generated"
    
    await db.commit()
    await db.refresh(lead)
    return lead

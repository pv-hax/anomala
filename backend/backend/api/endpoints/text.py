from fastapi import APIRouter, Depends, Request, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ...core.database import get_db
from ..schemas import TextEventCreate
from ..dependencies import get_client_ip
from ...models import TextMessage, Customer, IPList
from ...services.llm import LLMService
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

router = APIRouter()
llm_service = LLMService()


async def process_text_with_llm(
    db: Session, event_id: int, text: str, ip: int, domain: str
):
    """Background task to process text with OpenAI"""
    try:
        # Get analysis from OpenAI
        result = await llm_service.analyze_text(event_id, text, ip, domain)

        logger.info(f"Debug - Received result: {result}")

        # Update the database
        event = db.query(TextMessage).filter(TextMessage.id == event_id).first()
        if event:
            event.is_malicious = result["is_malicious"]
            event.type = result["type"]  # Using existing type column
            db.commit()

            # If malicious, update IP list
            if result["is_malicious"]:
                ip_entry = (
                    db.query(IPList)
                    .filter(IPList.ip_address == ip, IPList.domain == domain)
                    .first()
                )

                if ip_entry:
                    ip_entry.is_blocked = True
                    db.commit()

    except Exception as e:
        logger.info(f"Error processing text: {e}")
        # In production, add proper error handling and logging


@router.post("/text")
async def create_text_event(
    event: TextEventCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    try:
        logger.info("Starting text event creation")

        ip_int, domain = get_client_ip(request)
        logger.info(f"Debug - Received request for domain: {domain}")

        # Check if domain exists, if not create it
        customer = db.query(Customer).filter(Customer.domain == domain).first()
        if not customer:
            logger.info(f"Debug - Creating new customer for domain: {domain}")
            customer = Customer(
                domain=domain,
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)

        # Check if IP is blocked
        ip_blocked = (
            db.query(IPList)
            .filter(
                IPList.ip_address == ip_int,
                IPList.domain == domain,
                IPList.is_blocked is True,
            )
            .first()
        )
        if ip_blocked:
            raise HTTPException(status_code=403, detail="IP is blocked")

        # Create text event with initial type
        text_event = TextMessage(
            domain=domain,
            ip_address=ip_int,
            message=event.message,
            type=event.type,  # Use the type from the request
        )

        logger.info(f"Debug - Creating text event: {text_event.__dict__}")  # Debug line

        db.add(text_event)
        db.commit()
        db.refresh(text_event)

        # Add OpenAI processing to background tasks
        background_tasks.add_task(
            process_text_with_llm, db, text_event.id, event.message, ip_int, domain
        )

        return {"status": "success", "id": text_event.id}

    except Exception as e:
        logger.info(f"Error in create_text_event: {str(e)}")  # Debug line
        raise

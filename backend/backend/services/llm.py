from openai import AsyncOpenAI
from typing import Dict, Literal
from enum import Enum
import json
from os import getenv
import logging

logger = logging.getLogger(__name__)

class AttackType(str, Enum):
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    COMMAND_INJECTION = "command_injection"
    PATH_TRAVERSAL = "path_traversal"
    NORMAL = "normal"
    UNKNOWN = "unknown"

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=getenv("OPENAI_API_KEY"))

    async def analyze_text(
        self, event_id: int, text: str, ip: str, domain: str
    ) -> Dict:
        """Analyze text using OpenAI API to detect malicious content and attack type"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a security analyst. Analyze the following text and determine:
                        1. If it's malicious
                        2. The specific type of attack if malicious
                        Common attacks include: SQL injection, XSS, Command injection, Path traversal
                        Be precise in your analysis."""
                    },
                    {
                        "role": "user",
                        "content": f"Domain: {domain}\nIP: {ip}\nText: {text}",
                    },
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "security_analysis_schema",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "is_malicious": {
                                    "description": "Whether the analyzed content is malicious",
                                    "type": "boolean",
                                },
                                "attack_type": {
                                    "description": "The specific type of attack if malicious",
                                    "type": "string",
                                    "enum": [
                                        "sql_injection",
                                        "xss",
                                        "command_injection",
                                        "path_traversal",
                                        "normal",
                                        "unknown"
                                    ],
                                },
                                "confidence_score": {
                                    "description": "Confidence score of the analysis (0-1)",
                                    "type": "number",
                                    "minimum": 0,
                                    "maximum": 1
                                }
                            },
                            "required": ["is_malicious", "attack_type", "confidence_score"],
                            "additionalProperties": False,
                        },
                    },
                },
            )

            analysis = json.loads(response.choices[0].message.content)
            return {
                "event_id": event_id,
                "is_malicious": analysis["is_malicious"],
                "type": analysis["attack_type"],
                "confidence_score": analysis["confidence_score"]
            }

        except Exception as e:
            logger.error(f"Error in OpenAI analysis: {str(e)}", exc_info=True)
            return {
                "event_id": event_id,
                "is_malicious": False,
                "type": AttackType.UNKNOWN.value,
                "confidence_score": 0
            }

from openai import AsyncOpenAI
from typing import Dict
import json
from os import getenv


class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=getenv("OPENAI_API_KEY"))

    async def analyze_text(
        self, event_id: int, text: str, ip: int, domain: str
    ) -> Dict:
        """Analyze text using OpenAI API"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a security analyst. Analyze the following text and determine if it's malicious.",
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
                                "type": {
                                    "description": "The classification of the content (normal, suspicious, or malicious)",
                                    "type": "string",
                                    "enum": ["normal", "suspicious", "malicious"],
                                },
                                "additionalProperties": False,
                            },
                        },
                    },
                },
            )

            analysis = json.loads(response.choices[0].message.content)
            return {
                "event_id": event_id,
                "is_malicious": analysis.get("is_malicious", False),
                "type": analysis.get("type", "normal"),
            }

        except Exception as e:
            print(f"Error in OpenAI analysis: {e}")
            return {"event_id": event_id, "is_malicious": False, "type": "error"}

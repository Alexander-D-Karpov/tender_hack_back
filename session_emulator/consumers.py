import json
import os

import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tender_hack_back.settings")
django.setup()

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from competence.models import CompanyQuotationSession, Company, QuotationSession
from session_emulator.models import Lot


@database_sync_to_async
def create_lot(company_id: int, session: int, prise: int):
    company = Company.objects.get(id=company_id)
    quotation_session = QuotationSession.objects.get(id=session)
    quotation_session.current_price = prise
    quotation_session.save(update_fields=["current_price"])
    comp_quotation_session = CompanyQuotationSession.objects.get_or_create(
        company=company, quotation_session=quotation_session, is_bot=False
    )
    if CompanyQuotationSession.is_bot:
        r = requests.get("http://127.0.0.1:5000/")
        dat = r.json()["push_lot_prediction"]
        if dat:
            Lot.objects.create(
                comp_quotation_session=comp_quotation_session[0], price=prise * 0.99
            )
            return prise * 0.99, quotation_session.company.id
        return None, None


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = text_data.split(" ")
        company_id = int(data[0])
        lot = float(data[1])
        company2_id = int(data[2])
        session = self.room_group_name.split("_")[1]
        prise, company3_id = await create_lot(company_id, int(session), lot)
        if prise:
            mes = [lot, prise]
        else:
            mes = [lot]
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": mes,
                "company_id": company_id,
                "company2_id": company2_id,
                "company3_id": company3_id,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        company_id = event["company_id"]
        company2_id = event["company2_id"]
        company3_id = event["company3_id"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "lot": message,
                    "bot": False,
                    "company": company_id,
                    "company2": company2_id,
                    "company3": company3_id,
                }
            )
        )

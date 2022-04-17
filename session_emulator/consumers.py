import json
import os

import django

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
    comp_quotation_session = CompanyQuotationSession.objects.get_or_create(
        company=company, quotation_session=quotation_session, is_bot=False
    )
    Lot.objects.create(comp_quotation_session=comp_quotation_session[0], price=prise)


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
        session = self.room_group_name.split("_")[1]
        await create_lot(company_id, int(session), lot)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": lot}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"lot": message, "bot": False}))

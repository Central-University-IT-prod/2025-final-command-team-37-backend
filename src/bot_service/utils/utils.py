import asyncio
import os
from datetime import datetime

import aiohttp

sent_bookings = set()


async def send_request():
    url = "https://prod-team-37-ajc3mefd.REDACTED/api/v1/bookings/pending"

    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    for booking in data:
                        booking_id = booking["id"]
                        if booking_id not in sent_bookings:
                            print(f"Уведомление для booking_id {booking_id} отправлено")
                            async with session.post(
                                    f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage?user_id={booking['user_id']}&text=У вас забронировано место в коворкинге на сегодня в {datetime.fromisoformat(booking['start_time']).strftime('%H:%M')}") as r:
                                sent_bookings.add(booking_id)

            await asyncio.sleep(10)

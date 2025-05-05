from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from subscription_api.key_config_shaper import generate_config_key, get_traffic
from dao.update_methods_dao import update_last_seen
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get('/connection/sub/{user_uuid}', response_class=PlainTextResponse)
async def key_issuance(user_uuid: str):
    config_key = await generate_config_key(user_id=user_uuid)

    if config_key is not None:
        update_last_seen_status = await update_last_seen(user_id=user_uuid)

        if not update_last_seen_status:
            logger.error(f"Не удалось обновить поле last_seen для пользователя {user_uuid}")

        traffic = await get_traffic(user_id=user_uuid)

        headers = {
            "profile-title": "REVOLT VPN",
            "subscription-userinfo": f"upload={traffic.up}; download={traffic.down}; total={traffic.total}; expire=2524608000",
            "announce": "🚀 #27e8d5Тест",
            "announce-url": "https://t.me/kellpython",
            "profile-update-interval": "6",
            "update-always": "true"
        }
        return PlainTextResponse(content=config_key, headers=headers)

    raise HTTPException(status_code=404, detail="Subscription not detected")
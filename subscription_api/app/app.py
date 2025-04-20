from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from subscription_api.key_config_shaper import generate_config_key
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

        return config_key

    return HTTPException(status_code=404, detail="Subscription not detected")
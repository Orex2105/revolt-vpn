from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from subscription_api.subscription_api_helper import SubscriptionApiHelper
from dao.update_methods_dao import update_last_seen
from config import SubscriptionData
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

@app.api_route('/connection/sub/{user_uuid}', methods=["GET", "HEAD"], response_class=PlainTextResponse)
async def key_issuance(user_uuid: str):
    config_key = await SubscriptionApiHelper.generate_config_key(user_id=user_uuid)
    sub_data = SubscriptionData.get_subscription_data()

    if config_key is not None:
        update_last_seen_status = await update_last_seen(user_id=user_uuid)

        if not update_last_seen_status:
            logger.error(f"Не удалось обновить поле last_seen для пользователя {user_uuid}")

        headers = {
            "profile-web-page-url": sub_data.profile_web_page_url,
            "profile-title": sub_data.profile_title,
            "profile-update-interval": sub_data.update_interval,
            "support_url": sub_data.support_url,
            "announce": SubscriptionApiHelper.encode_title("#ad0901Тест!"),
            "announce-url": "https://t.me/rurevoltvpn",
        }
        return PlainTextResponse(content=config_key, headers=headers)

    raise HTTPException(status_code=404, detail="Subscription not detected")
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from subscription_api.subscription_api_helper import SubscriptionApiHelper
from config import SubscriptionApiData
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

@app.api_route(SubscriptionApiData.WEB_PATH+'{telegram_id}', methods=["GET", "HEAD"], response_class=PlainTextResponse)
async def key_issuance(telegram_id: str):
    config_key = await SubscriptionApiHelper.generate_config_key(telegram_id=telegram_id)

    if config_key is not None:
        client_data = await SubscriptionApiHelper.get_traffic(telegram_id=telegram_id)
        sub_data = SubscriptionApiData.get_subscription_data()
        headers = {
            "profile-web-page-url": sub_data.profile_web_page_url,
            "profile-title": sub_data.profile_title,
            "profile-update-interval": sub_data.update_interval,
            "support_url": sub_data.support_url,
            "announce": SubscriptionApiHelper.encode_title(sub_data.announce_text),
            "subscription-userinfo":
                f"upload={client_data.up}; download={client_data.down};"
                f"total={client_data.limitation}; expire={client_data.expiry_time}",
            "announce-url": sub_data.announce_url,
        }
        content = '\n'.join(config_key)

        if content is not None:
            return PlainTextResponse(content=content, headers=headers)
        else:
            HTTPException(status_code=404, detail="Error")

    return HTTPException(status_code=404, detail="Subscription not detected")
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
from subscription_api.key_config_shaper import generate_config_key
from dao.update_methods_dao import update_last_seen
from subscription_api.app.page import html_page
import logging

logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/connection/sub/{user_uuid}")
async def key_issuance(request: Request, user_uuid: str):
    config_key = await generate_config_key(user_id=user_uuid)
    if config_key is None:
        raise HTTPException(status_code=404, detail="Subscription not detected")

    update_ok = await update_last_seen(user_id=user_uuid)
    if not update_ok:
        logger.error(f"Не удалось обновить last_seen для {user_uuid}")

    accept = request.headers.get("accept", "")
    if "text/plain" in accept.lower():
        return PlainTextResponse(content=config_key, status_code=200)

    html_content = html_page(config_key=config_key)
    return HTMLResponse(content=html_content, status_code=200)
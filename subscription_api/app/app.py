from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from subscription_api.key_config_shaper import generate_config_key

app = FastAPI()

@app.get('/connection/sub/{user_uuid}', response_class=PlainTextResponse)
async def key_issuance(user_uuid: str):
    config_key = await generate_config_key(user_id=user_uuid)

    if config_key is None:
        raise HTTPException(status_code=404, detail="Subscription not detected")

    return config_key
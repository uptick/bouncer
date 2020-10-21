import base64
import json
import logging

from fastapi import FastAPI, HTTPException, Request
from starlette.responses import RedirectResponse


app = FastAPI()

logger = logging.getLogger('bouncer')


# Generic stateless reverse http proxy that derives it's redirect target from a state query parameter.
# The structure of the query parameter must be a base64 encoded json object with a `redirect_uri` key.
@app.get('/inbound/')
def make_auth_request(request: Request, state: str):
    logger.info("Inbound request received")
    try:
        # Decode state from b64 -> json -> python dict
        state_json = base64.b64decode(state).decode()
        state_dict = json.loads(state_json)
        redirect_uri = state_dict['redirect_uri']
    except base64.binascii.Error:
        logger.error(f"Error processing request, unable to b64 decode state: {state}")
        raise HTTPException(status_code=400, detail="Invalid state parameter (Could not decode b64)")
    except json.decoder.JSONDecodeError:
        logger.error(f"Error processing request, unable to json decode state: {state_json}")
        raise HTTPException(status_code=400, detail="Invalid state parameter (Could not decode json)")
    except KeyError:
        logger.error("Error processing request, state did not contain redirect_uri.")
        raise HTTPException(status_code=400, detail="Invalid state parameter (Missing redirect_uri)")
    # Redirect to target
    logger.info(f"Request successfully processed, redirecting to {redirect_uri}")
    return RedirectResponse(url=f'{redirect_uri}?{request.query_params}')

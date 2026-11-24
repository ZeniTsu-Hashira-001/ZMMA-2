import io
import logging
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import AnyHttpUrl
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from config import API_VERSION
from security import ensure_resources, limiter
from tools import brat, bw, reverse, welcome

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("zmma")

app = FastAPI(title="Zenitsu Multi Maker API", version=API_VERSION)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


def _png(data: bytes) -> StreamingResponse:
    return StreamingResponse(io.BytesIO(data), media_type="image/png")


# --- Health (non versionné, pour Render) ---
@app.get("/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok", "version": API_VERSION}


# --- Endpoints v1 ---
@app.post("/v1/brat", tags=["image"], dependencies=[Depends(ensure_resources)])
def brat_endpoint(
    text: str = Query(..., min_length=1, max_length=500),
    fg: str = Query("black"),
    bg: str = Query("white"),
    size: int = Query(512, ge=128, le=1024),
):
    try:
        data = brat.generate_brat(text=text, fg=fg, bg=bg, size=size)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        logger.exception("brat failed")
        raise HTTPException(status_code=500, detail="Internal error while generating image")
    return _png(data)


@app.post("/v1/reverse", tags=["image"], dependencies=[Depends(ensure_resources)])
def reverse_endpoint(url: AnyHttpUrl = Query(...)):
    try:
        data = reverse.generate_reverse(str(url))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        logger.exception("reverse failed")
        raise HTTPException(status_code=500, detail="Internal error while generating image")
    return _png(data)


@app.post("/v1/bw", tags=["image"], dependencies=[Depends(ensure_resources)])
def bw_endpoint(url: AnyHttpUrl = Query(...)):
    try:
        data = bw.generate_bw(str(url))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        logger.exception("bw failed")
        raise HTTPException(status_code=500, detail="Internal error while generating image")
    return _png(data)


@app.post("/v1/welcome", tags=["image"], dependencies=[Depends(ensure_resources)])
def welcome_endpoint(
    url: AnyHttpUrl = Query(...),
    username: str = Query(..., min_length=1, max_length=80),
    title: str = Query("Welcome", max_length=80),
    style: Literal["square", "round", "hex", "star", "heart"] = Query("square"),
):
    try:
        data = welcome.generate_welcome(
            url=str(url), username=username, title=title, style=style
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        logger.exception("welcome failed")
        raise HTTPException(status_code=500, detail="Internal error while generating image")
    return _png(data)
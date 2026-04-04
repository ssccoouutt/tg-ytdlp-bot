from __future__ import annotations

import pathlib
import logging
import os
from typing import Any, List
from fastapi import FastAPI, HTTPException, Query, Request, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware
from jinja2 import Environment, FileSystemLoader, select_autoescape

from CONFIG.config import Config
from services import stats_service
from services import system_service, lists_service
from services.auth_service import get_auth_service

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = pathlib.Path(__file__).resolve().parent

# Fix template caching - properly load templates from the templates folder
templates_dir = BASE_DIR / "templates"
static_dir = BASE_DIR / "static"

# Create Jinja2 environment with proper settings
env = Environment(
    loader=FileSystemLoader(str(templates_dir)),
    autoescape=select_autoescape(['html', 'xml']),
    cache_size=0  # Disable caching for Koyeb
)
templates = Jinja2Templates(env=env)

app = FastAPI(title="TG YTDLP Dashboard", version="1.0.0")

# Mount static files directory
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
else:
    logger.warning(f"Static directory not found: {static_dir}")

# CORS for API requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware to enforce authentication
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Public paths
        public_paths = ["/login", "/api/login", "/api/reset-lockdown", "/static", "/health", "/favicon.ico"]
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)
        
        # Read token from cookie
        token = request.cookies.get("auth_token")
        auth_service = get_auth_service()
        
        if not token or not auth_service.verify_token(token):
            if request.url.path.startswith("/api/"):
                raise HTTPException(status_code=401, detail="Unauthorized")
            return RedirectResponse(url="/login", status_code=302)
        
        response = await call_next(request)
        if request.url.path != "/api/logout":
            response.set_cookie(
                key="auth_token",
                value=token,
                httponly=True,
                secure=False,
                samesite="lax",
                max_age=auth_service.session_ttl,
            )
        return response


app.add_middleware(AuthMiddleware)


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page - uses login.html template"""
    try:
        return templates.TemplateResponse("login.html", {"request": request})
    except Exception as e:
        logger.error(f"Login template error: {e}")
        # Fallback HTML if template not found
        return HTMLResponse("""
        <html>
        <head><title>Login</title></head>
        <body>
            <h2>Login</h2>
            <form id="loginForm">
                <input type="text" id="username" placeholder="Username"><br>
                <input type="password" id="password" placeholder="Password"><br>
                <button type="submit">Login</button>
            </form>
            <script>
            document.getElementById('loginForm').onsubmit = async (e) => {
                e.preventDefault();
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        username: document.getElementById('username').value,
                        password: document.getElementById('password').value
                    })
                });
                if (res.ok) window.location.href = '/';
                else alert('Login failed');
            };
            </script>
        </body>
        </html>
        """)


class LoginRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


@app.post("/api/login")
async def api_login(payload: LoginRequest, request: Request):
    auth_service = get_auth_service()
    auth_service.reload_config()
    client_ip = request.client.host if request.client else "unknown"
    
    try:
        token = auth_service.login(payload.username, payload.password, client_ip)
        response = Response(content='{"status": "ok"}', media_type="application/json")
        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=auth_service.session_ttl,
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.post("/api/reset-lockdown")
async def api_reset_lockdown(request: Request):
    auth_service = get_auth_service()
    client_ip = request.client.host if request.client else "unknown"
    auth_service.reset_lockdown(client_ip)
    return {"status": "ok", "message": f"Lockdown reset for IP {client_ip}"}


@app.post("/api/logout")
async def api_logout(request: Request):
    token = request.cookies.get("auth_token")
    if token:
        auth_service = get_auth_service()
        auth_service.logout(token)
    response = Response(content='{"status":"ok"}', media_type="application/json")
    response.delete_cookie("auth_token")
    return response


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page - uses dashboard.html template"""
    try:
        # Pass config values to template
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "title": "Bot Statistics",
                "config": {
                    "STATS_ACTIVE_TIMEOUT": getattr(Config, "STATS_ACTIVE_TIMEOUT", 900),
                    "BOT_NAME": getattr(Config, "BOT_NAME", "TG YTDLP Bot"),
                    "DASHBOARD_PORT": getattr(Config, "DASHBOARD_PORT", 8000),
                }
            },
        )
    except Exception as e:
        logger.error(f"Dashboard template error: {e}")
        # Fallback HTML if template not found
        return HTMLResponse(f"""
        <html>
        <head>
            <title>TG YTDLP Bot Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .status {{ color: green; }}
            </style>
        </head>
        <body>
            <h1>🤖 TG YTDLP Bot Dashboard</h1>
            <p>Status: <span class="status">✅ Bot is running</span></p>
            <p>Bot Name: {getattr(Config, 'BOT_NAME', 'Unknown')}</p>
            <hr>
            <p><em>Dashboard template not found. Bot functionality is unaffected.</em></p>
            <a href="/login">Back to Login</a>
        </body>
        </html>
        """)


# ============ API Endpoints ============

@app.get("/api/active-users")
async def api_active_users(
    limit: int = 10,
    minutes: int | None = Query(default=None, ge=1, le=3600),
):
    try:
        return stats_service.fetch_active_users(limit=limit, minutes=minutes)
    except Exception as e:
        logger.error(f"Error in active-users: {e}")
        return []


@app.get("/api/top-downloaders")
async def api_top_downloaders(
    period: str = Query(default="today", pattern="^(today|week|month|all)$"),
    limit: int = 10,
):
    try:
        return stats_service.fetch_top_downloaders(period=period, limit=limit)
    except Exception as e:
        logger.error(f"Error in top-downloaders: {e}")
        return []


@app.get("/api/top-domains")
async def api_top_domains(period: str = "today", limit: int = 10):
    try:
        return stats_service.fetch_top_domains(period=period, limit=limit)
    except Exception as e:
        logger.error(f"Error in top-domains: {e}")
        return []


@app.get("/api/top-countries")
async def api_top_countries(period: str = "today", limit: int = 10):
    try:
        return stats_service.fetch_top_countries(period=period, limit=limit)
    except Exception as e:
        logger.error(f"Error in top-countries: {e}")
        return []


@app.get("/api/gender-stats")
async def api_gender_stats(period: str = "today"):
    try:
        return stats_service.fetch_gender_stats(period)
    except Exception as e:
        logger.error(f"Error in gender-stats: {e}")
        return {}


@app.get("/api/age-stats")
async def api_age_stats(period: str = "today"):
    try:
        return stats_service.fetch_age_stats(period)
    except Exception as e:
        logger.error(f"Error in age-stats: {e}")
        return {}


@app.get("/api/top-nsfw-users")
async def api_nsfw_users(limit: int = 10):
    try:
        return stats_service.fetch_top_nsfw_users(limit)
    except Exception as e:
        logger.error(f"Error in nsfw-users: {e}")
        return []


@app.get("/api/top-nsfw-domains")
async def api_nsfw_domains(limit: int = 10):
    try:
        return stats_service.fetch_top_nsfw_domains(limit)
    except Exception as e:
        logger.error(f"Error in nsfw-domains: {e}")
        return []


@app.get("/api/top-playlist-users")
async def api_playlist_users(limit: int = 10):
    try:
        return stats_service.fetch_top_playlist_users(limit)
    except Exception as e:
        logger.error(f"Error in playlist-users: {e}")
        return []


@app.get("/api/power-users")
async def api_power_users(min_urls: int = 10, days: int = 7, limit: int = 10):
    try:
        return stats_service.fetch_power_users(min_urls=min_urls, days=days, limit=limit)
    except Exception as e:
        logger.error(f"Error in power-users: {e}")
        return []


@app.get("/api/blocked-users")
async def api_blocked_users(limit: int = 50):
    try:
        return stats_service.fetch_blocked_users(limit)
    except Exception as e:
        logger.error(f"Error in blocked-users: {e}")
        return []


@app.get("/api/channel-events")
async def api_channel_events(hours: int = 48, limit: int = 100):
    try:
        return stats_service.fetch_recent_channel_events(hours=hours, limit=limit)
    except Exception as e:
        logger.error(f"Error in channel-events: {e}")
        return []


@app.get("/api/suspicious-users")
async def api_suspicious_users(
    period: str = Query(default="today", pattern="^(today|week|month|all)$"),
    limit: int = 20,
):
    try:
        return stats_service.fetch_suspicious_users(period=period, limit=limit)
    except Exception as e:
        logger.error(f"Error in suspicious-users: {e}")
        return []


@app.get("/api/user-history")
async def api_user_history(
    user_id: int = Query(..., gt=0),
    period: str = Query(default="all", pattern="^(today|week|month|all)$"),
    limit: int = Query(default=100, le=1000),
):
    try:
        return stats_service.fetch_user_history(user_id, period, limit)
    except Exception as e:
        logger.error(f"Error in user-history: {e}")
        return []


class BlockRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    reason: str | None = Field(default=None, max_length=120)


@app.post("/api/block-user")
async def api_block_user(payload: BlockRequest):
    try:
        stats_service.block_user(payload.user_id, reason=payload.reason or "manual")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "ok"}


@app.post("/api/unblock-user")
async def api_unblock_user(payload: BlockRequest):
    try:
        stats_service.unblock_user(payload.user_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "ok"}


@app.get("/api/system-metrics")
async def api_system_metrics():
    try:
        return system_service.get_system_metrics()
    except Exception as e:
        logger.error(f"Error in system-metrics: {e}")
        return {}


@app.get("/api/package-versions")
async def api_package_versions():
    try:
        return system_service.get_package_versions()
    except Exception as e:
        logger.error(f"Error in package-versions: {e}")
        return {}


@app.get("/api/config-settings")
async def api_config_settings():
    try:
        return system_service.get_config_settings()
    except Exception as e:
        logger.error(f"Error in config-settings: {e}")
        return {}


class ConfigUpdateRequest(BaseModel):
    key: str = Field(...)
    value: Any


@app.post("/api/update-config")
async def api_update_config(payload: ConfigUpdateRequest):
    try:
        success = system_service.update_config_setting(payload.key, payload.value)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to update config")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "ok"}


@app.get("/api/lists-stats")
async def api_lists_stats():
    try:
        return lists_service.get_lists_stats()
    except Exception as e:
        logger.error(f"Error in lists-stats: {e}")
        return {}


@app.get("/api/domain-lists")
async def api_domain_lists():
    try:
        return lists_service.get_domain_lists()
    except Exception as e:
        logger.error(f"Error in domain-lists: {e}")
        return {}


class DomainListUpdateRequest(BaseModel):
    list_name: str = Field(...)
    items: List[str] = Field(...)


@app.post("/api/update-domain-list")
async def api_update_domain_list(payload: DomainListUpdateRequest):
    try:
        success = lists_service.update_domain_list(payload.list_name, payload.items)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to update domain list")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "ok"}


@app.post("/api/rotate-ip")
async def api_rotate_ip():
    try:
        return system_service.rotate_ip()
    except Exception as e:
        logger.error(f"Error in rotate-ip: {e}")
        return {"status": "error", "message": str(e)}


@app.post("/api/restart-service")
async def api_restart_service():
    try:
        return system_service.restart_service()
    except Exception as e:
        logger.error(f"Error in restart-service: {e}")
        return {"status": "error", "message": str(e)}


@app.post("/api/update-engines")
async def api_update_engines():
    try:
        return system_service.update_engines()
    except Exception as e:
        logger.error(f"Error in update-engines: {e}")
        return {"status": "error", "message": str(e)}


@app.post("/api/cleanup-user-files")
async def api_cleanup_user_files():
    try:
        return system_service.cleanup_user_files()
    except Exception as e:
        logger.error(f"Error in cleanup-user-files: {e}")
        return {"status": "error", "message": str(e)}


@app.post("/api/update-lists")
async def api_update_lists():
    try:
        return lists_service.update_lists()
    except Exception as e:
        logger.error(f"Error in update-lists: {e}")
        return {"status": "error", "message": str(e)}


@app.get("/health")
async def health():
    return {"status": "ok", "bot": "running"}


@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

from __future__ import annotations

import pathlib
import logging
import os
import re
from typing import Any, List, Dict, Optional
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

# Fix template caching issue - disable cache
try:
    env = Environment(
        loader=FileSystemLoader(str(BASE_DIR / "templates")),
        autoescape=select_autoescape(['html', 'xml']),
        cache_size=0
    )
    templates = Jinja2Templates(env=env)
except Exception:
    templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
    if hasattr(templates, 'env') and hasattr(templates.env, 'cache'):
        templates.env.cache = {}

app = FastAPI(title="TG YTDLP Dashboard", version="1.0.0")

static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = ["/login", "/api/login", "/api/reset-lockdown", "/static", "/health", "/favicon.ico"]
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)
        
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
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TG YTDLP Bot - Login</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .login-container {
                background: white;
                border-radius: 10px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.2);
                padding: 40px;
                width: 100%;
                max-width: 400px;
                margin: 20px;
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 30px;
                font-size: 28px;
            }
            .logo {
                text-align: center;
                font-size: 48px;
                margin-bottom: 20px;
            }
            input {
                width: 100%;
                padding: 12px 15px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
                transition: border-color 0.3s;
            }
            input:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 20px;
                transition: transform 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
            }
            .error {
                color: #e74c3c;
                text-align: center;
                margin-top: 15px;
                display: none;
            }
            .info {
                text-align: center;
                margin-top: 20px;
                color: #666;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">🤖</div>
            <h1>TG YTDLP Bot</h1>
            <form id="loginForm">
                <input type="text" id="username" placeholder="Username" required autofocus>
                <input type="password" id="password" placeholder="Password" required>
                <div class="error" id="errorMsg">Invalid credentials</div>
                <button type="submit">Login</button>
            </form>
            <div class="info">
                Default credentials: admin / admin123<br>
                (Change in config.py)
            </div>
        </div>
        
        <script>
            const form = document.getElementById('loginForm');
            const errorMsg = document.getElementById('errorMsg');
            
            form.onsubmit = async (e) => {
                e.preventDefault();
                errorMsg.style.display = 'none';
                
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                try {
                    const res = await fetch('/api/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, password })
                    });
                    
                    if (res.ok) {
                        window.location.href = '/';
                    } else {
                        errorMsg.style.display = 'block';
                    }
                } catch (err) {
                    errorMsg.style.display = 'block';
                }
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


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
    """Main dashboard page"""
    try:
        # Get bot info from config
        bot_name = getattr(Config, "BOT_NAME", "TG YTDLP Bot")
        admin_list = getattr(Config, "ADMIN", [])
        admin_id = str(admin_list[0]) if admin_list else "Not set"
        dashboard_port = getattr(Config, "DASHBOARD_PORT", 8000)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>TG YTDLP Bot Dashboard</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{ box-sizing: border-box; }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    margin: 0;
                    padding: 0;
                    background: #f5f5f5;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .header h1 {{ margin: 0; font-size: 24px; }}
                .header p {{ margin: 5px 0 0; opacity: 0.9; }}
                .nav {{
                    background: white;
                    padding: 10px 20px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }}
                .nav a {{
                    color: #667eea;
                    text-decoration: none;
                    margin-right: 20px;
                    padding: 5px 10px;
                    border-radius: 5px;
                }}
                .nav a:hover {{ background: #f0f0f0; }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 0 20px;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .stat-card {{
                    background: white;
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    text-align: center;
                }}
                .stat-value {{
                    font-size: 36px;
                    font-weight: bold;
                    color: #667eea;
                }}
                .stat-label {{
                    color: #666;
                    margin-top: 10px;
                }}
                .card {{
                    background: white;
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .card h3 {{ margin-top: 0; color: #333; }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #eee;
                }}
                th {{ background: #f8f8f8; }}
                .status {{ color: #4caf50; font-weight: bold; }}
                button {{
                    background: #667eea;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    margin-right: 10px;
                }}
                button:hover {{ background: #5a67d8; }}
                .refresh-btn {{
                    background: #4caf50;
                    margin-bottom: 20px;
                }}
                .logout-btn {{
                    background: #e74c3c;
                }}
                .loading {{ text-align: center; padding: 20px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🤖 {bot_name}</h1>
                <p>Telegram Download Bot Dashboard</p>
            </div>
            <div class="nav">
                <a href="/">Dashboard</a>
                <a href="#" onclick="refreshAll()">Refresh</a>
                <button class="logout-btn" onclick="logout()" style="float: right;">Logout</button>
            </div>
            
            <div class="container">
                <button class="refresh-btn" onclick="refreshAll()">🔄 Refresh All Stats</button>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value" id="activeUsers">-</div>
                        <div class="stat-label">Active Users (24h)</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="totalDownloads">-</div>
                        <div class="stat-label">Total Downloads</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="blockedUsers">-</div>
                        <div class="stat-label">Blocked Users</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="uptime">-</div>
                        <div class="stat-label">Bot Uptime</div>
                    </div>
                </div>
                
                <div class="card">
                    <h3>📊 Top Downloaders</h3>
                    <div id="topDownloaders" class="loading">Loading...</div>
                </div>
                
                <div class="card">
                    <h3>🌐 Top Domains</h3>
                    <div id="topDomains" class="loading">Loading...</div>
                </div>
                
                <div class="card">
                    <h3>🔞 NSFW Stats</h3>
                    <div id="nsfwStats" class="loading">Loading...</div>
                </div>
                
                <div class="card">
                    <h3>⚙️ System Info</h3>
                    <div id="systemInfo" class="loading">Loading...</div>
                </div>
            </div>
            
            <script>
                async function fetchJSON(url) {{
                    try {{
                        const res = await fetch(url);
                        if (!res.ok) throw new Error(await res.text());
                        return await res.json();
                    }} catch(e) {{
                        console.error(url, e);
                        return null;
                    }}
                }}
                
                async function loadActiveUsers() {{
                    const data = await fetchJSON('/api/active-users?limit=1');
                    if (data && Array.isArray(data)) {{
                        document.getElementById('activeUsers').innerText = data.length;
                    }}
                }}
                
                async function loadTopDownloaders() {{
                    const data = await fetchJSON('/api/top-downloaders?period=all&limit=10');
                    const container = document.getElementById('topDownloaders');
                    if (data && Array.isArray(data) && data.length) {{
                        let html = '<table><tr><th>User ID</th><th>Downloads</th></tr>';
                        data.forEach(item => {{
                            html += `<tr><td>${{item.user_id || 'Unknown'}}</td><td>${{item.count || 0}}</td></tr>`;
                        }});
                        html += '</table>';
                        container.innerHTML = html;
                    }} else {{
                        container.innerHTML = '<p>No data available</p>';
                    }}
                }}
                
                async function loadTopDomains() {{
                    const data = await fetchJSON('/api/top-domains?period=all&limit=10');
                    const container = document.getElementById('topDomains');
                    if (data && Array.isArray(data) && data.length) {{
                        let html = 'table><tr><th>Domain</th><th>Downloads</th></tr>';
                        data.forEach(item => {{
                            html += `<tr><td>${{item.domain || 'Unknown'}}</td><td>${{item.count || 0}}</td></tr>`;
                        }});
                        html += '</table>';
                        container.innerHTML = html;
                    }} else {{
                        container.innerHTML = '<p>No data available</p>';
                    }}
                }}
                
                async function loadNSFWStats() {{
                    const data = await fetchJSON('/api/top-nsfw-users?limit=10');
                    const container = document.getElementById('nsfwStats');
                    if (data && Array.isArray(data) && data.length) {{
                        let html = 'table><tr><th>User ID</th><th>NSFW Requests</th></tr>';
                        data.forEach(item => {{
                            html += `<tr><td>${{item.user_id || 'Unknown'}}</td><td>${{item.count || 0}}</td></tr>`;
                        }});
                        html += '</table>';
                        container.innerHTML = html;
                    }} else {{
                        container.innerHTML = '<p>No NSFW data available</p>';
                    }}
                }}
                
                async function loadSystemInfo() {{
                    const container = document.getElementById('systemInfo');
                    container.innerHTML = `
                        <p><strong>Bot Name:</strong> {bot_name}</p>
                        <p><strong>Admin ID:</strong> {admin_id}</p>
                        <p><strong>Dashboard Port:</strong> {dashboard_port}</p>
                        <p><strong>Status:</strong> <span class="status">✅ Online</span></p>
                    `;
                }}
                
                async function loadBlockedUsers() {{
                    const data = await fetchJSON('/api/blocked-users?limit=1');
                    if (data && Array.isArray(data)) {{
                        document.getElementById('blockedUsers').innerText = data.length;
                    }}
                }}
                
                async function refreshAll() {{
                    document.getElementById('topDownloaders').innerHTML = '<div class="loading">Loading...</div>';
                    document.getElementById('topDomains').innerHTML = '<div class="loading">Loading...</div>';
                    document.getElementById('nsfwStats').innerHTML = '<div class="loading">Loading...</div>';
                    
                    await Promise.all([
                        loadActiveUsers(),
                        loadTopDownloaders(),
                        loadTopDomains(),
                        loadNSFWStats(),
                        loadSystemInfo(),
                        loadBlockedUsers()
                    ]);
                }}
                
                async function logout() {{
                    await fetch('/api/logout', {{ method: 'POST' }});
                    window.location.href = '/login';
                }}
                
                refreshAll();
                setInterval(refreshAll, 30000);
            </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return HTMLResponse(f"""
        <html>
        <head><title>Dashboard</title></head>
        <body>
            <h1>🤖 Bot Dashboard</h1>
            <p>Bot is running! Error: {str(e)}</p>
            <a href="/login">Back to Login</a>
        </body>
        </html>
        """, status_code=200)


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

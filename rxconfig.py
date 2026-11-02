import os
import reflex as rx

# Automatically detect Render's external URL or explicit API_URL if deployed on Render
_external_api_url = os.getenv("API_URL") or os.getenv("RENDER_EXTERNAL_URL")

_config_kwargs = {
    "app_name": "gradwyn",
    "db_url": os.getenv("DB_URL", "sqlite:///gradwyn.db"),
    "plugins": [
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV3Plugin(
            config={
                "theme": {
                    "extend": {
                        "fontFamily": {
                            "sans": ["Inter", "system-ui", "-apple-system", "sans-serif"],
                            "serif": ["Playfair Display", "Georgia", "serif"],
                        },
                        "colors": {
                            "brand": {
                                "50": "#f8fafc",
                                "100": "#f1f5f9",
                                "200": "#e2e8f0",
                                "300": "#cbd5e1",
                                "400": "#94a3b8",
                                "500": "#64748b",
                                "600": "#475569",
                                "700": "#334155",
                                "800": "#1e293b",
                                "900": "#0f172a",
                            }
                        },
                    }
                }
            }
        ),
    ],
}

if _external_api_url:
    _config_kwargs["api_url"] = _external_api_url

config = rx.Config(**_config_kwargs)

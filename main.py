import json
from rich.console import Console
from pathlib import Path

console = Console()
config_file = Path(__file__).parent / "config.json"

with open(config_file, "r", encoding="utf-8") as handler:
    config = json.load(handler)

_config = {
    "404_page": "<title>Not Found</title> <body><h1>404 Webpage Not Found</h1><p>Please Verify the URL and try again.</p></body><br><br><h3>If you are the owner of this site</h3><br><p>There is no hostname configured to serve for this domain, please check your configuration file or view the <a href='https://proxy-docs.minecraft-security.com'>docs</a>.<br><a href='https://github.com/Minecraft-Security/reverse_proxy'>View Source</a><p>"
}

projects = {}


def validate_config():
    if config["404_page"] != "":
        try:
            file = Path(config["404_page"])
            with open(file, "r", encoding="utf-8") as handler:
                _config["404_page"] = handler.read()
        except Exception as exc:
            console.print_exception(show_locals=True)
            console.log("Error parsing 404 page, please check your config.")
            return False

    if len(config["projects"]) == 0:
        console.log(
            "[red]Error[/red]\nYou must add atleast one project to the projects array."
        )
        return False

    for project in config["projects"]:
        hostname = project.get("hostname", "unnamed_project")

        if "hostname" not in project:
            console.log(
                f"[red]Error[/red], {hostname} must have a hostname. Please check your config."
            )

        if "serve" not in project:
            console.log(
                f"[red]Error, {hostname} doesn't have the `serve` field. Please check your config."
            )
            return False

        projects[hostname] = {"serve": project["serve"]}

    return True


validate_config()

import aiohttp
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()
session = []


@app.on_event("startup")
async def startup():
    console.log("Reverse Proxy started")
    console.log(projects)
    session.append(aiohttp.ClientSession())
    console.rule("Initiated")


@app.api_route(
    "/{path_name:path}",
    methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "HEAD",
        "OPTIONS",
        "PATCH",
        "TRACE",
        "CONNECT",
    ],
)
async def catch_all(request: Request, path_name: str):
    root_path = (
        str(request.url)
        .lower()
        .replace("http", "")
        .replace("https", "")
        .replace("://", "")
        .split("/")[0]
    )  # gets host of website being accessed (ex - google.com)

    serve_at = projects.get(root_path)
    if serve_at is None:
        return HTMLResponse(content=_config["404_page"], status_code=404)
    serve_at = serve_at.get("serve")

    async with session[0].request(
        method=request.method,
        url=str(serve_at) + "/" + path_name,
        headers=request.headers,
    ) as response:
        return HTMLResponse(
            await response.read(), status_code=response.status, headers=response.headers
        )


if __name__ == "__main__":
    import os, uvicorn

    uvicorn.run(
        f"{os.path.basename(__file__).replace('.py', '')}:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 80)),
    )

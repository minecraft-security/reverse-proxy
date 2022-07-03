import json
from rich.console import Console
from pathlib import Path

console = Console()
config_file = Path(__file__).parent / "config.json"

with open(config_file, "r", encoding="utf-8") as handler:
    config = json.load(handler)

_config = {
    "404_page": "<hostname>Not Found</hostname> <body><h1>404 Webpage Not Found</h1><br><p>Please Verify the URL and try again.</p></body>"
}

projects = {}


def validate_config():
    if config['404_age'] != "":
        try:
            file = Path(config['404_page'])
            with open(file, "r", encoding="utf-8") as handler:
                _config['404_page'] = handler.read()
        except Exception as exc:
            console.print_exception(show_locals=True)
            console.log("Error parsing 404 page, please check your config.")
            return False
        
    if len(config['projects']) == 0:
        console.log("[red]Error[/red]\nYou must add atleast one project to the projects array.")
        return False
    
    for project in config['projects']:
        hostname = project.get('hostname', 'unnamed_project')

        if "hostname" not in project:
            console.log(f"[red]Error[/red], {hostname} must have a hostname. Please check your config.")

        if "serve" not in project:
            console.log(f"[red]Error, {hostname} doesn't have the `serve` field. Please check your config.")
            return False
        
        projects[hostname] = {
            "serve": project['serve']
        }
    
    return True

validate_config()

import aiohttp
from fastapi import FastAPI, Request

app = FastAPI()
session = []

@app.on_event("startup")
async def startup():
    console.log("Reverse Proxy started")
    console.log(projects)
    session.append(aiohttp.ClientSession())
    console.rule("Initiated")

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH", "TRACE", "CONNECT"])
async def catch_all(request: Request, path_name: str):
    root_path = request.url.path # gets host of website being accessed (ex - google.com)
    console.log(root_path)

    serve_at = projects.get(root_path)
    if serve_at is None:
        return _config['404_page']
    serve_at = serve_at.get("serve")

    async with session[0].request(method=request.method, url=str(serve_at) + path_name, headers=request.headers) as response:
        return response

if __name__ == "__main__":
    import os, uvicorn
    uvicorn.run(f"{os.path.basename(__file__).replace('.py', '')}:app", host="0.0.0.0", port=int(os.environ.get("PORT", 80)))
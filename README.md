## Python Proxy

Tired of trying to figure out how nginx works? What about apache? Yeah, me too.

I made this project because I didn't want to deal with massive configuration files, it allows you to run multiple dynamic websites/servers (Think Flask, FastAPI, Quart applications, etc. Anything that you can access via the HTTP Protocol.), and access all of them on port 80 by determining the name/url of the user requesting it.

For example, I have two websites running on one machine, `a.com` on port 3000, and `b.com` on port 5000. Since I can't natively run two websites on machine, I need to use something to serve the correct application based on what url is being accessed. This application
- Request on `a.com`
- Sends a request to `localhost:3000`
- Relays content back to user
Headers, cookies are preserved on all requests.

#### Deploying

```
git clone https://github.com/minecraft-security/reverse-proxy reverse_proxy
cd reverse_proxy
pip install -r requirements.txt
nano config.json
python3 main.py
```

- Clone the repository and CD into it
- Install the requirements (`requirements.txt`)
- Modify the configuration file to suit your needs
- Run `main.py`

You need to restart the program for any modifications in the configuration to take effect. This program was tested only on `Python 3.10.4` but should support earlier versions of Python 3 as well.


#### Configuring

```json
{
    "404_page": "",
    "projects": []
}
```
This is an empty configuration, `404_page` is a path to a HTML File that's rendered when someone accesses a domain you haven't configured yet. Ex, `c.com`, which is running on the machine but not added to the configuration yet.

Projects is a list of dictionaries containing the URL (`a.com`, `b.com`), and where to serve from (`localhost:3000`, `localhost:5000`)

```json
{
    "404_page": "",
    "projects": [
        {
            "hostname": "a.com",
            "serve": "http://localhost:3000"
        },
        {
            "hostname": "b.com",
            "serve": "http://localhost:5000"
        }
    ]
}
```

Example implementation -
- Running my FastAPI/dynamic service on localhost:3000, and mapping my domain to it as a project.
- Deploying this service on my machine, on port 80
- Setting a DNS Record to point from my domain to this machine (A Record)
- Whenever someone accesses my domain, they're served this reverse proxy, which determines which domain they've used to access the program, and serve the proper content.

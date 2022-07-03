## Python Proxy

Tired of trying to figure out how nginx works? What about apache? Yeah, me too.

This project lets you host your dynamic websites on different ports on localhost, and serves the correct page based on the hostname. 

For example, if I have two websites, `a.com` and `b.com`, and need to run them on the same machine, I'd use something like this.

I would add `a.com` and `b.com` as elements in the projects array (in the config file), and write the url that's to be served alongside it.

**Note**: This may sound a bit complicated, but in implementation, it's much easier. I also might've over-explained it a bit.

```json
{
    "404_page": "",
    "projects": []
}
```
This is an empty configuration,
- `404_page` can either be empty, or should be a path to a static HTML file to render and serve if the domain input by the user points to your machine, but there's no relevant entry for the domain in your configuration file. ie, another website, `c.com` points to your machine, but you've only added relevant entries in the configuration file for `a.com` and `b.com`, in such a situation, this page is rendered and served.
- `projects`. is an array of projects, a project is structured like
```json
{
    "hostname": "base url of website",
    "serve": "the url of the webpage to serve"
}
```
An example project would look like
```json
{
    "hostname": "write.theonlywayup.live",
    "serve": "http://localhost:3000"
}
```
Hostname is the root url of the website, and serve is the URL of the webpage to be served. The hostname's DNS should point toward your server, when I visit `write.theonlywayup.live`, I'll get redirected to the machine this script is being run on, the script will determine what website was used to access it (in this case, `write.theonlywayup.live`). With the hostname, the appropriate URL to serve from is found, a request is sent to it through the backend, and the response is relayed back to the user.

Example implementation -
- Running my FastAPI/dynamic service on localhost:3000, and mapping my domain to it as a project.
- Deploying this service on my machine, on port 80
- Setting a DNS Record to point from my domain to this machine (A Record)
- Whenever someone accesses my domain, they're served this reverse proxy, which determines which domain they've used to access the program, and serve the proper url.
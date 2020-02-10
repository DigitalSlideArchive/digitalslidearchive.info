## Setting up an NGINX Proxy

This is.. always confusing.  But we do/can support proxies via DSA.  The full information is here.

Briefly, when you start the DSA services, you need to let the docker configuration know that you are going to proxy certain ports/services.  For example, girder runs on port 8080, but in many setup's I've found it easier to not 


It turns out that as of Girder 3 there is an additional setting needed to route proxies with paths.  I've caused the readthedocs to be updated:  https://girder.readthedocs.io/en/latest/deploy.html#reverse-proxy   .  Specifically, you need to add static_public_path = "/girder/static", rebuild the web client ("girder build --dev"), and restart girder.
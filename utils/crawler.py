import gzip
from urllib.request import Request
import urllib.request


def crawl(url, charset="gbk", timeout=10):
    request = Request(url, headers={'Accept-Encoding' : 'compress, gzip'})
    try:
        response = urllib.request.urlopen(request, timeout=timeout)
        if response.getheader("Content-Encoding") == "gzip":
            return gzip.decompress(response.read()).decode(charset)
        else:
            return response.read().decode(charset)
    except:
        print("error for url %s" % url)
        return None
    finally:
        response.close()
    
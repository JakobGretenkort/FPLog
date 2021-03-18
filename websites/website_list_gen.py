import concurrent.futures
import csv
from fake_useragent import UserAgent
import re
import requests
import socket
import sys
import tldextract
from urllib.parse import urlparse

PROTO = ['http://', 'https://']
PREFIX = ['', 'www.']
PATH = ['/']

IN_FILE = "top-1m.csv"
OUT_FILE = "website-list.csv"

TARGET = 15000

MT_SPLIT = 100

THREADS = 32

HEADERS = {'User-Agent': UserAgent().chrome}

def main():
  results = []

  print("starting threads")
  with concurrent.futures.ProcessPoolExecutor(max_workers=THREADS) as executor:
    futures = executor.map(thread_main, range(1, TARGET, MT_SPLIT))
    for result in futures:
      results.extend(result)

  print("sorting results")
  results.sort()

  print("writing results")
  with open(OUT_FILE, "w", newline='') as out_file:
    writer = csv.writer(out_file, delimiter=',')

    for entry in results:
      writer.writerow(entry)

def thread_main(index):
  print(str(index), "Starting")
  results = []

  with open(IN_FILE, "r", newline='') as in_file:
    reader = csv.reader(in_file, delimiter=',')

    for i in range(1, index):
      # skip a couple of lines from the file
      next(reader)

    for row in reader:
      if int(row[0]) >= index + MT_SPLIT:
        break
      domain = row[1]
      result = try_domain(domain)
      if result:
        results.append((int(row[0]), result))
  return results

def try_domain(domain):
  #for regex in DOMAIN_RE:
  #  if regex.search(domain):
  #    return None
  for proto in PROTO:
    for prefix in PREFIX:
      for path in PATH:
        url = proto + prefix + domain + path
        result = try_url(url)
        if result:
          return result
  return None

def try_url(url, redirects=0):
  if redirects >= 50:
    return None
  try:
    resp = requests.get(url, timeout=30, allow_redirects=False, headers=HEADERS)
    status_code = resp.status_code

    if status_code in [200]:
      if ('content-type' in resp.headers and
          resp.headers['content-type'].startswith('text/html')):
        return try_website(url, resp.text, redirects)
      else:
        return None

    if status_code in [201]:
      # created, probably not what we are looking for
      code_err(status_code, url)
      return None

    elif status_code in [204]:
      # no content
      code_err(status_code, url)
      return None

    elif status_code in [301, 302, 303, 307, 308]:
      # redirect
      if('location' in resp.headers):
        redirect = resp.headers['location']
        scheme = urlparse(url).scheme
        origin_domain = urlparse(url).hostname
        redirect_domain = urlparse(redirect).hostname
        origin_paylevel = tldextract.extract(origin_domain).domain
        redirect_paylevel = tldextract.extract(redirect_domain).domain

        if redirect_domain == "" and redirect.startswith('/'):
          # relative path!
          redirect = scheme + '://' + origin_domain + redirect
          return try_url(redirect, redirects + 1)
        if (origin_domain == redirect_domain or origin_paylevel == redirect_paylevel):
          return try_url(redirect, redirects + 1)
      return None

    elif status_code in [304]:
      # not modified: apparently, we already requested this?
      code_err(status_code, url)
      return None

    elif status_code in [400]:
      # malformed request: usually means unsupported head/get request
      code_err(status_code, url)
      return None

    elif status_code in [401, 404]:
      # can't do anything about any of these
      code_err(status_code, url)
      return None

    elif status_code in [403]:
      # They may have figured out that we are a bot. Maybe we should try
      # going to this site with our browser anyways?
      code_err(status_code, url)
      return None

    elif status_code in [405]:
      # method not allowed
      code_err(status_code, url)
      return None

    elif status_code in [406]:
      ## TODO
      # not acceptable: maybe modify our accept header?
      code_err(status_code, url)
      return None

    elif status_code in [407]:
      # proxy auth required
      code_err(status_code, url)
      return None

    elif status_code in [409]:
      # conflict: multiple clients accessing a resource? Nothing we can do.
      code_err(status_code, url)
      return None

    elif status_code in [410]:
      # gone: nothing we can do here
      code_err(status_code, url)
      return None

    elif status_code in [411]:
      # length required: should not be required for html
      code_err(status_code, url)
      return None

    elif status_code in [413]:
      # payload to large
      code_err(status_code, url)
      return None

    elif status_code in [415]:
      ## TODO
      # media type not supported: perhaps ask for text/html explicitly?
      code_err(status_code, url)
      return None

    elif status_code in [416]:
      # range not satisfiable: we are asking for a portion of a file?
      code_err(status_code, url)
      return None

    elif status_code in [418]:
      # teapot, probably a joke returned for head-only requests?
      code_err(status_code, url)
      return None

    elif status_code in [421]:
      # misdirect: server cannot produce response
      code_err(status_code, url)
      return None

    elif status_code in [422]:
      # unprocessable entity
      code_err(status_code, url)
      return None

    elif status_code in [426]:
      ## TODO
      # upgrade required: should probably do something here
      code_err(status_code, url)
      return None

    elif status_code in [429]:
      code_err(status_code, url)
      return None

    elif status_code in [500, 502, 503, 504, 508]:
      # serverside, nothing we can do
      code_err(status_code, url)
      return None

    elif status_code in [501]:
      # not implemented.
      code_err(status_code, url)
      return None

    elif status_code in [240, 440, 470, 477, 478, 520, 521, 523, 525, 526, 530, 592]:
      # unofficial code. I can't be bothered to deal with these as well
      code_err(status_code, url)
      return None

    else:
      code_err(status_code, url)

  except (requests.ConnectionError):
    # eprint("Conn fail : " + url)
    return None
  except (requests.exceptions.Timeout, socket.timeout):
    # eprint("Timeout   : " + url)
    return None
  except (requests.exceptions.MissingSchema):
    # Followed bad redirect, try to recover
    parse = urlparse(url)
    return try_url(PROTO[1] + parse.netloc + parse.path, redirects + 1)
    # eprint("Schema    : " + url)
  except requests.exceptions.RequestException as e:
    eprint("Some Exc  : " + url)
    return None

def try_website(url, text, redirects):
  return url

def code_err(status_code, url):
  eprint("Error " + str(status_code) + " : " + url)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if __name__ == '__main__':
  main()
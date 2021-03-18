import csv
from urllib.parse import urlparse

IN_FILE = "data_raw.csv"
URL_FILE = "url.csv"
OUT_FILE = "data_resolved.csv"

def domain(url):
  return urlparse(url).hostname

def set_origin(origins, embedded, embedder):
  if embedder == "":
    # direct call from user
    origins[domain(embedded)] = embedded
  else:
    # iframe
    origins[domain(embedded)] = origins[domain(embedder)]

def main():
  origins = {}

  with open(IN_FILE, "r", newline='', encoding='utf8') as in_file, \
       open(URL_FILE, "r", newline='', encoding='utf8') as url_file, \
       open(OUT_FILE, "w", newline='', encoding='utf8') as out_file:
    reader = csv.reader(in_file, delimiter=',')
    url_reader = csv.reader(url_file, delimiter=',')
    writer = csv.writer(out_file, delimiter=',')

    url_row = next(url_reader)

    for row in reader:
      while int(url_row[0]) <= int(row[0]):
        set_origin(origins, url_row[1], url_row[2])
        try:
          url_row = next(url_reader)
        except StopIteration as e:
          break
      set_origin(origins, row[1], row[2])

      origin = origins[domain(row[1])]

      new_row = row[0:3] + [origin] + row[3:]

      writer.writerow(new_row)

if __name__ == '__main__':
  main()
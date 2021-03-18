SET search_path = fplog;

-- Complete list of visited URLs
CREATE TABLE url AS
SELECT DISTINCT a.url
  FROM access AS a
 WHERE a.parent IS NULL
 UNION
SELECT DISTINCT f.url
  FROM font AS f
 WHERE f.parent IS NULL;
-- 10542 results.

-- Font count for every visited url
CREATE VIEW font_count AS
SELECT u.url, count(DISTINCT f.fontname) AS font_count
  FROM font AS f
  RIGHT JOIN url AS u
     ON f.top = u.url
 WHERE f.priority = 0
    OR f.top IS NULL
 GROUP BY u.url

-- Font usage histogram (Ignores 4 pages with only fonts of prio >= 1)
-- Only up to count 20
SELECT fc.font_count, count(*) AS page_count
  FROM font_count AS fc
 GROUP BY fc.font_count
 ORDER BY fc.font_count;

-- Font usage histogram (Ignores 4 pages with only fonts of prio >= 1)
-- Clustered
-- Only up to count 120
SELECT s.num AS font_count, SUM(pc.page_count) AS page_count
  FROM (SELECT generate_series(0, 700, 10) AS num) AS s
  LEFT JOIN (SELECT fc.font_count, count(*) AS page_count
               FROM font_count AS fc
              GROUP BY fc.font_count
              ORDER BY fc.font_count) AS pc
    ON s.num <= pc.font_count
   AND s.num + 10 > pc.font_count
 GROUP BY s.num
HAVING s.num <= 120

-- Count of sites with fc > 25
SELECT count(*) AS page_count
  FROM font_count AS fc
  WHERE fc.font_count > 25;
-- 263

-- For case studies
SELECT *
  FROM font_count AS fc
 WHERE fc.font_count > 25;

-- For case studies
SELECT * FROM fplog.font AS f WHERE f.priority = 0 AND f.top = 'https://onlyfans.com/';

-- What are the surfaces?
CREATE VIEW surface AS
SELECT DISTINCT a.object, a.accessed, a.parameters
  FROM access AS a;

-- Top url access
CREATE VIEW access_top AS
SELECT DISTINCT u.url, a.object, a.accessed, a.parameters
  FROM url AS u
 INNER JOIN access AS a
    ON u.url = a.top

-- How many sites use a surfaces?
SELECT a.object, a.accessed, a.parameters, COUNT(DISTINCT a.url)
 FROM access_top AS a
 GROUP BY a.object, a.accessed, a.parameters

-- URLs with virtual access to userAgent surface
CREATE VIEW access_ua AS
SELECT DISTINCT a.url, 'navigator' AS object, 'UA' AS accessed, NULL AS parameters
  FROM access_top AS a
 WHERE a.accessed IN ('appName', 'appVersion', 'cpuClass', 'platform', 'productSub', 'vendor')
 GROUP BY a.url
HAVING COUNT(DISTINCT a.accessed) >= 5
-- 1099 results

-- URLs with virtual access to webgl surface
CREATE VIEW access_webgl AS
SELECT DISTINCT a.url, 'HTMLCanvasElement.prototype' AS object, 'getContext' AS accessed, 'webgl' AS parameters
  FROM access_top AS a
 WHERE a.parameters IN ('webgl', 'webgl2', 'experimental-webgl', 'experimental-webgl2', 'moz-webgl', 'webkit-3d')
 GROUP BY a.url
-- 2203 results

-- URLs which access local or session storage
CREATE VIEW access_storage AS
SELECT DISTINCT a.url, 'window' AS object, 'storage' AS accessed, NULL AS parameters
  FROM access_top AS a
 WHERE a.accessed IN ('localStorage', 'sessionStorage')
 GROUP BY a.url

-- URLs wich access a certain number of fonts
CREATE VIEW access_fonts AS
SELECT DISTINCT fc.url, 'rendering' AS object, 'font' AS accessed, fc.font_count::varchar(255) AS parameters
  FROM font_count fc

-- URLs with access to virtual or real surfaces
CREATE VIEW access_complete AS
SELECT * FROM access_top
 UNION
SELECT * FROM access_ua
 UNION
SELECT * FROM access_webgl
 UNION
SELECT * FROM access_storage
 UNION
SELECT * FROM access_fonts
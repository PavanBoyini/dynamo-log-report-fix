There is an Apache-style access log at `/app/access.log`. Analyze the traffic
and write your findings to `/app/report.json` as a single JSON object with
exactly these keys:

- `total_requests` (integer): the total number of request lines in the log.
- `unique_ips` (integer): the number of distinct client IP addresses that
  made requests.
- `top_path` (string): the request path (e.g. `/index.html`) that was
  requested more often than any other path.

Write valid JSON only — no extra keys, no trailing commentary.

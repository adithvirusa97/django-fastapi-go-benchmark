import os, time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from psycopg_pool import ConnectionPool

app = FastAPI(title='FastAPI Benchmark')
pool = ConnectionPool(conninfo=f"host={os.getenv('DB_HOST')} port={os.getenv('DB_PORT')} dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASSWORD')}", min_size=2, max_size=10, open=False)
REQUESTS = Counter('http_requests_total', 'Total HTTP requests', ['method', 'path', 'status'])
LATENCY = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'path'])

@app.on_event('startup')
def startup(): pool.open()
@app.on_event('shutdown')
def shutdown(): pool.close()

@app.middleware('http')
async def metrics_middleware(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    path = '/users/:id' if request.url.path.startswith('/users/') else request.url.path
    REQUESTS.labels(request.method, path, str(response.status_code)).inc()
    LATENCY.labels(request.method, path).observe(time.perf_counter() - started)
    return response

@app.get('/health')
def health(): return {'status':'ok','framework':'fastapi'}

@app.get('/metrics')
def metrics(): return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get('/users/{user_id}')
async def user_detail(user_id: int):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, email FROM users WHERE id = %s', (user_id,))
            row = cur.fetchone()
    if row is None: raise HTTPException(404, 'User not found')
    return {'id': row[0], 'name': row[1], 'email': row[2]}

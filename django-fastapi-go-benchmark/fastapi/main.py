import os, time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from psycopg_pool import AsyncConnectionPool

app = FastAPI(title='FastAPI Benchmark')
# autocommit=True to match Django's default (autocommit, no ATOMIC_REQUESTS) —
pool = AsyncConnectionPool(
    conninfo=f"host={os.getenv('DB_HOST')} port={os.getenv('DB_PORT')} dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASSWORD')}",
    min_size=2, max_size=10, open=False,
    kwargs={"autocommit": True},
)
REQUESTS = Counter('http_requests_total', 'Total HTTP requests', ['method', 'path', 'status'])
LATENCY = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'path'])

@app.on_event('startup')
async def startup(): await pool.open()
@app.on_event('shutdown')
async def shutdown(): await pool.close()

@app.get('/health')
def health(): return {'status':'ok','framework':'fastapi'}

@app.get('/metrics')
def metrics(): return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get('/users/{user_id}')
async def user_detail(user_id: int):
    started = time.perf_counter()
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute('SELECT id, name, email FROM users WHERE id = %s', (user_id,))
            row = await cur.fetchone()
    status = 200 if row else 404
    REQUESTS.labels('GET', '/users/:id', str(status)).inc()
    LATENCY.labels('GET', '/users/:id').observe(time.perf_counter() - started)
    if row is None: raise HTTPException(404, 'User not found')
    return {'id': row[0], 'name': row[1], 'email': row[2]}
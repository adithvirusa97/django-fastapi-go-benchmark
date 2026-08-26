from django.db import connection
from django.http import JsonResponse, HttpResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

REQUESTS = Counter('http_requests_total', 'Total HTTP requests', ['method', 'path', 'status'])
LATENCY = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'path'])

def health(request):
    return JsonResponse({'status': 'ok', 'framework': 'django'})

def metrics(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)

def user_detail(request, user_id):
    started = time.perf_counter()
    with connection.cursor() as cursor:
        cursor.execute('SELECT id, name, email FROM users WHERE id = %s', [user_id])
        row = cursor.fetchone()
    status = 200 if row else 404
    REQUESTS.labels(request.method, '/users/:id', str(status)).inc()
    LATENCY.labels(request.method, '/users/:id').observe(time.perf_counter() - started)
    if row is None:
        return JsonResponse({'detail': 'User not found'}, status=404)
    return JsonResponse({'id': row[0], 'name': row[1], 'email': row[2]})

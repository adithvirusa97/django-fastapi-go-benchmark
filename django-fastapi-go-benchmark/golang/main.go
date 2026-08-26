package main

import (
    "context"
    "encoding/json"
    "errors"
    "log"
    "net/http"
    "os"
    "strconv"
    "time"
    _ "go.uber.org/automaxprocs"
    "github.com/jackc/pgx/v5"
    "github.com/jackc/pgx/v5/pgxpool"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

type User struct { ID int64 `json:"id"`; Name string `json:"name"`; Email string `json:"email"` }
var pool *pgxpool.Pool
var requests = prometheus.NewCounterVec(prometheus.CounterOpts{Name: "http_requests_total", Help: "Total HTTP requests"}, []string{"method", "path", "status"})
var latency = prometheus.NewHistogramVec(prometheus.HistogramOpts{Name: "http_request_duration_seconds", Help: "HTTP request duration"}, []string{"method", "path"})

func init() { prometheus.MustRegister(requests, latency) }
func env(k, d string) string { if v := os.Getenv(k); v != "" { return v }; return d }
func writeJSON(w http.ResponseWriter, code int, v any) { w.Header().Set("Content-Type", "application/json"); w.WriteHeader(code); _ = json.NewEncoder(w).Encode(v) }
func health(w http.ResponseWriter, r *http.Request) { writeJSON(w, 200, map[string]string{"status":"ok", "framework":"golang"}) }
func userDetail(w http.ResponseWriter, r *http.Request) {
    started := time.Now()
    id, err := strconv.ParseInt(r.PathValue("id"), 10, 64)
    if err != nil { requests.WithLabelValues(r.Method, "/users/:id", "400").Inc(); latency.WithLabelValues(r.Method, "/users/:id").Observe(time.Since(started).Seconds()); http.Error(w, "invalid id", 400); return }
    ctx, cancel := context.WithTimeout(r.Context(), 2*time.Second); defer cancel()
    var u User
    err = pool.QueryRow(ctx, "SELECT id, name, email FROM users WHERE id = $1", id).Scan(&u.ID, &u.Name, &u.Email)
    status := "200"
    if errors.Is(err, pgx.ErrNoRows) { status = "404"; requests.WithLabelValues(r.Method, "/users/:id", status).Inc(); latency.WithLabelValues(r.Method, "/users/:id").Observe(time.Since(started).Seconds()); writeJSON(w, 404, map[string]string{"detail":"User not found"}); return }
    if err != nil { status = "500"; requests.WithLabelValues(r.Method, "/users/:id", status).Inc(); latency.WithLabelValues(r.Method, "/users/:id").Observe(time.Since(started).Seconds()); http.Error(w, err.Error(), 500); return }
    requests.WithLabelValues(r.Method, "/users/:id", status).Inc(); latency.WithLabelValues(r.Method, "/users/:id").Observe(time.Since(started).Seconds())
    writeJSON(w, 200, u)
}
func main() {
    dsn := "postgres://" + env("DB_USER","benchmark") + ":" + env("DB_PASSWORD","benchmark") + "@" + env("DB_HOST","localhost") + ":" + env("DB_PORT","5432") + "/" + env("DB_NAME","benchmark")
    cfg, err := pgxpool.ParseConfig(dsn); if err != nil { log.Fatal(err) }
    cfg.MinConns, cfg.MaxConns = 2, 10
    pool, err = pgxpool.NewWithConfig(context.Background(), cfg); if err != nil { log.Fatal(err) }; defer pool.Close()
    mux := http.NewServeMux(); mux.HandleFunc("GET /health", health); mux.Handle("GET /metrics", promhttp.Handler()); mux.HandleFunc("GET /users/{id}", userDetail)
    log.Println("Go listening on :8000"); log.Fatal(http.ListenAndServe(":8000", mux))
}

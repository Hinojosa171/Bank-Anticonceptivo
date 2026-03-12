# gunicorn.conf.py
bind = "0.0.0.0:10000"          # Puerto que usa Render
workers = 1                      # Un solo worker para ahorrar memoria
threads = 2                      # Pero con 2 hilos para concurrencia básica
timeout = 120                    # Tiempo máximo para respuestas (2 minutos)
max_requests = 10                 # Reiniciar worker cada 10 peticiones
max_requests_jitter = 5           # Variación aleatoria para evitar reinicios sincronizados
worker_class = "gthread"          # Usar hilos en lugar de procesos (más ligero)
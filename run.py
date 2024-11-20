import gunicorn

gunicorn_opts = {
    'workers': 3,
    'bind': '0.0.0.0:5000', 
    'worker_class': 'uvicorn.workers.UvicornWorker',
    'accesslog': '-',
    'errorlog': '-'
}

if __name__ == '__main__':
    gunicorn.run('main:app', **gunicorn_opts)
print("Starting Gunicorn...")
gunicorn.run('main:app', **gunicorn_opts)
print("Gunicorn finished.")
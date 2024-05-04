from flask_server import app, db
from flask_server.views.v1 import app_views
import asyncio
from flask_server.email_client import mailSender
from asgiref.wsgi import WsgiToAsgi
from multiprocessing import Process, Queue

import sys
import signal

app.register_blueprint(app_views)

with app.app_context():
	db.create_all()


@app.errorhandler(404)
def page_not_found():
    """Handle page not found"""
    return 'This page does not exist', 404


# Initialize a multiprocessing queue for inter-process communication
queue = Queue()

# Setup a consumer for sending mails
async def start(queue):
    """send mails async"""
    while True:
        if not queue.empty():
            print("i got here")
            kwargs = queue.get()
            task = asyncio.create_task(mailSender(**kwargs))
            try:
                await task
            except Exception as e:
                # Handle exceptions gracefully (e.g., log the error)
                print(f"An error occurred: {e}")
        else:
            print(queue.get())
            print('i didnt get here')
            await asyncio.sleep(4)


def signal_handler(sig, frame):
    print("Stopping consumer process...")
    consumer_process.terminate()  # Terminate the consumer process
    sys.exit(0)
    

def run_consumer():
    asyncio.run(start(queue))


if __name__ == '__main__':
    
    # Create a separate process for running the consumer loop
    consumer_process = Process(target=run_consumer, args=(queue,))
    consumer_process.start()


    # Register signal handler for termination signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Wrap the Flask app with the ASGIProxyMiddleware
    app = WsgiToAsgi(app)
    import uvicorn
    # app.run(host="127.0.0.1", port=5000)
    uvicorn.run(app, host="127.0.0.1", port=5000)

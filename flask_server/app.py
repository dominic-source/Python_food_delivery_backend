from flask_server import app, db, queue
from flask_server.views.v1 import app_views
import asyncio
from flask_server.email_client import mailSender


app.register_blueprint(app_views)

with app.app_context():
	db.create_all()


@app.errorhandler(404)
def page_not_found():
    """Handle page not found"""
    return 'This page does not exist', 404

# Setup a consumer for sending mails
async def main():
    """send mails async"""
    while True:
        if not queue.empty():
            kwargs = queue.get(block=False)
            task = asyncio.create_task(mailSender(**kwargs))
            try:
                await task
            except Exception as e:
                # Handle exceptions gracefully (e.g., log the error)
                print(f"An error occurred: {e}")
        else:
            await asyncio.sleep(4)

if __name__ == '__main__':
    asyncio.run(main())
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
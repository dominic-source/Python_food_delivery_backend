"""
consumer.py

This module defines a consumer process that listens to a Redis queue for
tasks, processes these tasks, and sends emails using the mailSender function.
"""

from flask_server.email_client import mailSender
import logging
import asyncio
import redis
import json

# Configure logging
logging.basicConfig(filename='consumer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to Redis server
r = redis.Redis(host='localhost', port=6379)

async def main():
    """
    Main consumer process that listens to the Redis queue and processes tasks.

    This function runs in an infinite loop, blocking and popping messages from 
    the Redis queue, and then creating tasks to send emails based on the popped 
    messages.
    """
    print("Consumer process has started!")
    while True:
        logging.info("Loop 1")
        # Block and pop a message from the queue
        data = r.blpop('user_data_queue')
        data = data[1].decode('utf-8')
        if data:
            logging.info("Received task from queue")
            # Process the data (remove quotes from `b'...'`)
            user_data = json.loads(data)
            task = asyncio.create_task(mailSender(**user_data))
            await task
            if asyncio.as_completed(task):
                logging.info(f"Email task with user id = {user_data['id']} is completed!")

asyncio.run(main())

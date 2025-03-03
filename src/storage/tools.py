import logging
import os

from src.settings import BASE_DIR

logging.basicConfig(filename=os.path.join(BASE_DIR, 'actions.log'), level=logging.INFO,
                    format='%(asctime)s - %(message)s')


def log_action(user_id, action_type):
    logging.info(f"User: {user_id}, Action: {action_type}")

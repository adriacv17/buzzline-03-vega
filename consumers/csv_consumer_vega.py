"""
csv_consumer_vega.py

Consume JSON messages from a Kafka topic and process them with real-time analytics for heart rate monitoring.

Example Kafka message format:
{"timestamp": "2025-01-11T18:15:00Z", "heart_rate": 72.0}
"""

#####################################
# Import Modules
#####################################

# Import packages from Python Standard Library
import os
import json

# Use a deque ("deck") - a double-ended queue data structure
# A deque is a good way to monitor a certain number of "most recent" messages
# A deque is a great data structure for time windows (e.g. the last 5 messages)
from collections import deque

# Import external packages
from dotenv import load_dotenv

# Import functions from local modules
from utils.utils_consumer import create_kafka_consumer
from utils.utils_logger import logger

#####################################
# Load Environment Variables
#####################################

# Load environment variables from .env
load_dotenv()

#####################################
# Getter Functions for .env Variables
#####################################


def get_kafka_topic() -> str:
    """Fetch Kafka topic from environment or use default."""
    topic = os.getenv("HEART_TOPIC", "unknown_topic")
    logger.info(f"Kafka topic: {topic}")
    return topic


def get_kafka_consumer_group_id() -> str:
    """Fetch Kafka consumer group id from environment or use default."""
    group_id: str = os.getenv("HEART_CONSUMER_GROUP_ID", "default_group")
    logger.info(f"Kafka consumer group id: {group_id}")
    return group_id


def get_stall_threshold() -> float:
    """Fetch heart rate variation threshold from environment or use default."""
    hr_variation = float(os.getenv("HEART_STALL_THRESHOLD_BPM", 5.0))
    logger.info(f"Max stall heart rate variation: {hr_variation} BPM")
    return hr_variation


def get_rolling_window_size() -> int:
    """Fetch rolling window size from environment or use default."""
    window_size = int(os.getenv("HEART_ROLLING_WINDOW_SIZE", 5))
    logger.info(f"Rolling window size: {window_size}")
    return window_size


def get_heart_rate_threshold_high() -> float:
    """Fetch the high heart rate threshold for alerts."""
    threshold_high = float(os.getenv("HEART_RATE_THRESHOLD_HIGH", 120.0))
    logger.info(f"High heart rate threshold: {threshold_high} BPM")
    return threshold_high


def get_heart_rate_threshold_low() -> float:
    """Fetch the low heart rate threshold for alerts."""
    threshold_low = float(os.getenv("HEART_RATE_THRESHOLD_LOW", 40.0))
    logger.info(f"Low heart rate threshold: {threshold_low} BPM")
    return threshold_low


#####################################
# Define a function to detect a stall
#####################################


def detect_stall(rolling_window_deque: deque) -> bool:
    """
    Detect a heart rate stall based on the rolling window.

    Args:
        rolling_window_deque (deque): Rolling window of heart rate readings.

    Returns:
        bool: True if a stall is detected, False otherwise.
    """
    WINDOW_SIZE: int = get_rolling_window_size()
    if len(rolling_window_deque) < WINDOW_SIZE:
        # We don't have a full deque yet
        # Keep reading until the deque is full
        logger.debug(
            f"Rolling window size: {len(rolling_window_deque)}. Waiting for {WINDOW_SIZE}."
        )
        return False

    # Once the deque is full we can calculate the heart rate range
    # Use Python's built-in min() and max() functions
    # If the range is less than or equal to the threshold, we have a stall
    hr_range = max(rolling_window_deque) - min(rolling_window_deque)
    is_stalled: bool = hr_range <= get_stall_threshold()
    logger.debug(f"Heart rate range: {hr_range} BPM. Stalled: {is_stalled}")
    return is_stalled


#####################################
# Define function for real-time heart rate pattern alerting
#####################################

def alert_on_heart_rate_anomaly(heart_rate: float) -> None:
    """
    Alerts if the heart rate exceeds certain thresholds, indicating potential issues.

    Args:
        heart_rate (float): The heart rate to check against predefined thresholds.
    """
    high_threshold = get_heart_rate_threshold_high()
    low_threshold = get_heart_rate_threshold_low()

    if heart_rate > high_threshold:
        logger.warning(f"ALERT: High heart rate detected: {heart_rate} BPM!")
        # You can add more alerting logic here, like sending an email or triggering a webhook.

    elif heart_rate < low_threshold:
        logger.warning(f"ALERT: Low heart rate detected: {heart_rate} BPM!")
        # Similarly, more alerting logic can be added for low heart rate.


#####################################
# Function to process a single message
#####################################


def process_message(message: str, rolling_window: deque, window_size: int) -> None:
    """
    Process a JSON-transferred heart rate message and check for stalls and anomalies.

    Args:
        message (str): JSON message received from Kafka.
        rolling_window (deque): Rolling window of heart rate readings.
        window_size (int): Size of the rolling window.
    """
    try:
        # Log the raw message for debugging
        logger.debug(f"Raw message: {message}")

        # Parse the JSON string into a Python dictionary
        data: dict = json.loads(message)
        heart_rate = data.get("heart_rate")
        timestamp = data.get("timestamp")
        logger.info(f"Processed JSON message: {data}")

        # Ensure the required fields are present
        if heart_rate is None or timestamp is None:
            logger.error(f"Invalid message format: {message}")
            return

        # Alert on high or low heart rate
        alert_on_heart_rate_anomaly(heart_rate)

        # Append the heart rate reading to the rolling window
        rolling_window.append(heart_rate)

        # Check for a stall
        if detect_stall(rolling_window):
            logger.info(
                f"STALL DETECTED at {timestamp}: Heart rate stable at {heart_rate} BPM over last {window_size} readings."
            )

    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error for message '{message}': {e}")
    except Exception as e:
        logger.error(f"Error processing message '{message}': {e}")


#####################################
# Define main function for this module
#####################################


def main() -> None:
    """
    Main entry point for the consumer.

    - Reads the Kafka topic name and consumer group ID from environment variables.
    - Creates a Kafka consumer using the `create_kafka_consumer` utility.
    - Polls and processes messages from the Kafka topic.
    """
    logger.info("START consumer.")

    # fetch .env content
    topic = get_kafka_topic()
    group_id = get_kafka_consumer_group_id()
    window_size = get_rolling_window_size()
    logger.info(f"Consumer: Topic '{topic}' and group '{group_id}'...")
    logger.info(f"Rolling window size: {window_size}")

    rolling_window = deque(maxlen=window_size)

    # Create the Kafka consumer using the helpful utility function.
    consumer = create_kafka_consumer(topic, group_id)

    # Poll and process messages
    logger.info(f"Polling messages from topic '{topic}'...")
    try:
        for message in consumer:
            message_str = message.value
            logger.debug(f"Received message at offset {message.offset}: {message_str}")
            process_message(message_str, rolling_window, window_size)
    except KeyboardInterrupt:
        logger.warning("Consumer interrupted by user.")
    except Exception as e:
        logger.error(f"Error while consuming messages: {e}")
    finally:
        consumer.close()
        logger.info(f"Kafka consumer for topic '{topic}' closed.")


#####################################
# Conditional Execution
#####################################

# Ensures this script runs only when executed directly (not when imported as a module).
if __name__ == "__main__":
    main()
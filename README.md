# buzzline-03-vega

Streaming data does not have to be simple text. Many of us are familiar with streaming video content and audio (e.g., music) files.

Streaming data can be structured (e.g., CSV files) or semi-structured (e.g., JSON data). In this project, we’ll work with two different types of data and use two different Kafka topic names. See the `.env` file for more details.

## Task 1: Use Tools from Module 1 and 2
Before starting, ensure you have completed the setup tasks in:
- [buzzline-01-case](https://github.com/denisecase/buzzline-01-case)
- [buzzline-02-case](https://github.com/denisecase/buzzline-02-case)

**Note:** Python 3.11 is required for this project.

## Task 2: Copy This Example Project and Rename
Once the tools are installed, copy or fork this project into your GitHub account and create your own version of the project to run and experiment with. Name it `buzzline-03-yourname` (replace `yourname` with something unique to you).

For more details, follow the instructions in the [FORK-THIS-REPO.md](FORK-THIS-REPO.md).

## Task 3: Manage Local Project Virtual Environment
Follow the instructions in [MANAGE-VENV.md](MANAGE-VENV.md) to:
- Create a `.venv`
- Activate `.venv`
- Install the required dependencies using `requirements.txt`

## Task 4: Start Zookeeper and Kafka (2 Terminals)
If Zookeeper and Kafka are not already running, you'll need to restart them. Follow the instructions at [SETUP-KAFKA.md](SETUP-KAFKA.md) to:
- Start the Zookeeper Service
- Start Kafka

## Task 5: Start the JSON Producer and Consumer

### JSON Kafka Producer

To start the **JSON producer**, which sends heart rate data in JSON format to Kafka, follow these steps:

1. Open a terminal and activate the virtual environment.
2. Run the following command to start the JSON producer:

Windows:

```shell
.venv\Scripts\activate
py -m producers.json_producer_vega
```

Mac/Linux:
```zsh
source .venv/bin/activate
python3 -m producers.json_producer_vega
```
This producer will push heart rate data to the Kafka topic specified in your .env file.

### JSON Kafka Consumer
The JSON consumer listens to the Kafka topic and processes the incoming heart rate data in real time. To run the JSON consumer:

1. Open a new terminal and activate the virtual environment.
2. Run the following command to start the JSON consumer:

Windows:

```shell
.venv\Scripts\activate
py -m producers.json_consumer_vega
```

Mac/Linux:
```zsh
source .venv/bin/activate
python3 -m producers.json_consumer_vega
```

## Task 6: Start the CSV Producer and Consumer

### CSV Kafka Producer
To start the CSV producer, which sends heart rate data in CSV format to Kafka, follow these steps:

1. Open a terminal and activate the virtual environment.
2. Run the following command to start the CSV producer:

Windows:

```shell
.venv\Scripts\activate
py -m producers.csv_producer_vega
```

Mac/Linux:
```zsh
source .venv/bin/activate
python3 -m producers.csv_producer_vega
```
This producer sends heart rate data to Kafka in CSV format.

### CSV Kafka Consumer
To start the CSV consumer, which listens to the Kafka topic and processes the CSV data, follow these steps:

1. Open a new terminal and activate the virtual environment.
2. Run the following command to start the CSV consumer:

Windows:

```shell
.venv\Scripts\activate
py -m producers.csv_consumer_vega
```

Mac/Linux:
```zsh
source .venv/bin/activate
python3 -m producers.csv_consumer_vega
```

## Later Work Sessions
When resuming work on this project:
1. Open the folder in VS Code. 
2. Start the Zookeeper service.
3. Start the Kafka service.
4. Activate your local project virtual environment (.env).

## Save Space
To save disk space, you can delete the .venv folder when not actively working on this project.
You can always recreate it, activate it, and reinstall the necessary packages later. 
Managing Python virtual environments is a valuable skill. 

## License
This project is licensed under the MIT License as an example project. 
You are encouraged to fork, copy, explore, and modify the code as you like. 
See the [LICENSE](LICENSE.txt) file for more.
# Football League App with Kafka

## Description

The Football League app is designed as a learning project to explore the capabilities of Kafka consumers and producers within a real-world application context. This app simulates a football league, allowing users to activate weekly games, which dynamically updates a league table based on the outcomes of these games. It features various visual representations of league data, such as points and positions, using Streamlit for an interactive user experience.

The data for the football league is generated internally by the application, with no external data sources. This project serves as a practical example of integrating Kafka with Python and Streamlit, showcasing data streaming and processing in a sporting context.

## Technology Stack

- **Apache Kafka**: Used for handling real-time data feeds by producing and consuming messages that represent game activations and outcomes.
- **Python**: The primary programming language for backend development and Kafka integration.
- **Streamlit**: Powers the interactive web interface, allowing users to view and interact with the league table and related visualizations.
- **Docker**: Utilized for containerization, ensuring consistent environments and simplifying the setup process for development and deployment.

## Setup and Installation

Ensure Docker is installed on your system to facilitate an easy setup process for running the application and its dependencies, including Kafka and Zookeeper.



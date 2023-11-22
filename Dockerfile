# Use an appropriate base image
FROM bitnami/spark:3

# Set the working directory in the container
WORKDIR /app

# Copy the local application files to the container's working directory
COPY . /app

# Install any additional dependencies your application requires
# For example, if your app is a Python app, you might need to install Python packages:
# RUN pip install -r requirements.txt

# (Optional) Add any environment variables your application requires

# (Optional) Expose any ports your application uses

# Command to run your application
# CMD ["spark-submit", "your-spark-app.py"]
# or for Java/Scala apps, replace with the appropriate command

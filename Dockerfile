# Step 1: Use an official, lightweight Python base layer
FROM python:3.11-slim

# Step 2: Set the internal folder where our code will live inside the container
WORKDIR /app

# Step 3: Copy our list of libraries into the container
COPY requirements.txt .

# Step 4: Install the listed libraries inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy our python application code into the container
COPY main.py .
COPY recommendation.py .

# Step 6: Expose the network port our app runs on
EXPOSE 8000

# Step 7: Run our server command when the container boots up
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
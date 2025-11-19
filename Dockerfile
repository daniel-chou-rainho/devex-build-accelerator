# Use the same Java version as the Gradle Toolchain (Java 21)
FROM eclipse-temurin:21-jdk-jammy

# Install Python (for the deflaker script)
RUN apt-get update && apt-get install -y python3

# Set working directory
WORKDIR /app

# Copy strictly what we need to run the build
COPY gradle gradle
COPY gradlew .
COPY build-logic build-logic
COPY settings.gradle.kts .
COPY gradle.properties .

# Copy the source code
COPY payment-api payment-api
COPY core-banking core-banking
COPY tools tools

# Grant execution rights
RUN chmod +x gradlew

CMD ["python3", "tools/deflaker.py"]
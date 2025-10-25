# Use official Java 21 base image
FROM eclipse-temurin:21-jdk

# Set working directory
WORKDIR /app

# Copy the built JAR file from target/
COPY target/*.jar app.jar

# Expose port 4000
EXPOSE 4000

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]


FROM infotechsoft/maven:3.8.6-openjdk-17 

WORKDIR /app

COPY ./backend/pom.xml .

COPY ./backend/src ./src

EXPOSE 8080

# RUN mvn package -DskipTests

# FROM eclipse-temurin:17-jre-alpine

# WORKDIR /app

# COPY --from=builder /app/target/*.jar /app/app.jar

# ENTRYPOINT ["java", "-jar", "app.jar"]
ENTRYPOINT ["mvn", "spring-boot:run", "-X"]
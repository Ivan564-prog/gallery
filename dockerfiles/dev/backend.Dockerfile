FROM maven:3.8.6-openjdk-17 AS builder

WORKDIR /app

COPY ./backend/pom.xml .

COPY ./backend/src ./src

RUN mvn dependency:go-offline

RUN mvn package -DskipTests

FROM openjdk:17-slim

WORKDIR /app

COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]

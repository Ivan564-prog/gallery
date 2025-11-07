FROM infotechsoft/maven:3.8.6-openjdk-17 

WORKDIR /app

COPY ./backend/pom.xml .

COPY ./backend/src ./src

#RUN mvn dependency:go-offline

#RUN mvn package -DskipTests

#FROM openjdk:17-slim

#WORKDIR /app

#COPY --from=builder /app/target/*.jar app.jar

EXPOSE 8080

# ENTRYPOINT ["yes"]
#ENTRYPOINT ["java", "-jar", "app.jar"]
ENTRYPOINT ["mvn", "spring-boot:run"]
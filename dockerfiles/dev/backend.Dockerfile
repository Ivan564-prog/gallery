FROM infotechsoft/maven:3.8.6-openjdk-17 

WORKDIR /app

COPY ./backend/pom.xml .

COPY ./backend/src ./src

EXPOSE 8080

ENTRYPOINT [ \
    "mvn", \
    "spring-boot:run", \
    "-Dspring.output.ansi.enabled=always", \
    "-Dlogging.level.root=DEBUG", \
    "-Dlogging.pattern.console=%d{yyyy-MM-dd HH:mm:ss} %-5level [%thread] %logger{36} - %msg%n" \
]
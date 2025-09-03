FROM gessnerfl/fake-smtp-server:2.2.1

# Download JaCoCo agent
RUN curl -L -o /jacocoagent.jar \
    https://repo1.maven.org/maven2/org/jacoco/org.jacoco.agent/0.8.11/org.jacoco.agent-0.8.11-runtime.jar

# Expose JaCoCo dump port
EXPOSE 6300

# Volume for coverage data
VOLUME ["/coverage"]

# Set JaCoCo agent options
ENV JAVA_TOOL_OPTIONS="-javaagent:/jacocoagent.jar=destfile=/coverage/jacoco.exec,output=tcpserver,address=*,port=6300,append=true"
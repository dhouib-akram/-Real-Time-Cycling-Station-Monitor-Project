# Start from the Bitnami Spark image
FROM bitnami/spark:3.2.4

# Switch to root to install packages
USER root



# Install Scala 2.12
RUN curl -LO https://downloads.lightbend.com/scala/2.12.15/scala-2.12.15.tgz && \
    tar -xzvf scala-2.12.15.tgz -C /opt/ && \
    rm scala-2.12.15.tgz && \
    mv /opt/scala-2.12.15 /opt/scala

# Set up environment variables for Scala
ENV SCALA_HOME /opt/scala
ENV PATH $PATH:$SCALA_HOME/bin



# Install the Elasticsearch client for Python
RUN pip install elasticsearch==7.9.1

# Switch back to the default user
USER 1001

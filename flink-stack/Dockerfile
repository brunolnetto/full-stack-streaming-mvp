FROM apache/flink:1.17-python

USER root

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy user code
COPY src/ /opt/src/

USER flink 
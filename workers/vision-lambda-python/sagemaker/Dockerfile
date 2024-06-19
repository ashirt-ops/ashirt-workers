FROM --platform=linux/amd64 python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV TASK_ROOT=/opt/program
ENV PATH="${TASK_ROOT}:${PATH}"
WORKDIR ${TASK_ROOT}

# Install additional required packages
RUN pip3 install huggingface_hub gunicorn
# Download the required model components
RUN huggingface-cli download microsoft/Phi-3-vision-128k-instruct-onnx-cpu --include cpu-int4-rtn-block-32-acc-level-4/* --local-dir model/

# Copy requirements file and install dependencies
COPY requirements.txt ${TASK_ROOT}
RUN pip3 install -r requirements.txt --target "${TASK_ROOT}"

# Copy application file
COPY app.py ${TASK_ROOT}

# Run the Flask application
ENTRYPOINT ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "app:app"]
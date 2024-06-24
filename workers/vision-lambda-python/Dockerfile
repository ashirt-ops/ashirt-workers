FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.12

RUN pip3 install --upgrade huggingface_hub
RUN huggingface-cli download microsoft/Phi-3-vision-128k-instruct-onnx-cpu --include cpu-int4-rtn-block-32-acc-level-4/* --local-dir model/ 

COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY app "${LAMBDA_TASK_ROOT}"

CMD ["app.__main__"]
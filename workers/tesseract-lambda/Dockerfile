FROM public.ecr.aws/lambda/nodejs:16

# RUN yum update -y \
#     && yum install -y tesseract-ocr

RUN rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm \
    && yum -y update \
    && yum -y groupinstall 'Development Tools' \
    && yum -y install tesseract python3

COPY app ${LAMBDA_TASK_ROOT}
COPY package.json ${LAMBDA_TASK_ROOT}

RUN npm install

RUN yum -y remove python3 binutils \
    && yum -y --setopt=groupremove_leaf_only=1 groupremove 'Development Tools'

CMD ["app.handler"]

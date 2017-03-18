# Simply because I have it on my laptop but it doesn't matter that much
# Can be any
FROM oraclelinux:7

#----- Docker Metadata -------------

MAINTAINER Ekaterina Voidenko <katyavoid@gmail.com>

# Default time setup and timestamp of image build = dockermark
# RUN cp /usr/share/zoneinfo/UTC /etc/localtime
RUN echo "UTC" >/etc/timezone
RUN chmod 644 /etc/timezone /etc/localtime
RUN touch /dockermark

# Save a copy of this Dockerfile to the image - as metadata for what it is
COPY Dockerfile /Dockerfile

# Oracle way, I'll change it later
#-----------------------------------
RUN curl http://public-yum.oracle.com/public-yum-ol7.repo > /etc/yum.repos.d/public-yum-ol7.repo
RUN sed -i s~enabled=0~enabled=1~g /etc/yum.repos.d/public-yum-ol7.repo

# Or we can go in a true path and download pip
RUN yum install -y python-pip

COPY app /app
RUN pip install -r /app/requirements.txt

## Clean up unused files on image
RUN yum clean all
RUN mkdir /docker-entrypoint-initdb.d
ENV PATH=/app:$PATH

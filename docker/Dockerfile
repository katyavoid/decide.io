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

# Oracle way, but ok
#-----------------------------------
RUN curl http://public-yum.oracle.com/public-yum-ol7.repo > /etc/yum.repos.d/public-yum-ol7.repo
RUN sed -i s~enabled=0~enabled=1~g /etc/yum.repos.d/public-yum-ol7.repo
COPY nginx/nginx.repo /etc/yum.repos.d/

# Or we can go in a true way and download pip
RUN yum install -y python-pip nginx build-essential setuptools python-devel gcc cc

COPY app /app
RUN mkdir /var/log/app
RUN chown nginx:nginx /var/log/app
RUN rm -f /etc/nginx/conf.d/default.conf
COPY nginx/*0*.conf /etc/nginx/conf.d/
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Install requirements
RUN pip install -r /app/requirements.txt

## Clean up unused files on image
RUN yum clean all
RUN mkdir /docker-entrypoint-initdb.d
ENV PATH=/app:$PATH
CMD /entrypoint.sh

FROM oraclelinux:7

# install python 3
RUN  yum install -y python3

# install oracle instant client
#RUN  yum -y install oraclelinux-developer-release-el7
#RUN  yum -y install oracle-instantclient-release-el7
#RUN  yum -y install python36-cx_Oracle
RUN  curl -o /etc/yum.repos.d/public-yum-ol7.repo https://yum.oracle.com/public-yum-ol7.repo && \
     yum-config-manager --enable ol7_oracle_instantclient && \
     yum -y install oracle-instantclient18.3-basic oracle-instantclient18.3-devel oracle-instantclient18.3-sqlplus && \
     rm -rf /var/cache/yum && \
     echo /usr/lib/oracle/18.3/client64/lib > /etc/ld.so.conf.d/oracle-instantclient18.3.conf && \
     ldconfig

# add instant client to path
ENV PATH=$PATH:/usr/lib/oracle/18.3/client64/bin
ENV TNS_ADMIN=/usr/lib/oracle/18.3/client64/lib/network/admin

# add wallet files
ADD ./wallet /usr/lib/oracle/18.3/client64/lib/network/admin/

COPY . /

# set working directory
WORKDIR /

# install required libraries
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# This is the runtime command for the container
CMD python3 twitter_search.py

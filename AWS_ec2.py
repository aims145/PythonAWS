#import boto.ec2
#import botocore
import boto3
import sys
tomcatUsername = "amrit"
tomcatUserpass = "amrit"

user_data_script = """#!/bin/bash
cd /opt/
sudo su
############### Install java
wget --no-cookies --no-check-certificate --header "Cookie: oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u171-b11/512cd62ec5174c3487ac17c61aaa89e8/jdk-8u171-linux-x64.tar.gz"
filename=`ls|grep jdk*.tar.gz`
tar -zxf $filename
Dir_name=`tar -tzf $filename | head -1 | cut -f1 -d"/"`
javapath="`pwd`/$Dir_name"
chown root:root -R $javapath
echo "export JAVA_HOME=$javapath" >> /etc/profile
echo "export JRE_HOME=$javapath/jre" >> /etc/profile
echo "export PATH=\$PATH:\$JAVA_HOME/bin:\$JRE_HOME/bin" >> /etc/profile
/bin/bash /etc/profile
##########################################################################


########Download tomcat 
wget http://ftp.cixug.es/apache/tomcat/tomcat-7/v7.0.86/bin/apache-tomcat-7.0.86.tar.gz
tomcatfile=`ls apache-tomcat-*.tar.gz`
tar -zxf $tomcatfile
tomcatdir=`tar -tzf $tomcatfile | head -1 | cut -f1 -d"/"`
catalinahome=`pwd`/$tomcatdir/ ; 

echo '#!/bin/sh' >> /etc/rc.d/init.d/tomcat
echo "# Tomcat init script for Linux." >> /etc/rc.d/init.d/tomcat
#
# chkconfig: 2345 96 14
# description: The Apache Tomcat servlet/JSP container.
echo "JAVA_HOME=$javapath" >> /etc/rc.d/init.d/tomcat
echo "CATALINA_HOME=$catalinahome" >> /etc/rc.d/init.d/tomcat
echo "export \$JAVA_HOME \$CATALINA_HOME" >> /etc/rc.d/init.d/tomcat
echo "\$CATALINA_HOME/bin/catalina.sh \$*" >> /etc/rc.d/init.d/tomcat
  
chmod 755 /etc/rc.d/init.d/tomcat
chkconfig --level 2345 tomcat on 

sed  -i '/<\/tomcat-users>/i <role rolename="manager-gui"/>' $catalinehome/conf/tomcat-users.xml

sed  -i '/<\/tomcat-users>/i <role rolename="manager-script"/>' $catalinehome/conf/tomcat-users.xml

sed  -i '/<\/tomcat-users>/i <role rolename="manager-jmx"/>' $catalinehome/conf/tomcat-users.xml

sed  -i '/<\/tomcat-users>/i <role rolename="manager-status"/>' $catalinehome/conf/tomcat-users.xml

sed  -i '/<\/tomcat-users>/i <user username="""+tomcatUsername+""" password="""+tomcatUserpass+""" roles="manager-gui,manager-script,manager-jmx,manager-status"/>' $catalinehome/conf/tomcat-users.xml


service tomcat start

"""
#print(user_data_script)
#sys.exit(0)

ec2 = boto3.resource('ec2', 'us-east-1',aws_access_key_id='AKIAJWEV7LURRWXBOIWASAM',aws_secret_access_key='r7nEit5DGHE1qzzD0HlBFiAvuSbp8W5sBWkfaEOIsaM')
response = ec2.create_instances(ImageId='ami-467ca739',
                               InstanceType='t2.micro',
                               KeyName='amrit_sharma',
                               SecurityGroups=['default'],
                               MaxCount=1,
                               MinCount=1,
                               UserData=user_data_script,
                               DryRun=False,
                               TagSpecifications=[{
                                       'ResourceType': 'instance',
                                       'Tags':[{
                                               'Key': 'Name',
                                               'Value': 'MyNewInstance'
                                               }]
                                       }]
                               )

instance_id = response[0].id
public_ip = ec2.Instance(instance_id).public_ip_address

print("Instance with instance ID - " + str(instance_id) + " has been launched. You can access Tomcat with following URL. http://" + str(public_ip) +":8080")


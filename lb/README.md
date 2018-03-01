# Get all ssl certs ARN from all ELB and ALB by region

    $ python elb/elb_and_ssl.py > /tmp/all.txt
    $ cat /tmp/all.txt| grep 'xxx-xxx-xxx-xxx-xxx'

package main

import (
	"fmt"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/elb"
)

func main() {
	sess := session.Must(session.NewSession())

	svc := elb.New(sess, &aws.Config{
		Region: aws.String("us-east-1"),
	})

	params := &elb.DescribeLoadBalancersInput{
	// LoadBalancerNames: []*string{
	// 	aws.String("AccessPointName"), // Required
	// 	// More values...
	// },
	// Marker:   aws.String("Marker"),
	// PageSize: aws.Int64(1),
	}
	resp, err := svc.DescribeLoadBalancers(params)
	aaa := resp.LoadBalancerDescriptions

	for _, v := range aaa {
		fmt.Println(*v.LoadBalancerName)
		bbb := v.ListenerDescriptions
		for _, n := range bbb {
			fmt.Println(*n.Listener.InstancePort)
			fmt.Println(*n.Listener.LoadBalancerPort)
		}
	}

	if err != nil {
		// Print the error, cast err to awserr.Error to get the Code and
		// Message from an error.
		fmt.Println(err.Error())
		return
	}

	// Pretty-print the response data.
	// fmt.Println(resp)
}

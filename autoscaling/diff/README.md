#

## Requirements

    pip install -r requirements.txt

## Usage

    python check_autoscaling.py <ag_name>

## Example of termination

    (python3) λ ~ master* aws autoscaling terminate-instance-in-auto-scaling-group --instance-id *** --no-should-decrement-desired-capacity
    {
        "Activity": {
            "Cause": "At 2016-11-09T11:28:29Z instance xxx was taken out of service in response to a user request.",
            "StartTime": "2016-11-09T11:28:29.403Z",
            "Progress": 0,
            "Description": "Terminating EC2 instance: xxx
            "ActivityId": "xxx",
            "Details": "{\"Subnet ID\":\"xxx\",\"Availability Zone\":\"us-east-1c\"}",
            "StatusCode": "InProgress"
        }
    }

## Notes

- Works with python3
- Works on OSX Sierra

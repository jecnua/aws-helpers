#

## Enabled metrics

Autoscaling [groups metrics](https://docs.aws.amazon.com/cli/latest/reference/autoscaling/enable-metrics-collection.html) are [now free](https://aws.amazon.com/about-aws/whats-new/2016/08/free-auto-scaling-group-metrics-with-graphs/). By default Terraform do not activate
them, you need to add:

    enabled_metrics = [
      "GroupMinSize",
      "GroupMaxSize",
      "GroupDesiredCapacity",
      "GroupInServiceInstances",
      "GroupPendingInstances",
      "GroupStandbyInstances",
      "GroupTerminatingInstances",
      "GroupTotalInstances",
    ]

    metrics_granularity = "1Minute"

To the ag configuration.

To activate via cli:

    aws autoscaling enable-metrics-collection --auto-scaling-group-name <name> --granularity "1Minute"

But if you don't change the Terraform, it will revert it.

    ~ module.elasticsearch.aws_autoscaling_group.es_clientnodes_autoscaling_group
        enabled_metrics.#:          "8" => "0"
        enabled_metrics.119681000:  "GroupStandbyInstances" => ""
        enabled_metrics.1940933563: "GroupTotalInstances" => ""
        enabled_metrics.308948767:  "GroupPendingInstances" => ""
        enabled_metrics.3267518000: "GroupTerminatingInstances" => ""
        enabled_metrics.3394537085: "GroupDesiredCapacity" => ""
        enabled_metrics.3551801763: "GroupInServiceInstances" => ""
        enabled_metrics.4118539418: "GroupMinSize" => ""
        enabled_metrics.4136111317: "GroupMaxSize" => ""

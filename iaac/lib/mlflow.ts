import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import {CfnEIP, Vpc} from "aws-cdk-lib/aws-ec2";
import {Bucket} from "aws-cdk-lib/aws-s3";

export class MlflowConstruct extends cdk.Stack {
  public readonly instance: ec2.Instance;
  public mlflowBucketName: string;

  constructor(scope: Construct, id: string, props: {
    elasticIp: CfnEIP;
    vpc: Vpc;
    mlflowBucket: Bucket
  }) {
    super(scope, id);

    this.mlflowBucketName = props.mlflowBucket.bucketName;

    const securityGroup = new ec2.SecurityGroup(this, 'MLflowSecurityGroup', {
      vpc: props.vpc,
      description: 'Security group for MLflow EC2 instance',
      allowAllOutbound: true,
    });

    securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(5000), 'Allow inbound HTTP traffic for MLflow');
    securityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22), 'Allow SSH access');



    // Create the EC2 instance
    this.instance = new ec2.Instance(this, 'EC2Instance', {
      vpc: props.vpc,
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T4G, ec2.InstanceSize.MICRO),
      machineImage: ec2.MachineImage.latestAmazonLinux2023({
        cpuType: ec2.AmazonLinuxCpuType.ARM_64
      }),
      securityGroup,
      vpcSubnets: { subnetType: ec2.SubnetType.PUBLIC },
      associatePublicIpAddress: true

    });

    props.mlflowBucket.grantReadWrite(this.instance)

    this.instance.addUserData(
      'yum update -y',
      'yum install -y python3-pip git',
      'pip3 install mlflow boto3',
      'mkdir /mlflow',
      `mlflow server --backend-store-uri sqlite:////mlflow/mlflow.db --default-artifact-root s3://${props.mlflowBucket.bucketName}/mlflow-artifacts/ --host 0.0.0.0 --port 5000 &`
    );

    new ec2.CfnEIPAssociation(this, 'ElasticIPAssociation', {
      instanceId: this.instance.instanceId,
      allocationId: props.elasticIp.attrAllocationId,
    });
  }
}
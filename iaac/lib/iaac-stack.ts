import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as ecr_assets from 'aws-cdk-lib/aws-ecr-assets';
import * as s3 from 'aws-cdk-lib/aws-s3';
import {Architecture} from "aws-cdk-lib/aws-lambda";
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import {Duration} from "aws-cdk-lib";
import {Dag} from "./dag";
import * as iam from 'aws-cdk-lib/aws-iam';
import {MlflowConstruct} from "./mlflow";
import {WebService} from "./webservice";



export class IaacStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'MyVPC', {
      maxAzs: 2
    });

    const mlflowElasticIp = new ec2.CfnEIP(this, 'ElasticIP', {
      domain: 'vpc',
    });

    const dataBucket = new s3.Bucket(this, 'BikeDurationPredictorBucket', {
      bucketName: `bike-duration-predictor-${this.account}`,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    const dataProcessingAsset = new ecr_assets.DockerImageAsset(this, 'DataProcessingAsset', {
      directory: '../bike_duration_predictor',
      file: 'dataprocessing.dockerfile'
    });

    const modelTrainingAsset = new ecr_assets.DockerImageAsset(this, 'ModelTrainingAsset', {
      directory: '../bike_duration_predictor',
      file: 'modeltraining.dockerfile'
    });

    const dataProcessingFunction = new lambda.DockerImageFunction(this, "dataProcessingFunction", {
      code: lambda.DockerImageCode.fromEcr(dataProcessingAsset.repository, {
        tagOrDigest: dataProcessingAsset.imageTag
      }),
      architecture: Architecture.ARM_64,
      timeout: Duration.minutes(5),
      memorySize: 512
    });

    const modelTrainingRole = new iam.Role(this, 'ModelTrainingLambdaRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      description: 'Role for Model Training Lambda function',
    });
    modelTrainingRole.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'));
    modelTrainingRole.addToPolicy(new iam.PolicyStatement({
      actions: [
        'sagemaker:*',
      ],
      resources: ['*'],
    }));

    const account = cdk.Stack.of(this).account;
    const region = cdk.Stack.of(this).region;
    const sagemakerDefaultBucketName = `sagemaker-${region}-${account}`;

    modelTrainingRole.addToPolicy(new iam.PolicyStatement({
      actions: [
        's3:*',
      ],
      resources: [
        `${dataBucket.bucketArn}/*`,
        `arn:aws:s3:::${sagemakerDefaultBucketName}`,
        `arn:aws:s3:::${sagemakerDefaultBucketName}/*`,
      ],
    }));


    const modelTrainingFunction = new lambda.DockerImageFunction(this, "modelTrainingFunction", {
      code: lambda.DockerImageCode.fromEcr(modelTrainingAsset.repository, {
        tagOrDigest: modelTrainingAsset.imageTag
      }),
      architecture: Architecture.ARM_64,
      timeout: Duration.minutes(5),
      memorySize: 512,
      role: modelTrainingRole,
      environment: {
        MLFLOW_IP: mlflowElasticIp.ref
      }
    });

    dataBucket.grantReadWrite(dataProcessingFunction);
    dataBucket.grantReadWrite(modelTrainingFunction);

    const dag = new Dag(this, 'DAGStack', {
      dataProcessingFunction: dataProcessingFunction,
      modelTrainingFunction: modelTrainingFunction,
    });

    const mlflowBucket = new s3.Bucket(this, 'MLflowArtifactsBucket', {
      bucketName: `mlflow-data-bucket-${this.account}-${this.region}`,
      versioned: true,
      encryption: s3.BucketEncryption.S3_MANAGED,
      removalPolicy: cdk.RemovalPolicy.DESTROY, // Be cautious with this in production
      autoDeleteObjects: true, // Be cautious with this in production
    });

    mlflowBucket.grantReadWrite(modelTrainingFunction);

    const mlflow = new MlflowConstruct(this, 'MyEC2WithEIP', {
      vpc,
      elasticIp: mlflowElasticIp,
      mlflowBucket
    });

    new cdk.CfnOutput(this, 'PublicIP', {
      value: mlflowElasticIp.ref,
      description: 'Mlflow public IP address',
    });

    const webService = new WebService(this, 'WebService', {})

  }
}

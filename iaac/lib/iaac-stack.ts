import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as ecr_assets from 'aws-cdk-lib/aws-ecr-assets';
import * as s3 from 'aws-cdk-lib/aws-s3';
import {Architecture} from "aws-cdk-lib/aws-lambda";
import {Duration} from "aws-cdk-lib";


export class IaacStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const dataBucket = new s3.Bucket(this, 'BikeDurationPredictorBucket', {
      bucketName: `bike-duration-predictor-${this.account}`,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    const dataProcessingAsset = new ecr_assets.DockerImageAsset(this, 'DataProcessingAsset', {
      directory: '../bike_duration_predictor',
      file: 'dataprocessing.dockerfile'
    });

    const dataProcessingFunction = new lambda.DockerImageFunction(this, "dataProcessingFunction", {
      code: lambda.DockerImageCode.fromEcr(dataProcessingAsset.repository, {
        tagOrDigest: dataProcessingAsset.imageTag
      }),
      architecture: Architecture.ARM_64,
      timeout: Duration.minutes(5),
      memorySize: 512
    });

    dataBucket.grantReadWrite(dataProcessingFunction);
  }
}

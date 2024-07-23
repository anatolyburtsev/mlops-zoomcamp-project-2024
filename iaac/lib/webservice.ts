import * as cdk from "aws-cdk-lib";
import {Construct} from "constructs";
import * as ecr_assets from "aws-cdk-lib/aws-ecr-assets";
import * as lambda from "aws-cdk-lib/aws-lambda";
import {Architecture} from "aws-cdk-lib/aws-lambda";
import {Duration} from "aws-cdk-lib";
import * as apigateway from 'aws-cdk-lib/aws-apigateway';

type WebServiceProps = cdk.StackProps & {}

export class WebService extends cdk.Stack {
  constructor(scope: Construct, id: string, props: WebServiceProps) {
    super(scope, id, props);

    const webServiceAsset = new ecr_assets.DockerImageAsset(this, 'WebServiceAsset', {
      directory: '../bike_duration_predictor',
      file: 'webservice.dockerfile'
    });

    const webServiceFunction = new lambda.DockerImageFunction(this, "WebServiceFunction", {
      code: lambda.DockerImageCode.fromEcr(webServiceAsset.repository, {
        tagOrDigest: webServiceAsset.imageTag
      }),
      architecture: Architecture.ARM_64,
      timeout: Duration.minutes(5),
      memorySize: 512
    });

    const api = new apigateway.RestApi(this, 'bike-prediction-api', {
      restApiName: 'Bike Prediction Service',
      description: 'This service predicts bike sharing ride duration.'
    });

    const predictIntegration = new apigateway.LambdaIntegration(webServiceFunction, {
      requestTemplates: { "application/json": '{ "statusCode": "200" }' }
    });

    const predictResource = api.root.addResource('predict');
    predictResource.addMethod('POST', predictIntegration);

    // Output the API endpoint
    new cdk.CfnOutput(this, 'APIEndpoint', {
      value: api.url,
    });

  }
}
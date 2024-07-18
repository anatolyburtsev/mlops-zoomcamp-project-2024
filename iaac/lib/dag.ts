import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as stepfunctions from 'aws-cdk-lib/aws-stepfunctions';
import * as tasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import * as lambda from 'aws-cdk-lib/aws-lambda';

type DAGStackProps = cdk.StackProps & {
  dataProcessingFunction: lambda.Function;
  modelTrainingFunction: lambda.Function;
};

export class Dag extends cdk.Stack {
  constructor(scope: Construct, id: string, props: DAGStackProps) {
    super(scope, id, props);

    const dataProcessingTask = new tasks.LambdaInvoke(this, 'DataProcessingTask', {
      lambdaFunction: props.dataProcessingFunction,
      resultPath: stepfunctions.JsonPath.DISCARD,
    })
      .addRetry({ maxAttempts: 1 });

    // Define the second task
    const modelTrainingTask = new tasks.LambdaInvoke(this, 'ModelTrainingTask', {
      lambdaFunction: props.modelTrainingFunction,
      resultPath: stepfunctions.JsonPath.DISCARD,
    })
      .addRetry({ maxAttempts: 1 })


    // Define the state machine
    const definition = stepfunctions.Chain
      .start(dataProcessingTask)
      .next(modelTrainingTask);

    const stateMachine = new stepfunctions.StateMachine(this, 'MyStateMachine', {
      definitionBody: stepfunctions.DefinitionBody.fromChainable(definition),
      stateMachineName: 'DataProcessingAndModelTrainingWorkflow',
      timeout: cdk.Duration.minutes(10)
    });

    new cdk.CfnOutput(this, 'StateMachineArn', {
      value: stateMachine.stateMachineArn,
      description: 'State Machine ARN',
    });
  }
}

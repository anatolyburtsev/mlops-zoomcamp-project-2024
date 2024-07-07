import click
import joblib
from src.data_processing import process_data
from src.train_model import train_model
from src.utils import parse_s3_path, read_from_s3, read_from_local, write_to_s3, write_to_local


@click.group()
def cli():
    pass


@click.command()
@click.option('--input-path', required=True, help='The path to the input CSV file. Can be local or S3 path.')
@click.option('--output-path', required=True, help='The path to the output CSV file. Can be local or S3 path.')
def process(input_path, output_path):
    if input_path.startswith('s3://'):
        input_bucket, input_key = parse_s3_path(input_path)
        click.echo('Reading data from S3...')
        df = read_from_s3(input_bucket, input_key)
    else:
        click.echo('Reading data from local file...')
        df = read_from_local(input_path)

    click.echo('Processing data...')
    processed_df = process_data(df)

    if output_path.startswith('s3://'):
        output_bucket, output_key = parse_s3_path(output_path)
        click.echo('Writing processed data to S3...')
        write_to_s3(processed_df, output_bucket, output_key)
    else:
        click.echo('Writing processed data to local file...')
        write_to_local(processed_df, output_path)

    click.echo('Data processing complete.')


@click.command()
@click.option('--input-path', required=True, help='The path to the processed CSV file. Can be local or S3 path.')
@click.option('--output-path', required=True,
              help='The path to save the trained model and metrics. Can be local or S3 path.')
def train(input_path, output_path):
    if input_path.startswith('s3://'):
        input_bucket, input_key = parse_s3_path(input_path)
        click.echo('Reading processed data from S3...')
        df = read_from_s3(input_bucket, input_key)
    else:
        click.echo('Reading processed data from local file...')
        df = read_from_local(input_path)

    click.echo('Training model...')
    trained_model = train_model(df)

    model_file = 'model.pkl'
    metrics = trained_model.metrics.__dict__

    joblib.dump(trained_model.model, model_file)

    if output_path.startswith('s3://'):
        output_bucket, output_key_base = parse_s3_path(output_path)
        click.echo('Uploading model and metrics to S3...')
        write_to_s3(model_file, output_bucket, f"{output_key_base}/model.pkl")
        write_to_s3(metrics, output_bucket, f"{output_key_base}/metrics.json")
    else:
        click.echo('Saving model and metrics to local files...')
        write_to_local(model_file, f"{output_path}/model.pkl")
        write_to_local(metrics, f"{output_path}/metrics.json")

    click.echo('Model training complete.')


cli.add_command(process)
cli.add_command(train)

if __name__ == '__main__':
    cli()

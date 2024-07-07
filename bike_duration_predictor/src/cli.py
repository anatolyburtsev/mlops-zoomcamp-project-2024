import click
from src.data_processing import process_data
from src.utils import parse_s3_path, read_from_s3, read_from_local, write_to_s3, write_to_local


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


if __name__ == '__main__':
    process()

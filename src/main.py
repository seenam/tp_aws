import json
import boto3
import os

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff')

def lambda_handler(event, context):
    print("Event: ", json.dumps(event))

    table_name = os.environ['DYNAMODB_TABLE']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    for record in event.get('Records', []):
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        filename = key.split('/')[-1]

        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            print(f"Fichier ignoré (non-image) : {filename}")
            continue

        response = table.get_item(Key={'filename': filename})
        if 'Item' in response:
            print(f"Fichier déjà existant dans la BD : {filename}")
            continue

        table.put_item(Item={
            'filename': filename,
            'bucket': bucket,
            'key': key
        })
        print(f"Fichier ajouté dans la BD : {filename}")

    return {
        'statusCode': 200,
        'body': json.dumps('Traitement terminé')
    }

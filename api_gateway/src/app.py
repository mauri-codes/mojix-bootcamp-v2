import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

table_name = os.environ['CINEMA_TABLE']

dynamodb = boto3.resource('dynamodb')
cinema_table = dynamodb.Table(table_name)

def add_reservation(event, context):
    # show_id, person_id -> body
    body = json.loads(event["body"])
    cinema_table.update_item(
        Key={
            'pk': 'show_' + body["show_id"],
            'sk': 'person_' + body["person_id"]
        }
    )
    print(json.dumps(event))
    return {
        'statusCode': 200,
        'body': json.dumps({
            "success": True
        })
    }
def display_show(event, context):
    # /show/{show_id}
    path_parameters = event["pathParameters"]
    show_id = path_parameters["show_id"]
    response = cinema_table.query(
        KeyConditionExpression=Key('pk').eq('show_' + show_id)
    )
    items = response['Items']
    print(items)
    return {
        'statusCode': 200,
        'body': json.dumps({
            "success": True,
            "list": items
        })
    }
    
def display_movie(event, context):
    # /?movie_id={movie_id}
    query_params = event["queryStringParameters"]
    movie_id = query_params["movie_id"]
    response = cinema_table.query(
        KeyConditionExpression=Key('pk').eq('movie_' + movie_id)
    )
    items = response['Items']
    print(items)
    return {
        'statusCode': 200,
        'body': json.dumps({
            "success": True,
            "list": items
        })
    }

import datetime

import boto3
from boto3.session import Session
import json
from decimal import Decimal
from datetime import date, datetime
from botocore.exceptions import ClientError
import base64

cfn = boto3.client('cloudformation')
cloudwatch = boto3.client('cloudwatch')

# for Decimal json.dump
def decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError


def get_stacks(token=None):
    option = {
        'StackStatusFilter': ['CREATE_COMPLETE', 'UPDATE_COMPLETE']
    }

    if token is not None:
        option['NextToken'] = token

    res = cfn.list_stacks(**option)
    stacks = res.get('StackSummaries', [])

    if 'NextToken' in res:
        stacks += get_stacks(res['NextToken'])
    return stacks


def get_stack_resources(stack_name, token=None):
    option = {
        'StackName': stack_name
    }

    if token is not None:
        option['NextToken'] = token

    res = cfn.list_stack_resources(**option)
    resources = res.get('StackResourceSummaries', [])

    if 'NextToken' in res:
        resources += get_stack_resources(res['NextToken'])
    return resources


def cloud_watch(physical, start, end):

    json_load = {
        "metrics": [
            ["AWS/Lambda", "Invocations", "FunctionName", physical, {"stat": "Sum", "id": "m0"}]
        ],
        "legend": {
            "position": "bottom"
        },
        "period": 300,
        "view": "timeSeries",
        "stacked": False,
        "title": "All resource - Invocations",
        "width": 1000,
        "height": 500,
        "start": start,
        "end": end
    }

    print(json_load)

    try:
        response = cloudwatch.get_metric_widget_image(
            MetricWidget=json.dumps(json_load)
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return "hogefuga"
    else:
        data_encode_bytes = base64.b64encode(response["MetricWidgetImage"])
        print(response["MetricWidgetImage"])
        data_encode_str = data_encode_bytes.decode('utf-8')
        return data_encode_str


def lambda_handler(event, context):
    end = event['queryStringParameters']['end']
    start = event['queryStringParameters']['start']

    region = "ap-northeast-1"
    session = Session(
        region_name=region
    )
    dynamodb = session.resource('dynamodb')
    rds = boto3.client('rds')

    stacks = get_stacks()

    # 各スタックのリソース数を調べる
    result = []
    for stack in stacks:
        stack_name = stack['StackName']
        resources = get_stack_resources(stack_name)
        for resource in resources:
            if resource["ResourceType"] == "AWS::Lambda::Function":
                image = cloud_watch(resource["PhysicalResourceId"], start, end)
                result.append({
                    'StackName': stack_name,
                    'Resources': resource["PhysicalResourceId"],
                    'Image': image,
                })

    response = {
        "start": start,
        "end": end,
        "num_results": len(result),
        "results": result
    }
    # jsonstr = json.dumps(stacks, default=decimal_default_proc)
    result2 = json.dumps(response, default=decimal_default_proc)

    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        'body': result2
    }


message = {
    "status": "NG",
    "message": "Hello from AWS Lambda"
}

if __name__ == '__main__':
    print(lambda_handler("", ""))

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

global start
global end
global type

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


def cloud_watch(type,metrics,physical):

    json_load = {}
    if type == "Lambda" and metrics == "Invocations":
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
    elif type == "Lambda" and metrics == "Duration":
        json_load = {
            "metrics": [
                [ "AWS/Lambda", "Duration", "FunctionName", physical, { "stat": "Average", "id": "m0" } ]
            ],
            "legend": {
                "position": "bottom"
            },
            "period": 300,
            "view": "timeSeries",
            "stacked": False,
            "title": "All resource - Duration",
            "width": 1000,
            "height": 500,
            "start": start,
            "end": end
        }

    try:
        response = cloudwatch.get_metric_widget_image(
            MetricWidget=json.dumps(json_load)
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {"image": "hogefuga", "type": type, "metrics": metrics }
    else:
        data_encode_bytes = base64.b64encode(response["MetricWidgetImage"])
        data_encode_str = data_encode_bytes.decode('utf-8')
        return {"image": data_encode_str, "type": type, "metrics": metrics }


def lambda_handler(event, context):

    global start
    global end
    if not event == "":
        end = event['queryStringParameters']['end']
        start = event['queryStringParameters']['start']
        type = event['queryStringParameters']['type']
    else:
        start = "PT1H"
        end = "P0D"
        type = "All"

    region = "ap-northeast-1"
    session = Session(
        region_name=region
    )
    dynamodb = session.resource('dynamodb')
    rds = boto3.client('rds')

    stacks = get_stacks()

    # 各スタックのリソース数を調べる
    result = []
    resource_list = []
    for stack in stacks:
        stack_name = stack['StackName']
        resources = get_stack_resources(stack_name)
        for resource in resources:
            resource_list.append(resource)
            if resource["ResourceType"] == "AWS::Lambda::Function" and (type == "All" or type == "Lambda"):
                image = cloud_watch("Lambda", "Invocations", resource["PhysicalResourceId"])
                result.append({
                    'StackName': stack_name,
                    'Resources': resource["PhysicalResourceId"],
                    'Image': image["image"],
                    'Type': "Lambda",
                    'Metrics': "Invocations",
                })
                image = cloud_watch("Lambda", "Duration", resource["PhysicalResourceId"])
                result.append({
                    'StackName': stack_name,
                    'Resources': resource["PhysicalResourceId"],
                    'Image': image["image"],
                    'Type': "Lambda",
                    'Metrics': "Duration",

                })

    response = {
        "start": start,
        "end": end,
        "num_results": len(result),
        "results": result,
        "resource_list": resource_list
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

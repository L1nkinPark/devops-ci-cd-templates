import json

def lambda_handler(event, context):
    # for debug
    print("DEBUG INPUT FROM CLIENT:")
    print(event)
    
    # Hỗ trợ cả hai trường hợp: Test trực tiếp trên Lambda (Direct Event) hoặc gọi qua API Gateway Proxy (bật Lambda Proxy Integration)
    if isinstance(event, dict) and 'body' in event:
        # Nếu event nhận từ API Gateway Proxy, event['body'] là chuỗi JSON string
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    else:
        body = event
        
    firstNum = body['firstNum']
    secondNum = body['secondNum']
    operator = body['operator'] # ADD, MULTIPLE, DEVIDE, SUBSTRACT
    # Process the request
    result = calculate(firstNum, secondNum, operator)
    
    # Create the response body
    response_body = {
        'message': 'Request processed successfully',
        'result': result
    }
    
    # Create the HTTP response
    response = {
        'statusCode': 200,
        'body': json.dumps(response_body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    
    return response

def calculate(num1, num2, operator):
    if operator == 'ADD':
        return num1 + num2
    elif operator == 'SUBSTRACT':
        return num1 - num2
    elif operator == 'MULTIPLE':
        return num1 * num2
    elif operator == 'DEVIDE':
        return num1 / num2
    else:
        return 0

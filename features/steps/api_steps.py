#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

from behave import when, then
from features.api.api_client import ApiClient
import json
from datetime import datetime
import time

@when('I send GET request to "{endpoint}" and "{params}"')
def step_impl(context, endpoint,params):
    context.api_client = ApiClient()
    context.response = context.api_client.get(endpoint, params=params)

    assert context.response is not None, "API response is None. The request might have failed."


@then('the response status code should be {status_code:d}')
def step_impl(context, status_code):
    assert context.response.status_code == status_code, \
        f"Expected status code {status_code}, but got {context.response.status_code}"

@then('the response should match "{expected_response_file}"')
def step_impl(context, expected_response_file):
    expected_response = context.api_client.load_test_responces_data(expected_response_file)
    actual_response = context.response.json()
    
    assert actual_response == expected_response, \
        f"Response doesn't match expected. Differences: {json.dumps(actual_response, indent=2)}"

@then('the response should have the following structure')
def step_impl(context):
    response_json = context.response.json()
    for row in context.table:
        field = row['field']
        expected_value = int(row['value'])  # Convert to int since we're dealing with numbers
        assert field in response_json, f"Field '{field}' not found in response"
        assert response_json[field] == expected_value, \
            f"Expected {field} to be {expected_value}, but got {response_json[field]}"

@then('each user in response should have required fields')
def step_impl(context):
    response_json = context.response.json()
    required_fields = [row[0] for row in context.table]
    
    for user in response_json['data']:
        for field in required_fields:
            assert field in user, f"Field '{field}' missing in user data: {user}" 

@when('I send POST request to "{endpoint}" with data from "{request_file}"')
def step_impl(context, endpoint, request_file):
    context.api_client = ApiClient()
    request_data = context.api_client.load_test_requests_data(f"requests/{request_file}")
    context.response = context.api_client.post(endpoint, request_data)

@then('the response should contain "{field}" field')
def step_impl(context, field):
    response_json = context.response.json()
    assert field in response_json, \
        f"Field '{field}' not found in response: {json.dumps(response_json, indent=2)}"

@then('the token should not be empty')
def step_impl(context):
    response_json = context.response.json()
    assert response_json['token'], "Token is empty"
    assert isinstance(response_json['token'], str), "Token is not a string"
    assert len(response_json['token']) > 0, "Token length is 0" 

@when('I send PUT request to "{endpoint}" with data from "{request_file}"')
def step_impl(context, endpoint, request_file):
    context.api_client = ApiClient()
    request_data = context.api_client.load_test_requests_data(f"requests/{request_file}")
    context.response = context.api_client.put(endpoint, request_data)

@when('I send PATCH request to "{endpoint}" with data from "{request_file}"')
def step_impl(context, endpoint, request_file):
    context.api_client = ApiClient()
    request_data = context.api_client.load_test_requests_data(f"requests/{request_file}")
    context.response = context.api_client.patch(endpoint, request_data)

@then('the response should contain fields')
def step_impl(context):
    response_json = context.response.json()
    for row in context.table:
        field = row[0]
        expected_value = row[1]
        assert field in response_json, \
            f"Field '{field}' not found in response: {json.dumps(response_json, indent=2)}"
        assert response_json[field] == expected_value, \
            f"Expected {field} to be '{expected_value}', but got '{response_json[field]}'"

@then('the "{field}" should be a valid timestamp')
def step_impl(context, field):
    response_json = context.response.json()
    timestamp = response_json[field]
    try:
        # Try to parse the timestamp
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as e:
        raise AssertionError(f"Invalid timestamp format: {timestamp}. Error: {str(e)}") 

@when('I send DELETE request to "{endpoint}"')
def step_impl(context, endpoint):
    context.api_client = ApiClient()
    context.response = context.api_client.delete(endpoint)

@then('the response body should be empty')
def step_impl(context):
    assert len(context.response.content) == 0, \
        f"Expected empty response body, but got: {context.response.content}" 

@when('I send POST request to "{endpoint}" with data')
def step_impl(context, endpoint):
    context.api_client = ApiClient()
    # Convert table to dictionary
    request_data = {row[0]: row[1] for row in context.table}
    context.response = context.api_client.post(endpoint, request_data)

@when('I send PUT request to "{endpoint}" with data')
def step_impl(context, endpoint):
    context.api_client = ApiClient()
    # Convert table to dictionary
    request_data = {row[0]: row[1] for row in context.table}
    context.response = context.api_client.put(endpoint, request_data)

@then('the "{field}" field should contain "{expected_text}"')
def step_impl(context, field, expected_text):
    response_json = context.response.json()
    assert field in response_json, \
        f"Field '{field}' not found in response: {json.dumps(response_json, indent=2)}"
    actual_text = str(response_json[field])
    assert expected_text in actual_text, \
        f"Expected text '{expected_text}' not found in '{field}' field. Got: '{actual_text}'" 

@when('I send GET request to "{endpoint}" with delay of {delay:d} seconds')
def step_impl(context, endpoint, delay):
    context.api_client = ApiClient()
    
    # Record start time
    start_time = time.time()
    
    context.response = context.api_client.get(endpoint, params={'delay': delay})
    
    # Calculate and store response time
    context.response_time = time.time() - start_time

@then('the response time should be less than {max_time:d} seconds')
def step_impl(context, max_time):
    assert context.response_time < max_time, \
        f"Response took {context.response_time:.2f} seconds, which is more than {max_time} seconds"

    # Log the actual response time
    print(f"Request completed in {context.response_time:.2f} seconds") 
            
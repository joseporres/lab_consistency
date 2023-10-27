import requests
import concurrent.futures

# Define the URL of your API endpoint
url = "http://localhost:8000/v1"

# Define the number of concurrent requests you want to send
num_requests = 2  # You can adjust this number

# Define the function to send a single HTTP request
def send_request(i):
    try:
        response = requests.get(url)
        return f"Request {i}: Status Code {response.status_code}"
    except Exception as e:
        return f"Request {i}: Failed with error {str(e)}"

# Create a ThreadPoolExecutor to send concurrent requests
with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
    # Submit the tasks for concurrent execution
    future_to_request = {executor.submit(send_request, i): i for i in range(num_requests)}
    
    # Wait for all tasks to complete
    for future in concurrent.futures.as_completed(future_to_request):
        i = future_to_request[future]
        result = future.result()
        print(result)

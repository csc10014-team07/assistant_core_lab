PART E - Testing API

E.2 With curl
Testing Progress:
Step 1: Activate Virtual Environment. In my case i use the command: .venv\Scripts\activate
Step 2: Run the serve:r uvicorn assistant_api.main:create_app --factory --reload
Is success, you would see a message: Uvicorn running on http://127.0.0.1:8000
Step 3: Open a new Terminal and Activate Virtual Environment like the former step
Step 4: Run bash api-tests/curl_tests.sh
The result would show up on my screen
== health (expect 200)
{"status":"ok","version":"1.0.0"}  [200]

== chat fee (expect 200)
Internal Server Error  [500]

== chat rule with source (200)
Internal Server Error  [500]

== chat empty (expect 422)
{"error":{"code":"invalid_request","message":"message: String should have at least 1 character"}}  [422]

== chat wrong type (expect 422)
{"error":{"code":"invalid_request","message":"message: Input should be a valid string"}}  [422]

== feedback (expect 201)
Internal Server Error  [500]

== feedback bad rating (422)
{"error":{"code":"invalid_request","message":"rating: Input should be less than or equal to 1"}}  [422]

== list feedback no key (401)
{"error":{"code":"missing_or_invalid_api_key","message":"Missing or invalid API key"}}  [401]

== list feedback with key (200)
{"error":{"code":"missing_or_invalid_api_key","message":"Missing or invalid API key"}}  [401]

== weather (200, or 503 if down)
Internal Server Error  [500]

== unknown route (404)
{"detail":"Not Found"}  [404]

*Note: You can check issue #16 for evidence


===========================================================================================================

E.3 With Postman or Bruno

Part 1: Install Dependencies and Run the Backend
Step 1. Navigate to the Starter Directory
$ cd starter

Step 2. Activate the Python Virtual Environment
$ source ../.venv/Scripts/activate

Step 3. Install Dependencies
Install the required packages:
$ python -m pip install -r requirements.txt

Install the project in editable mode:
$ python -m pip install -e .

Step 4. Start the API Server
Run:
$ python -m uvicorn assistant_api.main:create_app --factory --reload

Part 2: Test API Endpoints Using Postman
Step 1. Import file api-tests/study-assistant.postman_collection.json

Step 2. Click "Send" to run per Test

Result:
- health 
{
    "status": "ok",
    "version": "1.0.0"
}
- chat - fee
{
    "answer": "Your tuition is 9,450,000 VND.",
    "intent": "fee",
    "sources": [],
    "degraded": false,
    "request_id": "c91fc44cdd28"
}
- chat - rule
{
    "answer": "Based on 'Thesis registration': Students may register a thesis when they have at least 120 accumulated credits and a GPA of at least 2.0.",
    "intent": "rule",
    "sources": [
        {
            "id": "H26-5.3",
            "title": "Thesis registration"
        }
    ],
    "degraded": false,
    "request_id": "4e0abf7dd499"
}
- chat - empty
{
    "error": {
        "code": "invalid_request",
        "message": "message: String should have at least 1 character"
    }
}
- feedback - add
{
    "request_id": "abc123",
    "rating": 1,
    "comment": null,
    "id": 1,
    "created_at": "2026-11-05T13:43:55.902090Z"
}
- feedback - list
{
    "error": {
        "code": "missing_or_invalid_api_key",
        "message": "Missing or invalid API key"
    }
}
- weather 
{
    "temperature_c": 28.1,
    "wind_kmh": 6.2,
    "description": "clear sky",
    "observed_at": "2026-11-05T13:45",
    "stale": false
}

===========================================================================================================

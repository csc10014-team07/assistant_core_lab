PART E - Testing API

E.3 With curl
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
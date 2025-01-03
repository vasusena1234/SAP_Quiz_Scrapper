import pandas as pd
import requests

# File containing the URLs
csv_file = "urlnew.csv"
post_url = "https://learning.sap.com/service/quiz/verifyResponses"

# Load the URLs from the CSV file
try:
    url_data = pd.read_csv(csv_file)
    if 'url' not in url_data.columns:
        raise ValueError(f"Column 'url' not found in {csv_file}. Ensure the file is properly formatted.")

    results = {}

    # Loop through each URL
    for index, fetch_url in enumerate(url_data['url']):
        try:
            print(f"Processing URL {index + 1}: {fetch_url}")

            # Fetch the data
            response = requests.get(fetch_url)
            response.raise_for_status()
            data = response.json()

            # Extracting data to build the payload
            quiz_id = data["pageProps"]["data"]["quiz"]["ID"]
            questions = data["pageProps"]["data"]["quiz"]["questions"]

            payload = {
                "quizID": quiz_id,
                "responses": [],
                "progressRequest": {
                    "learningObject": {
                        "objId": data["pageProps"]["data"]["nav"]["courses"][0]["units"][0]["objId"],
                        "objType": "quiz",
                        "release": "1"
                    },
                    "parents": [
                        {
                            "objId": data["pageProps"]["data"]["nav"]["objId"],
                            "objType": "learning-journey",
                            "release": "1"
                        },
                        {
                            "objId": data["pageProps"]["data"]["nav"]["courses"][0]["objId"],
                            "objType": "course",
                            "release": "1"
                        },
                        {
                            "objId": data["pageProps"]["data"]["nav"]["courses"][0]["units"][0]["objId"],
                            "objType": "unit",
                            "release": "1"
                        }
                    ]
                },
                "metrics": {
                    "timeSpent": 193090
                }
            }

            # Initialize results for each question
            for question in questions:
                results[question["ID"]] = {
                    "questionText": question["questionText"],
                    "questionType": question.get("questionType", "unknown"),
                    "responseTexts": [option["responseText"] for option in question["options"]],
                    "correctOptionIDs": []
                }

            # Simulate responses and make POST requests
            #here we are ssuming that there are max 7 options possible for one question, but can be incresed or decresed accordingly
            #for every question we are making post call by making a{n} as an option and checking if it is right answer or not
            #if it is right we will append to result dictionary.
            for i in range(1, 8):
                responses = []
                for question in questions:
                    responses.append({
                        "questionID": question["ID"],
                        "response": ["a" + str(i)]
                    })

                payload["responses"] = responses

                # Make a POST request with the payload
                headers = {
                    "Content-Type": "application/json",
                    "Cookie": "Your Cookie goes here(Mandatory for posting to the post url)"  # Replace with actual cookie if required
                }
                post_response = requests.post(post_url, headers=headers, json=payload).json()

                # Process POST response to update results
                options = post_response["questionDetails"]
                for q in options:
                    correct_options = [
                        opt["optionID"]
                        for opt in q["optionDetails"]
                        if opt["isCorrect"]
                    ]
                    # Map "a1", "a2", etc. to "a", "b", etc.
                    mapped_options = [chr(96 + int(opt[1:])) for opt in correct_options]  # Convert to alphabet
                    results[q["questionID"]]["correctOptionIDs"].extend(mapped_options)

            print(f"Results for URL {index + 1}: {results}")

        except KeyError as e:
            print(f"Error parsing JSON data from {fetch_url}: Missing key {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error processing URL {fetch_url}: {e}")

except FileNotFoundError:
    print(f"Error: File {csv_file} not found.")
except Exception as e:
    print(f"Error: {e}")

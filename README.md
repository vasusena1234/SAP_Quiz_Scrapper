# Quiz URL Processor

## Overview
This script automates the process of fetching quiz data from a list of URLs, extracting relevant information, and simulating responses to determine the correct answers for each quiz question. The results are stored in a dictionary, which is output in JSON-like format and can be parsed for further use. The script is designed for Python enthusiasts and developers looking to showcase their ability to work with APIs, JSON, and HTTP requests in their portfolios.

---

## Features
- **Automated URL Processing:** Reads URLs from a CSV file and fetches JSON data.
- **Quiz Data Extraction:** Extracts quiz ID, questions, and related details.
- **Simulated Responses:** Posts simulated responses to identify correct answers.
- **JSON-Like Output:** Outputs results in a structured dictionary that can be converted to JSON.
- **Error Handling:** Includes robust error handling for missing keys, invalid responses, and network issues.

---

## Prerequisites
Before running the script, ensure the following:
1. **Python Installation:** Install Python 3.7 or higher.
2. **Libraries:** The script requires the following Python libraries:
   - `pandas`
   - `requests`

   Install them using pip:
   ```bash
   pip install pandas requests
   ```
3. **CSV File:** Prepare a CSV file named `urlnew.csv` containing a column `url` with the URLs to process.

4. **Cookie Configuration:** Replace the placeholder in the `headers` section with your valid cookie value to authorize POST requests:
   ```python
   "Cookie": "Your Cookie goes here(Mandatory for posting to the post url)"
   ```

---

## File Structure
- `name.py`: The script file.
- `urlnew.csv`: The CSV file containing the URLs.

---

## How to Run
1. Save the script as `name.py`.
2. Place the `urlnew.csv` file in the same directory as the script.
3. Run the script and redirect output to a file:
   ```bash
   python name.py > output.txt
   ```

---

## Script Output
- The script generates a dictionary for each URL processed.
- This dictionary contains:
  - `questionText`: The text of each question.
  - `questionType`: The type of the question.
  - `responseTexts`: A list of available responses for the question.
  - `correctOptionIDs`: A list of correct answer options mapped to alphabetical representations (e.g., `a`, `b`, `c`).
- The output is saved in `output.txt` and can be parsed as JSON for further processing.

### Example Output
```json
{
    "12345": {
        "questionText": "What is Python?",
        "questionType": "multiple-choice",
        "responseTexts": ["A programming language", "A snake", "A coffee brand"],
        "correctOptionIDs": ["a"]
    }
}
```

---

## Key Components of the Script
1. **CSV Handling:**
   ```python
   url_data = pd.read_csv(csv_file)
   ```
   Loads the URLs from the `urlnew.csv` file.

2. **Data Extraction:**
   ```python
   quiz_id = data["pageProps"]["data"]["quiz"]["ID"]
   questions = data["pageProps"]["data"]["quiz"]["questions"]
   ```
   Extracts quiz data from the fetched JSON.

3. **Simulated Responses:**
   Simulates responses by iterating over possible options (`a1`, `a2`, ..., `a7`) and making POST requests.

4. **POST Request:**
   ```python
   post_response = requests.post(post_url, headers=headers, json=payload).json()
   ```
   Sends the payload to the endpoint to validate responses.

5. **Error Handling:**
   Handles various exceptions, such as missing keys, HTTP errors, or file not found errors.

---

## Error Handling and Debugging
- **File Not Found:**
  If the CSV file is missing, an error message is displayed:
  ```
  Error: File urlnew.csv not found.
  ```
- **Invalid JSON Key:**
  If a key is missing in the JSON response:
  ```
  Error parsing JSON data from <URL>: Missing key <KeyName>
  ```
- **Network Errors:**
  Handles network-related issues using `requests.exceptions.RequestException`.

---

## Notes
- **Customizing Options:** The script assumes a maximum of 7 options per question. Adjust this range in the `for i in range(1, 8)` loop if needed.
- **Authorization:** Ensure that the cookie in the `headers` is valid to avoid authentication errors during POST requests.
- **Output Parsing:** Use any JSON parser to process the output and transform it into the required format.

---

## Conclusion
This script showcases Python's capabilities in handling APIs, JSON data, and automating repetitive tasks. Its modular design, robust error handling, and structured output make it an ideal addition to any developer's portfolio.


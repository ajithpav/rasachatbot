# Rasa Chatbot with Custom Actions

## Overview
This Rasa chatbot is designed to handle multiple intents related to telecom services and general inquiries. It includes custom actions for retrieving country data from a CSV file and integrating a Mongolian BERT model for NLP processing.

## Features
- **Intent Handling:** Supports various user intents related to telecom plans, rewards, eligibility, and balance inquiries.
- **Custom Actions:**
  - `action_country_data`: Retrieves country information from a CSV file.
  - `mongolian_bert_action`: Uses a Mongolian BERT model for text processing.
- **Entity Recognition:** Extracts phone numbers and email IDs.
- **Slot Filling:** Captures and stores user-provided details like phone numbers and emails.
- **Custom Responses:** Provides static responses for different intents.

## Installation
### Prerequisites
- Python 3.7+
- Rasa Open Source
- Transformers
- Pandas
- PyTorch
- CSV file (`countries.csv`) with country data

### Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate  # For Windows
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Train the Model**
   ```bash
   rasa train
   ```
5. **Run the Rasa Server**
   ```bash
   rasa run --enable-api
   ```
6. **Run the Action Server**
   ```bash
   rasa run actions
   ```
7. **Test the Bot**
   ```bash
   rasa shell
   ```

## Custom Actions
### `action_country_data`
- Reads data from `countries.csv`.
- Extracts country name, full name, and capital city.
- Returns formatted country information.

### `mongolian_bert_action`
- Loads `tugstugi/bert-base-mongolian-cased` model.
- Uses `fill-mask` task for text processing.
- Generates and returns masked token predictions.

## Intents
- **User Queries:** `greet`, `goodbye`, `confused`, `cheer_up`, `express`
- **Telecom Services:** `check_balance`, `check_bill`, `prepaid`, `postpaid`
- **Plan Information:** `plans`, `amazon_prime_offer`, `rewards_claim_process`
- **Technical Queries:** `ask_for_churn_chart_image`, `subscriptions_tabular_data`
- **Personal Info:** `phone`, `gmailid`

## Entities
- `number`: Extracts phone numbers.
- `mailid`: Extracts email addresses.

## Slots
- `phone`: Stores extracted phone numbers.
- `gmailid`: Stores extracted email IDs.

## Responses
The chatbot provides predefined responses for different user intents, including general information, greetings, and telecom-related inquiries.

## API Endpoints
- **Rasa API**: `http://localhost:5005/webhooks/rest/webhook`
- **Action Server API**: `http://localhost:5055/webhook`

## Contributing
Feel free to open issues or submit pull requests to improve the chatbot.

## License
This project is licensed under the MIT License.


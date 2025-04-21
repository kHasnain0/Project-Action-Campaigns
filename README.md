# Salesforce Campaign Data Parser

A Python tool for parsing and cleaning campaign data exported from Salesforce. This script reads a CSV file containing **ACTIONCAMPAIGNID** and **CAMPAIGN_COOKIE_DATA_JSON** columns, decodes and parses the JSON in the `CAMPAIGN_COOKIE_DATA_JSON` field, cleans up UTM parameters, and generates a new CSV file with structured and cleaned data.

## Features

- Decodes and parses URL-encoded JSON data from Salesforce campaign tracking data.
- Cleans up UTM parameters, ensuring the values are readable and properly decoded.
- Handles missing or incomplete data, skipping rows and logging the issues.
- Outputs a clean, structured CSV with user-friendly column headers and progress updates.
- Uses a terminal progress bar to track processing status for large datasets.

## Prerequisites

Before you can run the script, ensure you have the following installed:

- Python 3.6 or higher
- Python libraries:
  - `tqdm` for the progress bar
  - `json`, `csv`, and `urllib.parse` (these are part of Python's standard library, so no installation needed)

You can install `tqdm` via pip:

```bash
pip install tqdm 
 ```

## Setup

### Prerequisites
Before using this script, ensure you have the following installed:
- **Python 3.x**: Ensure that you have Python 3 or higher installed.
- **tqdm library**: This script uses `tqdm` to show a progress bar during CSV processing. Install it using pip.

### Installation

1. Clone the repository:
   git clone https://github.com/kHasnain0/Project-Action-Campaigns.git
   cd Project-Action-Campaigns

2.  Install the required Python libraries:
    pip install tqdm


### 4. **Usage**
1. Prepare a CSV file that contains two columns:
   - `ACTIONCAMPAIGNID` (Campaign identifier)
   - `CAMPAIGN_COOKIE_DATA_JSON` (Encoded JSON string containing campaign and URL parameters)

2. Save your CSV file in the same directory as the script.

3. Run the script from the terminal with the following command:
   ```bash
   python campaign_parser.py

4. Follow the prompt to enter the name of the input CSV file.

5. Once processing is complete, the script will generate a new CSV file with the parsed data. The output will contain all the relevant fields like campaign name, visitor ID, URL tracking information, etc.


Example:
Input CSV:

| ACTIONCAMPAIGNID | CAMPAIGN_COOKIE_DATA_JSON                                                                                                  |
|------------------|-----------------------------------------------------------------------------------------------------------------------------|
| 1234             | %7B%22Campaign_Name__c%22%3A%22Campaign+1%22%2C%22Visitor_ID__c%22%3A%2212345%22%2C%22utm_medium%22%3A%22email%22%7D         |


### 5. **Contributing**

## Contributing

Contributions are welcome! If you find any issues or would like to add new features, feel free to fork this repository and submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to your branch (`git push origin feature-branch`).
5. Create a pull request.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

import urllib.parse
import json
import csv
import os
import sys
from typing import Dict, Any, List
from tqdm import tqdm


class CampaignParser:
    CAMPAIGN_FIELDS = [
        'Campaign_Name__c', 'Campaign_Content__c', 'Campaign_Keywords__c',
        'Campaign_Medium__c', 'Campaign_Referrer__c', 'Campaign_Page__c'
    ]

    VISITOR_FIELDS = [
        'Visitor_ID__c', 'Visitor_IP_Address__c', 'Campaign_Page_View_Count__c',
        'First_Visit_Time__c', 'Previous_Session_Start_Time__c', 'Current_Session_Start_Time__c',
        'Campaign_Session_Count__c', 'Campaign_Hit_Count__c', 'Responded_Date__c'
    ]

    UTM_FIELDS = [
        'utm_source', 'utm_medium', 'utm_term', 'utm_content', 'utm_campaign', 'utm_id',
        'gclid', 'gbraid', 'wbraid', 'gad_source', 'gclsrc', '_hsenc', '_hsmi',
        'fbclid', 'ccid', 'campaign'
    ]

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def _log(self, message: str) -> None:
        if self.verbose:
            print(message)

    def _decode_campaign_data(self, encoded_data: str) -> Dict[str, Any]:
        decoded_data = urllib.parse.unquote(encoded_data)
        try:
            parsed = json.loads(decoded_data)
            if isinstance(parsed, list) and parsed:
                return parsed[0]
            elif isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            self._log("⚠️ Failed to decode JSON.")
        return {}

    def _parse_url_params(self, url: str) -> Dict[str, str]:
        def clean_value(val: str) -> str:
            return urllib.parse.unquote_plus(val.lstrip('=+').strip())

        parsed_url = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed_url.query)
        return {k: clean_value(v[0]) for k, v in query.items()}

    def _build_campaign_data(self, campaign_data: Dict[str, Any], url_params: Dict[str, str]) -> Dict[str, str]:
        campaign_info = {f: campaign_data.get(f, '') for f in self.CAMPAIGN_FIELDS}
        visitor_info = {f: campaign_data.get(f, '') for f in self.VISITOR_FIELDS}
        url_tracking = {
            f: url_params.get(f, campaign_data.get(f, ''))
            for f in self.UTM_FIELDS
        }
        return {**campaign_info, **visitor_info, **url_tracking}

    def process_csv(self, input_csv: str, output_csv: str) -> None:
        results: List[Dict[str, str]] = []
        skipped = 0

        try:
            with open(input_csv, mode='r', encoding='utf-8-sig') as infile:
                reader = csv.DictReader(infile)
                rows = list(reader)

                for i, row in enumerate(tqdm(rows, desc="🔄 Processing records", unit="record"), start=1):
                    row = {k.strip(): v for k, v in row.items()}
                    record_id = row.get('ACTIONCAMPAIGNID', '').strip()
                    encoded = row.get('CAMPAIGN_COOKIE_DATA_JSON', '').strip()

                    if not record_id or not encoded:
                        skipped += 1
                        tqdm.write(f"⚠️ Skipped row {i}: Missing required fields")
                        continue

                    campaign_data = self._decode_campaign_data(encoded)
                    if not campaign_data:
                        skipped += 1
                        tqdm.write(f"⚠️ Skipped row {i}: Invalid campaign cookie data")
                        continue

                    url_params = self._parse_url_params(campaign_data.get('Campaign_Page__c', ''))
                    parsed_row = self._build_campaign_data(campaign_data, url_params)
                    parsed_row = {'Record ID': record_id, **parsed_row}
                    results.append(parsed_row)

            if not results:
                print("⚠️ No valid records to write.")
                return

            headers = list(results[0].keys())
            with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(results)

            print(f"\n✅ Done! Exported {len(results)} records to '{output_csv}'.")
            if skipped:
                print(f"⚠️ Skipped {skipped} record(s) due to issues.")

        except FileNotFoundError:
            print(f"❌ File '{input_csv}' not found.")
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")

    def run_from_terminal(self):
        print("🟢 Campaign CSV Parser\n")
        input_file = input("📥 Enter the input CSV file name (e.g., input.csv): ").strip()
        output_file = f"parsed_{os.path.splitext(input_file)[0]}.csv"
        self.process_csv(input_file, output_file)


if __name__ == "__main__":
    CampaignParser(verbose=False).run_from_terminal()

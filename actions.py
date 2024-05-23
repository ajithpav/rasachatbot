from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import random
import pandas as pd

class ActionCountryData(Action):
    def name(self) -> Text:
        return "action_country_data"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Read country data from CSV filesentry
        country_data = pd.read_csv("countries.csv", delimiter="|")  # Assuming your CSV file is delimited by "|"
        
        # Extracting required information
        countries = country_data["country"]
        full_names = country_data["country_full_name"]
        capital_cities = country_data["capital_city"]
        
        # Formulate the response
        response = "Here is some country data:\n"
        for country, full_name, capital_city in zip(countries, full_names, capital_cities):
            response += f"Country: {country}\nFull Name: {full_name}\nCapital City: {capital_city}\n\n"

        dispatcher.utter_message(text=response)

        return []
    
class MongolianBertAction(Action):
 
    def name(self) -> Text:
        return "mongolian_bert_action"
 
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            "tugstugi/bert-base-mongolian-cased", use_fast=False
        )
        self.model = AutoModelForMaskedLM.from_pretrained(
            "tugstugi/bert-base-mongolian-cased"
        )
        self.pipe = pipeline(
            task="fill-mask", model=self.model, tokenizer=self.tokenizer
        )
 
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        user_input = tracker.latest_message["text"]
        output_ = self.pipe(f"[MASK] {user_input}")
        for i in range(len(output_)):
            print(output_[i])
 
        dispatcher.utter_message(text=output_[0]["sequence"])
 
        return {}
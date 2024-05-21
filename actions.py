import os
import re
from typing import Any, Text, Dict, List
import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import tabula
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
from typing import Any, Text, Dict, List
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher


class ExtractTableFromPdf(Action):
    def name(self):
        return "Subscriptions_Tabular_Data_View"

    def run(self, dispatcher, tracker, domain):
        response = convert_pdf_to_txt()
        dispatcher.utter_message(image=response)
        return []


class GenerateChurnGraph(Action):
    def name(self):
        return "churn_monthly_charge_graph_View"

    def run(self, dispatcher, tracker, domain):
        response = generate_graph()
        dispatcher.utter_message(text="Here's the graph:",image=response,)
        return []
    


def convert_pdf_to_txt():
 
    filepath = r"trai.pdf"
    tables = tabula.read_pdf(filepath, pages="all", multiple_tables=True)
    result = pd.DataFrame(tables[0])
 
    plt.figure(figsize=(10, 5))
    plt.table(cellText=result.values, colLabels=result.columns, loc="center")
    plt.axis("off")
    path = f"{uuid.uuid1()}.png"
    file_name = f"{uuid.uuid4()}.png"
    path = f"{os.getcwd()}/{file_name}"
    plt.savefig(path)
    plt.close()
    url = f"http://localhost:8080/{file_name}"
 
    return url
 


def generate_graph():
    tele_data = pd.read_csv("Telecom_Industry.csv")

    churned_monthly_charge_between_zero_fifty = tele_data[
        (tele_data["Churn"] == 1)
        & (tele_data["MonthlyCharge"] >= 0)
        & (tele_data["MonthlyCharge"] <= 50)
    ]
    churned_monthly_charge_between_fifty_hundred = tele_data[
        (tele_data["Churn"] == 1)
        & (tele_data["MonthlyCharge"] > 50)
        & (tele_data["MonthlyCharge"] <= 100)
    ]
    churned_monthly_charge_greater_hundred = tele_data[
        (tele_data["Churn"] == 1) & (tele_data["MonthlyCharge"] > 100)
    ]

    churned_monthly_charge_between_zero_fifty_per = (
        churned_monthly_charge_between_zero_fifty.shape[0] / tele_data.shape[0]
    ) * 100
    churned_monthly_charge_between_fifty_hundred_per = (
        churned_monthly_charge_between_fifty_hundred.shape[0] / tele_data.shape[0]
    ) * 100
    churned_monthly_charge_greater_hundred_per = (
        churned_monthly_charge_greater_hundred.shape[0] / tele_data.shape[0]
    ) * 100

    sns.set_style("whitegrid")

    percentage_data = [
        round(churned_monthly_charge_between_zero_fifty_per),
        round(churned_monthly_charge_between_fifty_hundred_per),
        round(churned_monthly_charge_greater_hundred_per),
    ]

    plt.figure(figsize=(8, 6))
    ax = sns.barplot(
        x=[
            "0 - 50 rs",
            "51 - 100 rs",
            "101 - 150 rs",
        ],
        y=percentage_data,
        hue=[
            "0 - 50 rs",
            "51 - 100 rs",
            "101 - 150 rs",
        ],
        palette="pastel",
        legend=False,
    )
    ax.set(
        xlabel="customers monthly charge",
        ylabel="percentage of churned Customers",
        title="Distribution of Churn Customers in terms of monthly charge",
    )
    for index, _ in enumerate(range(3)):
        ax.text(
            index,
            percentage_data[index],
            f"{percentage_data[index]}%",
            fontsize=14,
            color="black",
            ha="center",
        )
    plt.xticks(rotation=45)
    plt.tight_layout()
    file_name = f"{uuid.uuid4()}.png"
    path = f"{os.getcwd()}/{file_name}"
    plt.savefig(path)
    url = f"http://localhost:8080/{file_name}"
    return url



class action_monthly_charge_impact(Action):
 
    # How does the average monthly bill (MonthlyCharge) impact churn rate?
    def name(self) -> Text:
        return "action_monthly_charge_impact"
 
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
 
        tele_Data = pd.read_csv("Telecom_Industry.csv")
 
        churned = tele_Data[(tele_Data["Churn"] == 1)]
        active = tele_Data[(tele_Data["Churn"] == 0)]
 
        churned_monthly_charge_mean = churned["MonthlyCharge"].mean()
        active_monthly_charge_mean = active["MonthlyCharge"].mean()
 
        churned_percentage = (churned.shape[0] / tele_Data.shape[0]) * 100
 
        if churned_monthly_charge_mean > active_monthly_charge_mean:
 
            response = f"Increase in average of {round(churned_monthly_charge_mean - active_monthly_charge_mean,2)} rs of monthly charge may affected churn rate. Current churn rate is: {round(churned_percentage,2)}%"
            print(response)
            dispatcher.utter_message(text=response)
 
        else:
 
            response = (
                f"increasing on monthly price has no effect on churn rate, but current churn rate is: {round(churned_percentage,2)}%",
            )
            print(response)
            dispatcher.utter_message(text=response)
 
        return []
    
class action_data_plan_churn_comparison(Action):
    # Are customers with data plans less likely to churn compared to those without data plans?
    def name(self):
        return "action_data_plan_churn_comparison"
 
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
 
        tele_Data = pd.read_csv("Telecom_Industry.csv")
 
        churned_and_have_data_plan = tele_Data[
            (tele_Data["DataPlan"] == 1) & (tele_Data["Churn"] == 1)
        ].shape[0]
 
        churned_and_have_no_data_plan = tele_Data[
            (tele_Data["DataPlan"] == 0) & (tele_Data["Churn"] == 1)
        ].shape[0]
 
        if churned_and_have_data_plan < churned_and_have_no_data_plan:
 
            response = (
                f"yes, customers with data plans less likely to churn compared to those without data plans. More details:"
                f"total churned customers with data plans -> {round(churned_and_have_data_plan,2)},"
                f"total churned customers without data plans -> {round(churned_and_have_no_data_plan,2)},"
                f"in an average of {round(tele_Data.describe().mean()['AccountWeeks'] / 52.14,2)} yrs."
            )
            print(response)
            dispatcher.utter_message(text=response)
 
        else:
 
            response = (
                f"No, customers with data plans are not less likely to churn compared to those without data plans. More details:"
                f"total churned customers with data plans -> {round(churned_and_have_data_plan,2)},"
                f"total churned customers without data plans -> {round(churned_and_have_no_data_plan,2)},"
                f"in an average of {round(tele_Data.describe().mean()['AccountWeeks'] / 52.14,2)} yrs."
            )
 
            print(response)
            dispatcher.utter_message(text=response)
 
        return []

class action_correlation_CustServCalls_churn(Action):
    # What is the correlation between each feature and churn?
    def name(self):
        return "action_correlation_CustServCalls_churn"
 
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
 
        tele_data = pd.read_csv("Telecom_Industry.csv")
        correlation_coefficient = tele_data.corr(method="pearson")["CustServCalls"][
            "Churn"
        ]
        if (correlation_coefficient >= 0) & (correlation_coefficient <= 0.5):
 
            response = f"correlation cofficient is {round(correlation_coefficient,2)}.It indicates a weak or no linear relationship between the variables. In this case, the number of customer service calls may not have a significant impact on churn."
            print(response)
            dispatcher.utter_message(text=response)
            return []
 
        elif (correlation_coefficient >= 0.5) & (correlation_coefficient <= 1):
 
            response = f"correlation cofficient is {round(correlation_coefficient,2)} ,it indicates a strong positive linear relationship between the variables. In this case, a higher number of customer service calls may be associated with a higher likelihood of churn."
            print(response)
            dispatcher.utter_message(text=response)
            return []
 
        else:
 
            response = f"correlation cofficient is {round(correlation_coefficient,2)}, it indicates a negative linear relationship between the variables."
            print(response)
            dispatcher.utter_message(text=response)
            return []
    
    
class ActionContractRenewalChurnComparison(Action):
    # Do customers who recently renewed their contract (ContractRenewal) exhibit lower churn rates?
    def name(self) -> Text:
        return "action_contract_renewal_churn_comparison"
 
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
 
        tele_data = pd.read_csv("Telecom_Industry.csv")
 
        recently_renewed = tele_data[
            (tele_data["ContractRenewal"] == 1) & (tele_data["Churn"] == 1)
        ].shape[0]
        not_renewed = tele_data[
            (tele_data["ContractRenewal"] == 0) & (tele_data["Churn"] == 1)
        ].shape[0]
 
        if recently_renewed > not_renewed:
            response = (
                f"No, customers who recently renewed their contract exhibit higher churn rates. "
                f"Details: total customers churned who recently renewed service -> {round(recently_renewed,2)}, "
                f"and total customers churned who recently did not renew service -> {round(not_renewed,2)}."
            )
        elif recently_renewed < not_renewed:
            response = (
                f"Yes, customers who recently renewed their contract exhibit lower churn rates. "
                f"Details: total customers churned who recently renewed service -> {round(recently_renewed,2)}, "
                f"and total customers churned who recently did not renew service -> {round(not_renewed,2)}."
            )
        else:
            response = (
                f"Customers who recently renewed their contract and customers who recently did not renew their contract exhibit the same churn rates. "
                f"Details: total customers churned who recently renewed service -> {round(recently_renewed,2)}, "
                f"and total customers churned who recently did not renew service -> {round(not_renewed,2)}."
            )
            
        print(response)
        dispatcher.utter_message(text=response)
        return []

    
class action_customer_serv_calls_churn_comparison(Action):
    # Is there a relationship between the number of calls to customer service (CustServCalls) and churn?
    def name(self):
        return "action_customer_serv_calls_churn_comparison"
 
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        tele_Data = pd.read_csv("Telecom_Industry.csv")
        churned = (
            tele_Data[(tele_Data["Churn"] == 1)].describe().mean()["CustServCalls"]
        )
 
        active = tele_Data[(tele_Data["Churn"] == 0)].describe().mean()["CustServCalls"]
 
        if churned < active:
 
            response = f"For customers who churned, the mean number of customer service calls is approximately {round(churned,2)}. For customers who did not churn, the mean number of customer service calls is approximately {round(active,2)}."
            conclusion = (
                "It indicates that there may be a relationship between the number of calls to customer service and churn. "
                "The customers who churned tended to have fewer interactions with customer service compared to customers who did not churn. "
                "This could suggest that dissatisfaction or issues with the service may have led to churn for some customers."
            )
            print(response, conclusion)
            dispatcher.utter_message(text=f"{response}. {conclusion}")
 
        else:
 
            response = f"For customers who churned, the mean number of customer service calls is approximately {round(churned,2)} .For customers who did not churn, the mean number of customer service calls is approximatel {round(active,2)} ."
            conclusion = "It indicates that that there may be a relationship between the number of calls to customer service and churn. The customers who churned tended to have more interactions with customer service compared to customers who did not churn. This could suggest that dissatisfaction or issues with the service may have led to churn for some customers."
            print(response, conclusion)
            dispatcher.utter_message(text=f"{response}. {conclusion}")
 
        return []
    

class ExtractEmailAddress(Action):
    def name(self) -> Text:
        return "action_say_phone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        phone = tracker.get_slot("phone")

        if not phone:
            dispatcher.utter_message(text="Sorry, I don't know your phone number.")
        else:
            dispatcher.utter_message(text=f"Your phone number is {phone}.")

        return []
    

class ExtractEmailidAddress(Action):
    def name(self) -> Text:
        return "action_say_mailid"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mailid = tracker.get_slot("gmailid")  # Update this line to retrieve the "gmailid" slot

        if not mailid:
            dispatcher.utter_message(text="Sorry, I don't have your mailid.")
        else:
            dispatcher.utter_message(text=f"Your mailid is {mailid}.")  # Update this line to mention mailid

        return []
    

class SelectColor(Action):
    def name(self) -> Text:
        return "action_select_color"

    def run(self, dispatcher: CollectingDispatcher, tracker: Any, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [
            {"title": "Red", "payload": "red"},
            {"title": "Blue", "payload": "blue"},
            {"title": "Green", "payload": "green"},
        ]
        dispatcher.utter_message(text="Choose a color:", buttons=buttons)
        return []


        
    


    
    





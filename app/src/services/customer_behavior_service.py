import io
import numpy as np
import pandas as pd
import base64
import seaborn as sns

from fastapi import UploadFile, File
import matplotlib.pyplot as plt


async def import_customer_behaviors(
    file: UploadFile = File(...),
):

    df = pd.read_csv(file.file)
    buffer = io.StringIO()
    df.info(buf=buffer)
    FileInfo = buffer.getvalue()
    headData = df.head()
    # # Cleaning the Data
    df.dropna(inplace=True)

    # Analysis and Visualization

    # Gender
    Gender = df["Gender"].value_counts().reset_index()
    gender_pie_chart = generate_gender_pie_chart(Gender)

    # Gender with Age
    GenderwithAge = df.groupby("Gender")["Age"].value_counts().reset_index()
    GenderwithAgeChart = generate_genderwithage_bar_chart(GenderwithAge)

    # Gender With Membershiptype
    GenderWithMembershiptype = (
        df[["Gender", "Membership Type"]].value_counts().reset_index()
    )
    GenderWithMembershiptype_chart = generate_GenderWithMembershiptype_bar_chart(
        GenderWithMembershiptype
    )

    # The member ship between the all values
    member_ship_between_chart = member_ship_between_the_all_values_chart(df)

    # The number for customers for all ages
    The_number_for_customers_for_all_ages = The_number_for_customers_for_all_ages_chart(
        df
    )

    # Gender with City
    GenderwithCity = df[["Gender", "City"]].value_counts().reset_index()
    GenderwithCity_chart = generate_GenderwithCity_chart(GenderwithCity)
    # Membership Type
    MembershipType = df["Membership Type"].value_counts().reset_index()
    membership_type_chart = generate_membership_type_chart(MembershipType)

    # Number of customers in any membership type
    NumberofcustomersinanymembershiptypeChart = generate_membership_type_pie_chart(
        MembershipType
    )
    # Membership Type and Total Spend
    MembershipTypeandTotalSpend = (
        df[["Membership Type", "Total Spend"]]
        .value_counts()
        .reset_index()
        .sort_values(by="Total Spend", ascending=True)
    )
    MembershipTypeandTotalSpendChart = generate_membership_type_spend_chart(
        MembershipTypeandTotalSpend
    )
    # Distribution Days Since Last Purchase
    DistributionDaysSinceLastPurchaseChart = generate_purchase_histogram(df)
    # Satisfaction Level
    SatisfactionLevel = df["Satisfaction Level"].value_counts().reset_index()
    SatisfactionLevelChart = generate_satisfaction_level_chart(SatisfactionLevel)

    # Items Purschased with Gender
    ItemsPurschased = (
        df.groupby("Gender")["Items Purchased"].value_counts().reset_index()
    )
    ItemsPurschasedwithGenderChart = generate_items_purchased_by_gender_chart(
        ItemsPurschased
    )

    # Discount Applied with Gender
    DiscountApplied = (
        df.groupby("Gender")["Discount Applied"].value_counts().reset_index()
    )
    DiscountAppliedwithGenderChart = generate_discount_applied_by_gender_chart(
        DiscountApplied
    )

    # Average Rating with Satisfaction Level
    satisfaction_rating = df.groupby("Satisfaction Level")["Average Rating"].mean()
    AverageRatingwithSatisfactionLevelChart = average_rating_plot(satisfaction_rating)

    return {
        "success": True,
        "FileInfo": FileInfo,
        "headData": headData.to_html(),
        "Gender": Gender.to_html(),
        "gender_pie_chart": gender_pie_chart,
        "GenderwithAge": GenderwithAge.to_html(),
        "GenderwithAgeChart": GenderwithAgeChart,
        "GenderWithMembershiptype": GenderWithMembershiptype.to_html(),
        "GenderWithMembershiptype_chart": GenderWithMembershiptype_chart,
        "member_ship_between_chart": member_ship_between_chart,
        "The_number_for_customers_for_all_ages": The_number_for_customers_for_all_ages,
        "GenderwithCity_chart": GenderwithCity_chart,
        "membership_type_chart": membership_type_chart,
        "NumberofcustomersinanymembershiptypeChart": NumberofcustomersinanymembershiptypeChart,
        "MembershipTypeandTotalSpendChart": MembershipTypeandTotalSpendChart,
        "DistributionDaysSinceLastPurchaseChart": DistributionDaysSinceLastPurchaseChart,
        "SatisfactionLevelChart": SatisfactionLevelChart,
        "ItemsPurschasedwithGenderChart": ItemsPurschasedwithGenderChart,
        "DiscountAppliedwithGenderChart": DiscountAppliedwithGenderChart,
        "AverageRatingwithSatisfactionLevelChart": AverageRatingwithSatisfactionLevelChart,
    }


def generate_gender_pie_chart(Gender):
    # Create the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(
        Gender["count"],
        colors=["skyblue", "pink"],
        shadow=True,
        labels=Gender["Gender"],
        autopct="%1.2f%%",
    )
    plt.legend()

    # Save it to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()  # Close the figure to free memory
    buf.seek(0)

    # Convert to base64
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    return encoded


def generate_genderwithage_bar_chart(GenderwithAge):
    # Create the bar chart
    plt.figure(figsize=(8, 8))
    plt.bar(GenderwithAge["Gender"], GenderwithAge["Age"], color=["pink", "skyblue"])
    plt.xlabel("Gender")
    plt.ylabel("Age")
    plt.title("Age by Gender")

    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    # Encode to base64
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_b64


def generate_GenderWithMembershiptype_bar_chart(GenderWithMembershiptype):
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=GenderWithMembershiptype, x="Gender", y="count", hue="Membership Type"
    )
    plt.title("Gender Distribution by Membership Type")

    # Save chart to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    # Convert to base64
    chart_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return chart_b64


def member_ship_between_the_all_values_chart(df):
    # Prepare the data
    gender_age_data = (
        df[["Gender", "Age"]]
        .value_counts()
        .reset_index()
        .sort_values(ascending=False, by="count")
    )

    # Create the plot
    plt.figure(figsize=(8, 8))
    sns.barplot(
        data=gender_age_data,
        x="Age",
        y="count",
        hue="Gender",
        palette=["pink", "skyblue"],
    )
    plt.title("Age Distribution")
    plt.legend(loc=(1.05, 0.9))

    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)

    # Convert to base64
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_b64


def The_number_for_customers_for_all_ages_chart(df):
    # Prepare the data
    age_data = df["Age"].value_counts().reset_index()
    age_data.columns = ["Age", "count"]

    # Create the bar plot
    plt.figure(figsize=(8, 8))
    sns.barplot(data=age_data, x="Age", y="count")
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")  # Rotate the labels for better readability
    plt.title("Age by Count")
    plt.tight_layout()  # Adjust layout to prevent clipping of labels

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    # Convert to base64
    chart_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return chart_b64


def generate_GenderwithCity_chart(df):
    # Prepare the data
    labels = df["City"]
    counts = df["count"]

    # Create the pie chart
    plt.figure(figsize=(8, 10))
    plt.pie(counts, shadow=True, labels=labels, autopct="%1.2f%%")
    plt.legend(loc=(0.8, 1))

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    # Convert to base64
    chart_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return chart_b64


def generate_membership_type_chart(df):
    # Create the Seaborn bar plot
    plt.figure(figsize=(8, 8))

    # Set hue to "Membership Type" and use a color palette with enough colors
    sns.barplot(
        data=df,
        x="Membership Type",
        y="count",
        hue="Membership Type",
        palette="dark:red",  # Or use other Seaborn palettes like 'Blues', 'Set1', etc.
    )

    # Disable legend if you don't want it (or set to False)
    plt.legend([], [], frameon=False)  # Hide the legend, or set legend=False

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)

    # Convert to base64
    chart_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return chart_b64


def generate_membership_type_pie_chart(df):
    # Prepare the data
    labels = df["Membership Type"]
    counts = df["count"]

    # Create the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(
        counts,
        colors=["skyblue", "pink", "darkred"],
        shadow=True,
        labels=labels,
        autopct="%1.2f%%",
    )
    plt.legend(loc=(0.8, 1))

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    # Convert to base64
    chart_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return chart_b64


def generate_membership_type_spend_chart(df):
    # Create the bar plot
    plt.figure(figsize=(8, 8))
    plt.bar(
        df["Membership Type"], df["Total Spend"], label="Total Spend", color="darkred"
    )
    plt.legend(loc="upper left")
    plt.xlabel("Membership Type")
    plt.ylabel("Total Spend")
    plt.title("Total Spend by Membership Type")

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)

    # Convert to base64
    chart_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return chart_b64


def generate_purchase_histogram(df):
    # Create the histogram
    plt.figure(figsize=(8, 6))
    sns.histplot(
        df["Days Since Last Purchase"], color="darkred", kde=True
    )  # Optional KDE line
    plt.title("Distribution of Days Since Last Purchase")
    plt.xlabel("Days Since Last Purchase")
    plt.ylabel("Frequency")

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)

    # Convert to base64
    chart_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return chart_b64


def generate_satisfaction_level_chart(df):
    # Create the bar plot
    plt.figure(figsize=(8, 8))
    plt.bar(
        df["Satisfaction Level"],
        df["count"],
        label="Satisfaction Level",
        color="darkred",
    )
    plt.legend(loc="upper right")  # Adjust the location of the legend
    plt.xlabel("Satisfaction Level")
    plt.ylabel("Count")

    # Rotate x-axis labels
    plt.xticks(rotation=45)

    # Set title
    plt.title("Satisfaction Level VS Count")

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)

    # Convert to base64
    chart_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return chart_b64


def generate_items_purchased_by_gender_chart(ItemsPurschased):
    # Create the bar plot
    plt.figure(figsize=(8, 8))
    ax = sns.barplot(
        data=ItemsPurschased,
        x="Gender",
        y="Items Purchased",
        hue="Gender",
        palette=["pink", "skyblue"],
    )

    # Manually set the legend labels
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, title="Gender")

    # Set plot labels and title
    plt.xlabel("Gender")
    plt.ylabel("Items Purchased")
    plt.title("Items Purchased by Gender")

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)

    # Convert to base64
    chart_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return chart_b64


def generate_discount_applied_by_gender_chart(DiscountApplied):
    # Create the bar plot
    plt.figure(figsize=(8, 8))
    sns.barplot(
        data=DiscountApplied,
        x="Gender",
        y="Discount Applied",
        hue="Discount Applied",
        palette=["pink", "skyblue"],
    )

    # Set plot labels and title
    plt.xlabel("Gender")
    plt.ylabel("Count")
    plt.title("Count of Discounts Applied by Gender")
    plt.legend(title="Discount Applied")

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)

    # Convert to base64
    chart_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return chart_b64


def average_rating_plot(satisfaction_rating):
    # Create the bar plot
    plt.figure(figsize=(8, 6))
    satisfaction_rating.plot.bar(color="darkred")

    # Adding labels and title
    plt.ylabel("Average Rating")
    plt.title("Average Rating by Satisfaction Level")

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)

    # Convert to base64
    chart_b64 = base64.b64encode(buf.read()).decode("utf-8")
    return chart_b64

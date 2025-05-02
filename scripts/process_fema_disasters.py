import pandas as pd
import os

def process_fema_disasters():
    os.makedirs("data/processed/", exist_ok=True)
    df = pd.read_csv("data/raw/DisasterDeclarationsSummaries.csv", low_memory=False)
    df["declarationDate"] = pd.to_datetime(df["declarationDate"], errors="coerce")
    df["year"] = df["declarationDate"].dt.year
    df = df[["state", "year", "incidentType"]].dropna()
    grouped = df.groupby(["state", "year", "incidentType"]).size().reset_index(name="count")
    pivoted = grouped.pivot(index=["state", "year"], columns="incidentType", values="count").fillna(0).reset_index()
    pivoted.to_csv("data/processed/fema_disasters_by_state.csv", index=False)
    print("Processed FEMA disaster declarations")

if __name__ == "__main__":
    process_fema_disasters()

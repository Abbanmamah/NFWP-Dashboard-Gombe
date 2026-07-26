import pandas as pd
import plotly.express as px


def chart_wags(summary):

    df = pd.DataFrame(summary).T.reset_index()
    df.rename(columns={"index": "LGA"}, inplace=True)

    fig = px.bar(
        df,
        x="LGA",
        y="WAGs",
        color="LGA",
        title="WAGs by LGA"
    )

    fig.update_layout(showlegend=False)

    return fig


def chart_members(summary):

    df = pd.DataFrame(summary).T.reset_index()
    df.rename(columns={"index": "LGA"}, inplace=True)

    fig = px.bar(
        df,
        x="LGA",
        y="Members",
        color="LGA",
        title="Members by LGA"
    )

    fig.update_layout(showlegend=False)

    return fig


def chart_savings(summary):

    df = pd.DataFrame(summary).T.reset_index()
    df.rename(columns={"index": "LGA"}, inplace=True)

    fig = px.bar(
        df,
        x="LGA",
        y="Savings",
        color="LGA",
        title="Savings by LGA"
    )

    fig.update_layout(showlegend=False)

    return fig


def chart_loans(summary):

    df = pd.DataFrame(summary).T.reset_index()
    df.rename(columns={"index": "LGA"}, inplace=True)

    fig = px.bar(
        df,
        x="LGA",
        y="Loan Disbursed",
        color="LGA",
        title="Loan Disbursed by LGA"
    )

    fig.update_layout(showlegend=False)

    return fig
import plotly.express as px

## chart helpers
# color sets
sequential = [
    "#E5FAFF",
    "#B7F2FF",
    "#8AEAFF",
    "#5CE1FF",
    "#2FD9FF",
    "#00D1FF",
    "#00B0D6",
    "#006D85",
    "#004B5C",
]
categorical = ["#00D1FF", "#EB46FF", "#6B59FF", "#4FD1C5", "#1F68AC", "#FDE8FF"]


def chart_bars(df, x_col, y_cols, title, color=None, height=400):
    fig = px.bar(
        df,
        x=x_col,
        y=y_cols,
        title=title,
        color=color,
        color_discrete_sequence=categorical,
        template="plotly_dark",
    )

    # remove axis labels
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="", tickprefix="$")

    # calculate width
    width = height * 1.91

    # Update layout for dark theme readability
    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        width=width,
        height=height,
    )

    return fig
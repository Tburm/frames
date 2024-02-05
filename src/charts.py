from datetime import datetime
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
    fig.update_xaxes(
        title_text="",
        automargin=True,
    )
    fig.update_yaxes(title_text="", tickprefix="$")

    # calculate width
    width = height * 1.91

    # Update layout for dark theme readability
    fig.update_layout(
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=None,
        ),
        width=width,
        height=height,
        font=dict(
            family="sans-serif",
        ),
        plot_bgcolor="#06061B",
        paper_bgcolor="#06061B",
    )

    # add the last updated timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fig.add_annotation(
        text="Last updated: " + current_time,
        x=-0.07,
        y=-0.3,
        xref="paper",
        yref="paper",
        showarrow=False,
    )
    return fig

def chart_lines(df, x_col, y_cols, title, color=None, smooth=False, height=400):
    fig = px.line(
        df,
        x=x_col,
        y=y_cols,
        title=title,
        color=color,
        color_discrete_sequence=categorical,
        template="plotly_dark",
    )

    fig.update_traces(
        hovertemplate=None,
        line_shape=None if smooth else "hv",
    )

    # remove axis labels
    fig.update_xaxes(
        title_text="",
        automargin=True,
    )
    fig.update_yaxes(title_text="", tickprefix="$")

    # calculate width
    width = height * 1.91

    # Update layout for dark theme readability
    fig.update_layout(
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=None,
        ),
        width=width,
        height=height,
        font=dict(
            family="sans-serif",
        ),
        plot_bgcolor="#06061B",
        paper_bgcolor="#06061B",
    )

    # add the last updated timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fig.add_annotation(
        text="Last updated: " + current_time,
        x=-0.07,
        y=-0.3,
        xref="paper",
        yref="paper",
        showarrow=False,
    )
    return fig

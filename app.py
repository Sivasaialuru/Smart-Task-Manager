import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Smart Task Manager",
    page_icon="✅",
    layout="wide"
)

st.title("✅ Smart Task Manager")

FILE_NAME = "tasks.csv"

if not os.path.exists(FILE_NAME):
    pd.DataFrame(
        columns=[
            "task",
            "priority",
            "category",
            "status"
        ]
    ).to_csv(FILE_NAME, index=False)

df = pd.read_csv(FILE_NAME)

st.sidebar.header("Add New Task")

task = st.sidebar.text_input(
    "Task Name"
)

priority = st.sidebar.selectbox(
    "Priority",
    ["High", "Medium", "Low"]
)

category = st.sidebar.selectbox(
    "Category",
    [
        "Study",
        "Coding",
        "Personal",
        "Health"
    ]
)

if st.sidebar.button("Add Task"):

    if task:

        new_task = pd.DataFrame(
            {
                "task": [task],
                "priority": [priority],
                "category": [category],
                "status": ["Pending"]
            }
        )

        df = pd.concat(
            [df, new_task],
            ignore_index=True
        )

        df.to_csv(
            FILE_NAME,
            index=False
        )

        st.success(
            "Task Added Successfully"
        )

total_tasks = len(df)

completed_tasks = len(
    df[df["status"] == "Completed"]
)

pending_tasks = len(
    df[df["status"] == "Pending"]
)

completion_rate = 0

if total_tasks > 0:
    completion_rate = (
        completed_tasks /
        total_tasks
    ) * 100

st.header("📊 Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Tasks",
    total_tasks
)

col2.metric(
    "Completed",
    completed_tasks
)

col3.metric(
    "Pending",
    pending_tasks
)

col4.metric(
    "Completion %",
    f"{completion_rate:.1f}%"
)

st.subheader("📋 Task List")

if not df.empty:

    for i in range(len(df)):

        col1, col2, col3 = st.columns([6, 2, 2])

        with col1:

            st.write(
                f"**{df.loc[i,'task']}** | "
                f"{df.loc[i,'priority']} | "
                f"{df.loc[i,'category']} | "
                f"{df.loc[i,'status']}"
            )

        with col2:

            if (
                df.loc[i, "status"]
                == "Pending"
            ):

                if st.button(
                    f"Complete {i}"
                ):

                    df.loc[
                        i,
                        "status"
                    ] = "Completed"

                    df.to_csv(
                        FILE_NAME,
                        index=False
                    )

                    st.rerun()

        with col3:

            if st.button(
                f"Delete {i}"
            ):

                df = df.drop(i)

                df.to_csv(
                    FILE_NAME,
                    index=False
                )

                st.rerun()

st.subheader("📈 Task Analytics")

if total_tasks > 0:

    status_chart = px.pie(
        df,
        names="status",
        title="Task Status Distribution"
    )

    st.plotly_chart(
        status_chart,
        use_container_width=True
    )

    category_chart = px.bar(
        df["category"]
        .value_counts()
        .reset_index(),
        x="category",
        y="count",
        title="Tasks By Category"
    )

    st.plotly_chart(
        category_chart,
        use_container_width=True
    )

st.subheader("📄 Data")

st.dataframe(
    df,
    use_container_width=True
)
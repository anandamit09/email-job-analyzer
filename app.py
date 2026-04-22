import streamlit as st
import pandas as pd
from fetch_emails import fetch_emails
from extractor import extract_info

st.title("📧 Email Job Analyzer")

placement_email = st.text_input("Enter Sender Email")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if st.button("Analyze Emails"):

    with st.spinner("Fetching emails..."):
        emails = fetch_emails(
            placement_email,
            str(start_date),
            str(end_date)
        )

    st.write(f"Total Emails Found: {len(emails)}")

    results = []
    progress = st.progress(0)

    for i, email in enumerate(emails):
        text = email["subject"] + "\n" + email["body"]

        #FILTER NON-JOB EMAILS (improves accuracy)
        if not any(word in text.lower() for word in [
            "job", "placement", "hiring", "role", "ctc", "package", "lpa"
        ]):
            continue

        data = extract_info(text)

        if data:
            results.append(data)

        progress.progress((i + 1) / len(emails))

    if results:
        df = pd.DataFrame(results)

        #CLEAN DATA
        df = df.drop_duplicates()

        #Remove useless rows
        df = df[
            df["role"].notna() |
            df["package"].notna() |
            df["location"].notna()
        ]

        st.success("Extraction Complete!")
        st.dataframe(df)

        #Save Excel
        file_path = "output.xlsx"
        df.to_excel(file_path, index=False)

        with open(file_path, "rb") as f:
            st.download_button(
                label="Download Excel",
                data=f,
                file_name="job_data.xlsx"
            )
    else:
        st.warning("No relevant job emails found.")
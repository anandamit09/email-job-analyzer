HOW TO RUN

Step 1: Clone Repo
git clone https://github.com/your-username/email-job-analyzer.git

cd email-job-analyzer

Step 2: Create Virtual environment
python -m venv venv

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Setup Gmail Access
Enable 2-Step Verification
Generate App Password
Add your email + app password in `fetch_emails.py`

Step 5: Add Groq API Key
Replace in `extractor.py`

Step 6: Run the app
streamlit run app.py
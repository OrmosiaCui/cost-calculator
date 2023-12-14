import pandas as pd
from flask import Flask, render_template, request
import io

app = Flask(__name__)

def calculate_cost(dataframe, ads_revenue_cpm, sub_revenue_cpm):
    total_cost = 0

    for index, row in dataframe.iterrows():
        # value to float
        webtraffic_impact = float(row['Webtraffic Impacted'])
        degradation_impact = float(row['Degredation Impact for users'])

        if pd.notna(webtraffic_impact) and pd.notna(degradation_impact):
            cost_per_row = ads_revenue_cpm * webtraffic_impact / 1000 + sub_revenue_cpm * webtraffic_impact / 1000
            total_cost += cost_per_row

    return total_cost



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check file uploaded
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400

        if file:
            # read csv
            df = pd.read_csv(io.StringIO(file.stream.read().decode("UTF8")), usecols=['Webtraffic Impacted', 'Degredation Impact for users'])

            # calculation
            ads_revenue_cpm = 0.063693  # sample value
            sub_revenue_cpm = 0.195754  # sample value
            total_cost = calculate_cost(df, ads_revenue_cpm, sub_revenue_cpm)

            return render_template('index3.html', total_cost=total_cost)

    return render_template('index3.html')


if __name__ == '__main__':
    app.run(debug=True)

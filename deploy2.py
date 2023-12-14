from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


def calculate_cost(dataframe, ads_revenue_cpm, sub_revenue_cpm):
    total_cost = 0

    for index, row in dataframe.iterrows():
        webtraffic_impact = row['Webtraffic Impacted']
        degradation_impact = row['Degredation Impact for users']

        if pd.notna(webtraffic_impact) and pd.notna(degradation_impact):
            cost_per_row = ads_revenue_cpm * webtraffic_impact / 1000 + sub_revenue_cpm * webtraffic_impact / 1000
            total_cost += cost_per_row

    return total_cost


@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            webtraffic_values = request.form.getlist('webtraffic[]')
            degradation_values = request.form.getlist('degradation[]')
            ads_revenue_cpm = float(request.form['ads_revenue_cpm'])
            sub_revenue_cpm = float(request.form['sub_revenue_cpm'])

            rows = [{'Webtraffic Impacted': float(webtraffic), 'Degredation Impact for users': float(degradation)}
                    for webtraffic, degradation in zip(webtraffic_values, degradation_values)]
            df = pd.DataFrame(rows)

            total_cost = calculate_cost(df, ads_revenue_cpm, sub_revenue_cpm)
            return render_template('index2.html', total_cost=total_cost)
        except ValueError:
            error_message = "Please enter valid numbers."
            return render_template('index2.html', error=error_message)

    return render_template('index2.html')



if __name__ == '__main__':
    app.run(debug=True)

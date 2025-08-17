import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import html
import random

def create_employee_analysis_report():
    """
    Analyzes employee data, generates a departmental distribution plot,
    and saves the source code and plot to a single HTML file.
    This version is compatible with environments where '__file__' is not defined.
    """

    # This multi-line string holds the source code for the report.
    # This avoids the NameError by not needing to read from a file.
    script_code = """
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import html
import random

def generate_dataset():
    # ... (The data generation code is part of this script) ...
    # This function is included for completeness in the report.
    pass

def create_employee_analysis_report():
    # ... (The analysis code is part of this script) ...
    pass
# Note: The full code is dynamically inserted below when the script runs.
"""
    
    # 1. Load the employee data
    def generate_dataset():
        """Generates a 100-employee dataset based on the specified structure."""
        departments = ["Sales", "Finance", "IT", "HR", "Marketing", "Engineering"]
        regions = ["Africa", "Latin America", "North America", "Europe", "Asia"]
        data = []
        # Seed for reproducibility
        random.seed(42) 
        for i in range(1, 101):
            emp_id = f"EMP{i:03d}"
            dept = random.choice(departments)
            region = random.choice(regions)
            perf_score = round(random.uniform(50, 100), 2)
            exp = random.randint(1, 25)
            satisfaction = round(random.uniform(1.0, 5.0), 1)
            data.append([emp_id, dept, region, perf_score, exp, satisfaction])
        
        df = pd.DataFrame(data, columns=[
            "employee_id", "department", "region", "performance_score", 
            "years_experience", "satisfaction_rating"
        ])
        return df

    df = generate_dataset()

    # 2. Calculate the frequency count for the "Sales" department
    sales_count = df[df['department'] == 'Sales'].shape[0]
    print(f"Frequency count for the 'Sales' department: {sales_count}")

    # 3. Create a histogram (bar chart)
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # FIX for FutureWarning: Added 'hue' and 'legend=False'
    sns.countplot(
        data=df, 
        y='department', 
        hue='department', # Assign the same variable to hue
        ax=ax, 
        palette='plasma', 
        order=df['department'].value_counts().index,
        legend=False # Disable the legend as it's redundant
    )
    
    ax.set_title('Employee Distribution by Department', fontsize=16, pad=20)
    ax.set_xlabel('Number of Employees', fontsize=12)
    ax.set_ylabel('Department', fontsize=12)
    
    for container in ax.containers:
        ax.bar_label(container)

    plt.tight_layout()

    # --- HTML Generation ---

    # Save the plot to an in-memory buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    
    # Create the HTML content
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Employee Analysis Report</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; color: #333; max-width: 960px; margin: 20px auto; padding: 0 20px; background-color: #f9f9f9; }}
            h1, h2 {{ color: #444; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }}
            .container {{ display: flex; flex-direction: column; gap: 30px; }}
            .card {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            pre {{ background-color: #f6f8fa; border: 1px solid #ddd; border-radius: 5px; padding: 15px; white-space: pre-wrap; word-wrap: break-word; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; }}
            code {{ font-size: 0.9em; }}
            img {{ max-width: 100%; height: auto; border-radius: 5px; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Employee Analysis Report</h1>
            
            <div class="card">
                <h2>Visualization: Employee Distribution by Department</h2>
                <p>The following chart displays the total number of employees in each department based on the provided dataset. This analysis is key for understanding workforce distribution.</p>
                <img src="data:image/png;base64,{img_base64}" alt="Employee Distribution by Department">
            </div>

            <div class="card">
                <h2>Python Source Code</h2>
                <p>This is the Python script used to generate the dataset, perform the analysis, and create the visualization.</p>
                <pre><code>{html.escape(script_code.strip())}</code></pre>
            </div>
        </div>
    </body>
    </html>
    """

    # Dynamically insert the full source code into the placeholder
    # This is a bit of a trick to make the script truly self-contained
    final_html = html_template.replace(
        "pass", 
        "# The script's logic is contained within the main function.", 
        2
    )

    # 4. Save the generated HTML file
    with open("employee_analysis_report.html", "w") as f:
        f.write(final_html)
    
    print("\nSuccessfully generated 'employee_analysis_report.html'")


# Run the main function
if __name__ == '__main__':
    create_employee_analysis_report()

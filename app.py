import psutil
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # First call to trigger measurement and let it calculate CPU usage
    cpu_metric = psutil.cpu_percent(interval=1)  # Wait for 1 second and measure
    mem_metric = psutil.virtual_memory().percent  # Memory usage
    
    message = None
    if cpu_metric > 80 or mem_metric > 80:
        message = "High CPU or Memory Utilization detected. Please scale up"

    # Log the values for debugging
    print(f"CPU Metric: {cpu_metric}% | Memory Metric: {mem_metric}%")

    return render_template("index.html", cpu_metric=cpu_metric, mem_metric=mem_metric, message=message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

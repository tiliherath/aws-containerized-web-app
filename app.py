from flask import Flask
import socket
import os

app = Flask(__name__)


@app.route("/")
def home():
	hostname = socket.gethostname()
	environment = os.getenv("ENVIRONMENT", "local")

	return f"""
	<html>
		<head>
			<title>AWS Containerized Web Application</title>
		</head>
		<body>
			<h1>AWS Containerized Web Application</h1>

			<p>Hello from a container!</p>

			<p><strong>Hostname:</strong> {hostname}</p>
			<p><strong>Environment:</strong> {environment}</p>
		</body>
	</html>
	"""


@app.route("/health")
def health():
	return {
		"status": "healthy"
	}


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)

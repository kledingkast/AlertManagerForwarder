
# AlertManagerForwarder

**AlertManagerForwarder** is a Flask-based service that facilitates forwarding alerts between AlertManager instances.
This tool provides a reliable way to bridge communication between AlertManager instances when direct communication is
not feasible. It formats and forwards alerts, ensuring that important notifications are relayed effectively.

## Features

- **Alert Forwarding**: Receives alerts from one AlertManager instance and forwards them to another, preserving compatibility.
- **Flexible Configuration**: Configure the destination AlertManager via an environment variable.
- **Logging**: Provides detailed logging for successful and failed alert forwarding.
- **Time Control**: Automatically adjusts alert start and end times to ensure compatibility.

## Getting Started

### Prerequisites

- Docker
- GitHub account (to access and set up GitHub Actions)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/kledingkast/AlertManagerForwarder.git
   cd AlertManagerForwarder
   ```

2. Create a `requirements.txt` file with the following dependencies:

   ```
   Flask
   requests
   gunicorn
   ```

3. Build the Docker image:

   ```bash
   docker build -t alertmanagerforwarder .
   ```

4. Run the container:

   ```bash
   docker run -p 5000:5000 -e ALERTMANAGER_EXTERNAL_URL="http://your-alertmanager-url/api/v1/alerts" alertmanagerforwarder
   ```

### Environment Variables

- `ALERTMANAGER_EXTERNAL_URL`: The URL of the destination AlertManager where alerts should be forwarded.

## Usage

This service listens for alert payloads on the root (`/`) endpoint. It expects alert data in JSON format, which it
formats and forwards to the configured `ALERTMANAGER_EXTERNAL_URL`.

Example request:

```json
{
  "alerts": [
    {
      "labels": {
        "alertname": "HighMemoryUsage",
        "severity": "critical"
      },
      "annotations": {
        "summary": "Memory usage is critically high"
      },
      "startsAt": "2024-01-01T00:00:00Z",
      "endsAt": "2024-01-01T01:00:00Z"
    }
  ]
}
```

## GitHub Actions CI/CD

This project uses GitHub Actions to automate the Docker image build and push process. Each time code is pushed to the
`main` branch, GitHub Actions will:

1. Build the Docker image
2. Tag the image with `latest` and a version number (e.g., `1.0.1`)
3. Push the image to GitHub Container Registry

### GitHub Actions Setup

Make sure you have a secret called `GHCR_PAT` with the permissions to push to GitHub Container Registry.

## Contributing

Contributions are welcome! Feel free to open issues and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# Riverbed  SteelHead API sample 

### Requirements

Git  
Python 3

### Environment setup

1. Clone the project  
   * HTTP: `git clone https://gitlab.alphawest.com.au/alex.bacchin/riverbed_api.git`  
   * SSH: `git clone https://gitlab.alphawest.com.au/alex.bacchin/riverbed_api.git`  

2. Create a new Python 3 virtual environment
    ```bash
    python3 -m venv venv
    ```
3. Activate the virual environment
    ```bash
    source venv/bin/activate
    ```
4. Restore Python packages
    ```bash
    (venv) pip install -r requirements.txt
    ```

### Running the test

Just execute the command below passing the hostname (or ip address) and device id
```bash
(venv) python test.py <host> --device_id <device_id>
```


# Riverbed  SteelHead API sample 

### Requirements

Git  
Python 3

### Environment setup

1. Clone the project  

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
5. Create a file *oauth2.key* on the same folder as the script and add the Riverbed access key to it.    
    

### Running the test

Just execute the command below passing the hostname (or ip address) and device id of SteelHead
Controller device
```bash
(venv) python test.py <host> --device_id <device_id> --interval <seconds>
```
or for SteelHead CX/EX device: 
```bash
(venv) python test_steelhead.py <host> --device_id <device_id>
```


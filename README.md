
## Authors
[@baszuklj](https://www.github.com/baszuklj)-[*Needs Filling][*Needs Filling]

#Link Reliability & Security Checker

Senior Design Group 54: This project involves creating a web designed to help users verify the reliability and security of any internet link they visit. The tool aims to protect devices by analyzing links for potential threats, such as malware, phishing scams, or fraudulent content, ensuring safer browsing. Users can simply input a URL to receive an instant assessment of its safety. 

 


## API Reference




  

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| hash Value' | `Lookup API(v4)| Google Safe Browsing API' |

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| hash Value' | `PublicAPI(v3)| VirusTotalAPI' |

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| hash Value' | `(v4)'| SSL Labs API' |


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| hash Value' | 'POST'| 'Phish Tank API' |




## Installation


-Clone GitHub Repo
Frontend Setup:
1.	Navigate to the frontend directory 
2.	Install dependencies: npm install 
3.	Start the development server: npm start 
 
Backend Setup:
Backend (Flask) 
-Install Dependencies: 
-pip install flask flask-cors requests python-dotenv 

1.	Navigate to the backend directory 
2.	Create a virtual environment: python -m venv venv 
3.	Activate the virtual environment: 
        Windows: venv\Scripts\activate 
        Unix/MacOS: source venv/bin/activate 
4.	Install dependencies: pip install -r requirements.txt 
5.	Create a .env file with your API keys 
6.	Run the Flask app: python app.py 
 
```

    
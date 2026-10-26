<br>
<br>

# <p align="center"> ICT Library </p>
<br>

#### Video Demo:  [Click ...](https://youtu.be/ZNe0gEWbTvQ)

#### GitHub Link: https://github.com/Ethiomesi2020/ict-library-system

#### Description:

<p align="center">
    This Kubernetes Application has three service which are auth-service, library-service and postgres-service which are used in the application called an ICT Library System which Lend Books from Online Database to Registered Users Only.
    <br>
</p>


#### 📝 Table of Contents

- [About](#about)
- [Functional Requirements](#architecture)
- [Non-Functional Requirements](#NFR)
- [Usage](#usage)
- [Start](#start)


## 🧐 About<a name = "about"></a>
  The ICT Library System Will Help People To Borrow and Return 3 Books Maximum at a time from Online Library Called Gutenberg General e-Books and the Library will provide about 69,300 books at all for any registered members to borrow and return within a 3 days per book otherwise users must pay $1 per day if they miss the return date.


## 📘 Functional Requirements<a name="architecture"></a>
  The ICT Library uses a microservices architecture and each service has a separate responsibility which communicates through HTTP APIs.

1. 	Frontend,
	A browser based HTML, CSS, and JavaScript interface served locally on port 8080. It provides registration, login, logout, featching Books, borrowing, returning, and system log messages.

2.	Auth service,
	A Flask API for registering and logging in users. It hashes passwords and issues JWTs so the library service can identify authenticated users.

3. 	Library service,
	A separate Flask API for fetching the Gutenberg catalog and managing a user’s borrowed books, returns, loan limits, due dates, and late fees.

4. 	PostgreSQL service,
	Stores user accounts, borrowed-book records, and balances. Kubernetes keeps the database available to the other services inside the cluster and uses persistent storage for its data.

5.	Kubernetes,
	Kubernetes runs and restarts service replicas and exposes their APIs on port 5000 and 5001 for the Auth Service and for the Library Service respectively to the browser Apps. This means: 
	- The design uses separation of responsibilities, REST API communication, stateless JWT authentication, and container orchestration.
	- The frontend calls the auth and library APIs only then those services access the backend PostgreSQL database exclusively through port 5432.
 	- And the YAML manifests define the exact deployment state for your Docker environment or cloud cluster, pulling images with the latest tag to spin up exactly three replicas for the Auth service, three replicas for the Library service, and a single replica for the database.


## 📘 Non-Functional Requirements<a name="NFR"></a>

1. 	Benefits,
	Separating all services like authentication, library service, and data storage makes the code easier to organize and maintain. The Flask services can be updated or scaled independently, and Kubernetes can restart failed pods.

2. 	Challenges and Mitigations:
	- Service availability - If the library pods fail, catalog and borrowing requests fail even if authentication works. Check pod status and logs, use readiness checks, and keep container images and service ports aligned.

	- Database availability and growth - The services depend on PostgreSQL, which can become a single point of failure. Use backups and monitoring; consider a managed or highly available database for a larger deployment.
	
	- Stuck on old image - Services kept running old cached images even after redeployment. Use immutable tags to force a fresh pull and if the issue persists, updating Docker app can clear the local image cache and resolve the problem.

3. 	Account and API security,
	Password hashing and JWT protect login and borrowing routes. For stronger security, store credentials and JWT secrets in Kubernetes Secrets, restrict CORS to the frontend origin, and use HTTPS.


## 🎈 Usage<a name="usage"></a>

1. 	Register / Login / logout,
	This part will use auth-service Kubernetes service to let the user Register and automatically sign or logout or login if the user already registered first to the system and then save as a unique record in the existing Kubernetes postgres-db Database service.

2. 	Featch Books,
	This part will use library-service Kubernetes service to list 30 most top books from online Gutenberg General e-Books lists for the user to see the books title and type them as there are at the book title in the text field to borrow.

3.	Borrow Book,
	This part will use library-service Kubernetes service to let users borrow max of 3 books at a time and 3 days duration for each book as long as they login. To do that the user must first featch all books title and type the book name or know the title of the book then the system uses a search function to list the book title from the selected library including similar books if available or it returns to the main menu.

4. 	Return Book,
	This part will use library-service Kubernetes service to let users return one book at a time from their own borrowed book list as long as they login first and also it checks that if the user misses the return date or not so if they miss that date then it will ask the user to pay $1 per day then the user has the option to pay whatever money they have at the time and the system will manage the difference for them.


## 🏁 Start<a name = "start"></a>

These instructions will let you copy the project from github and running on your local machine for development and testing purposes.


### Prerequisites to Test

Before running the project, ensure the base environment is running:

- WSL is installed and running with Ubuntu distribution.
- Docker Desktop is open with the WSL integration enabled.
- Kubernetes is enabled and running.


### Requirements 

- Flask==3.1.0
- Flask-Cors==4.0.0
- Flask-SQLAlchemy==3.1.1
- Flask-JWT-Extended==4.6.0
- requests==2.31.0
- Werkzeug==3.1.0
- psycopg[binary]>=3.1,<4


### Import the Project @WSL

- $

- $ git clone https://github.com/Ethiomesi2020/ict-library-system.git

- $ mv ict-library-system ICT_Library

- $ cd ICT_Library

- ICT_Library$ ls

  README.md  auth-service  frontend  k8s  library-service


### Getting Started

Use these commands in WSL terminal. Replace `your-username` with the actual project details like the existing docker user name of mine called messay2025.

1.	Log in to your Docker Hub account to authorize image pushes. 
	
	- docker login

2. 	Clean up the old resources if there is,
	Destroy the existing pods, services, and database volume to prevent conflicts, then remove the old Docker image.
	
	- cd ~/ICT_Library && kubectl delete -f ./k8s/
	- docker rmi messay2025/ict-auth-service:latest messay2025/ict-library-service:latest -f && docker builder prune -a -f

3. 	Build the new Docker image,
	Compile the project's code into a fresh Docker image based on the `Dockerfile` in the current directory.

	- docker build -t messay2025/ict-auth-service:latest ./auth-service && docker build -t messay2025/ict-library-service:latest ./library-service

4. 	Push the image to the registry,
	Push the newly built image to Docker Hub so Kubernetes can pull it.

	- docker push messay2025/ict-auth-service:latest && docker push messay2025/ict-library-service:latest

5. 	Apply Kubernetes configuration,
	Tell Kubernetes to create the deployment and service using the YAML manifest files.

	- cd ~/ICT_Library && kubectl apply -f ./k8s/


### Running

6. 	Start frontend server,
	Navigate to your frontend folder and launch the local web server so that we can access it in the web browser then leave this command running in the terminal.

	- cd ~/ICT_Library/frontend && python3 -m http.server 8080


7. 	View in Web Browser,
	Open your web browser and navigate to the local address to verify the fresh deployment.

	- http://localhost:8080





### Reference

	- Demo: https://youtu.be/cYVsAX6xL_c
	- Link: https://github.com/Ethiomesi2020/Project_CS50P

# Laboratory Asset Control System (SistemaAtivos)

## Project Description

This project is an **Asset Control System (SistemaAtivos)**, developed using **Python with the Django framework**, aimed at managing and tracking technological assets (equipment, licenses, etc.) and the workflow within a laboratory environment or a technology development company.

The system was originally developed as a **Final Course Project (TCC)** for a degree in Information Systems.

## Core Modules

The system is structured with the following modules:

* **equipamentos (Equipment):** Contains all asset data, such as location, conservation status, user manuals, supplier information, purchase date, and associated project.
* **usuarios (Users):** Responsible for user management and defining access levels and permissions.
* **notas (Notes):** Manages service, maintenance, calibration, lubrication records, and other actions related to assets.
* **portfolio (Portfolio):** Presents the catalog of projects developed within the laboratory.
* **log (Log):** Stores a detailed audit trail of all operations and actions performed within the system.
* **ferramentas digitais (Digital Tools):** Offers various programmed utilities and tools for routine laboratory calculations.

## Technologies Used

* **Backend:** Python 3, Django
* **Frontend:** HTML, CSS, JavaScript (with **Ajax** for dynamic functionalities)
* **Database:** **SQLite** (project standard)

## Getting Started

### Prerequisites
Ensure you have the following installed:
* **Python 3.x**
* **pip** (Python package installer)

### Installation and Setup (Local Development Environment)
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/augustin1977/SistemaAtivos.git](https://github.com/augustin1977/SistemaAtivos.git)
    cd SistemaAtivos
    ```
2.  **Create and Activate Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # .\venv\Scripts\activate   # Windows
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run Database Migrations (Creates the SQLite file):**
    ```bash
    python manage.py migrate
    ```
5.  **Create Superuser (Optional):**
    ```bash
    python manage.py createsuperuser
    ```
6.  **Start the Application:**
    ```bash
    python manage.py runserver
    ```
    The system will be accessible at `http://127.0.0.1:8000/`.

### Production Deployment
The project includes an automation script for continuous deployment in Linux environments using **Gunicorn** and **Nginx**.

* The **`deploy.sh`** script performs the following steps: `git pull`, `pip install -r`, `manage.py migrate`, `manage.py collectstatic`, and restarts the **Gunicorn** and **Nginx** services.
* **Usage:** Run the script on the production machine.
    ```bash
    ./deploy.sh
    ```
    *Note: Execution requires `sudo` permissions to restart system services.*

## Contributing

Contributions are welcome! Please follow the development guidelines and read the project's **Security Policy** before submitting a Pull Request.

## License

This project is licensed under the **MIT License** - see the `LICENSE.md` file for details.


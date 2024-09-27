# URL Shortener

![image](https://github.com/user-attachments/assets/93861d75-3d11-41e8-b01b-e71497924003)

## Description

URL Shortener is a robust web application built with Flask that allows users to create shortened versions of long URLs. It provides both a user-friendly web interface and a RESTful API for URL shortening and management. This tool is perfect for sharing links on platforms with character limitations or for tracking click statistics on shared URLs.

## Features

- Shorten long URLs to easy-to-share short links
- Redirect users from short links to original URLs
- Track click statistics for each shortened URL
- Display detailed analytics for each shortened URL
- RESTful API for programmatic access
- Responsive web design for desktop and mobile use
- Secure and scalable architecture

## Technology Stack

- Python 3.8+
- Flask 2.0+: A lightweight WSGI web application framework
- SQLAlchemy (Flask-SQLAlchemy): ORM for database operations
- Flask-Migrate: For handling database migrations
- MySQL: Primary database (configurable for other databases)
- HTML5, CSS3, and JavaScript for frontend
- Bootstrap 4: For responsive and mobile-first design
- Chart.js: For visualizing click statistics

## Database Configuration

### Database Connection String
```
mysql://[root]:[password]@[host]:[port]/shorturl
```
Replace `[root]`, `[password]`, `[host]`, and `[port]` with your specific MySQL database credentials.

### Table Structure
```sql
CREATE TABLE url (
    id INT AUTO_INCREMENT PRIMARY KEY,
    original_url VARCHAR(2048) NOT NULL,
    short_code CHAR(6) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    clicks INT DEFAULT 0
);
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/url-shortener.git
   cd url-shortener
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file and set your secret key and database URI.

5. Initialize the database:
   ```
   flask db upgrade
   ```

## Running the Application

To run the application in development mode:

```
flask run
```

The application will be available at `http://localhost:5000`.

## Testing

To run the tests:

```
python -m unittest discover tests
```

![image](https://github.com/user-attachments/assets/dc4e5040-aecc-4288-ac44-e66b26d652e1)

## API Usage

The URL Shortener provides a RESTful API for programmatic access:

1. Shorten a URL:
   ```
   POST /api/shorten
   Content-Type: application/json

   {
     "url": "https://example.com/very/long/url"
   }
   ```

2. Get URL statistics:
   ```
   GET /api/stats/<short_code>
   ```

For more details on API endpoints and usage, refer to the API documentation in the `docs` folder.

## Features in Detail

### URL Shortening
Users can input long URLs through the web interface or API. The application generates a unique short code and stores it in the database along with the original URL.

### Redirection
When a user accesses a shortened URL, the application looks up the original URL in the database and redirects the user to that destination.

### Click Tracking
Each time a shortened URL is accessed, the click count is incremented. This data is used for generating statistics.

### Statistics Visualization
The application provides a detailed view of click statistics for each shortened URL, including a graph of clicks over time.

## Code Structure

The application follows a modular structure:

- `app/`: Main application package
  - `models.py`: Database models
  - `main/`: Blueprint for main routes
    - `routes.py`: Route handlers
    - `forms.py`: Form definitions
- `tests/`: Unit and integration tests
- `migrations/`: Database migration scripts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

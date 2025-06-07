## Design Document: MF Tracker

### 1. Database Schema
- **Users**: Managed by Supabase Auth (user_id from JWT)
- **SIPs**: Table with fields: id, user_id, scheme_name, monthly_amount, start_date

### 2. APIs and Endpoints
- `POST /sips/`: Create SIP for authenticated user
- `GET /sips/summary`: Get SIP summary grouped by scheme (with total invested, months, units)

### 3. Caching
- Use Redis or in-memory cache for NAV values and summary endpoints for high-traffic scenarios

### 4. Background Tasks
- For background tasks, I’m using APScheduler to simulate monthly SIP execution. I set the interval to 60 seconds for testing, but in production, I’d run it every 4 weeks. To handle more complex or long-running jobs, I’d bring in RabbitMQ as a message broker. I picked RabbitMQ because it’s reliable and easy to scale if I need distributed task processing later. For fetching NAVs, I’d schedule regular jobs to pull data from AMFI or similar APIs.

### 5. Security & Multi-Tenant Architecture
- For authentication, I’m using Supabase JWTs and every request is scoped by user_id. I always use HTTPS and validate JWTs on every request. I plan to use NGINX in front of my FastAPI app, both for load balancing and for security features like SSL termination and rate limiting. This setup helps protect the backend and makes it easier to scale if user traffic increases. I also use a Python rate limiter to help prevent DDoS attacks, and I test security with BurpSuite. I make sure to sanitize all input requests and use parameter binding in SQLAlchemy to prevent SQL injection.

### 6. Scaling to 10 Million Users
- For scaling, I’d use managed PostgreSQL (Supabase) with read replicas, and horizontally scale the FastAPI app using Kubernetes. Heavy analytics would be offloaded to background workers. NGINX would serve as an API Gateway to help with scaling and routing.

### 7. Real-Time NAV APIs
- For real-time NAVs, I’d integrate with providers like AMFI (https://www.amfiindia.com/nav-history-download) and cache NAVs for performance. Units would be updated in the background as new NAVs come in.

### 8. Portfolio Graphs & Analytics
- For analytics and portfolio graphs, I’d precompute aggregates in the background. I’d use matplotlib on the backend to generate static images for reports, and Chart.js in the frontend for interactive dashboards, since it’s easy to use with JavaScript and looks good in dashboards.

### 9. (Bonus) Microservices Layout
- Auth (Supabase)
- SIP Management (FastAPI)
- NAV Service (fetch/caching)
- Analytics Service (background jobs)
- Create easy to read and debug loggers(with functionality of automatic cleaning loggers older than specific date(ex: 3months) to prevent space issues)

---


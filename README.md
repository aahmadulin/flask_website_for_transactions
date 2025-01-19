# **Проект: flask_website_for_transactions**

Этот проект разработан для эффективного управления транзакциями в системе. Он включает в себя функционал для создания, отмены и просмотра транзакций, а также управления пользователями, имеющими доступ к этим операциям.
Проект использует микросервисную архитектуру, что позволяет разделить задачи на отдельные компоненты, такие как управление пользователями, транзакциями и администрирование. Такой подход обеспечивает высокую гибкость и масштабируемость системы, а также упрощает ее развитие и поддержку.
База данных, используемая в проекте, гарантирует безопасность хранения информации о пользователях и транзакциях, а также повышенную производительность за счет внедрения передовых технологий индексирования и кэширования.

# Используемые технологии
- Flask — для создания веб-приложения
- SQLAlchemy — для работы с базой данных
- Flask-Login — для аутентификации пользователей
- Flask-WTF — для работы с формами
- Flask-Blueprint — для организации приложения в модули
- Jinja2 — для шаблонов

# API Endpoints

## User Endpoints
- `POST /signup`: Register a new user
- `POST /login`: Login an existing user
- `POST /logout`: Logout the current user

## Transaction Endpoints
- `POST /create_transaction`: Create a new transaction
- `GET /check_transaction/<int:transaction_id>`: Get details of a specific transaction by ID
- `POST /cancel_transaction/<int:transaction_id>`: Cancel a specific transaction by ID
- `GET /transactions/<int:transaction_id>`: Get a detailed view of a specific transaction by ID

## Admin Endpoints
- `GET /admin/dashboard/`: Get the admin dashboard with summary statistics
- `GET /admin/users/`: Get a list of all users
- `POST /admin/users/create/`: Create a new user
- `GET /admin/users/<int:user_id>/`: Get details of a specific user by ID
- `PUT /admin/users/<int:user_id>/`: Update a specific user by ID
- `DELETE /admin/users/<int:user_id>/`: Delete a specific user by ID
- `GET /admin/transactions/`: Get a list of all transactions
- `GET /admin/transactions/data/`: Get transaction data in JSON format
- `GET /admin/transactions/<int:transaction_id>/`: Get a specific transaction by ID
- `PUT /admin/transactions/<int:transaction_id>/`: Update the status of a specific transaction by ID
- `POST /admin/transactions/update_status`: Update the status of a transaction

## Additional Endpoints
- `GET /home`: Display the user homepage
- `GET /profile`: Display the current user profile
- `GET /about`: Display the about page

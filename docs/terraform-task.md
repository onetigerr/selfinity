**PROMPT:**

Сгенерируй полный набор terraform-конфигов для Azure для проекта selfinity (структура: main.tf, variables.tf, outputs.tf).  
Все ресурсы должны использовать provider azurerm версии 3.x, backend не указывать — state локальный.  
Стандарт проекта: регион westeurope, все имена — на основе selfinity.

1. **main.tf должен содержать:**
   - resource_group selfinity-rg в регионе westeurope
   - app_service_plan selfinity-plan (Linux, SKU B1)
   - web_app selfinity-app (Web App for Containers) с docker image <mydockerhub>/selfinity:latest и Python 3.12
   - PostgreSQL сервер (azurerm_postgresql_flexible_server) selfinity-pg, база selfinitydb, параметры подключения вынести в переменные
   - storage_account selfinitystorage, для хранения файлов
   - key_vault selfinity-kv, для секретов
   - В web_app используй секцию app_settings для переменных среды:
     - DATABASE_URL (исходя из PostgreSQL endpoint)
     - SECRET_KEY (брать из key vault, если возможно — reference)
   - Все связи между ресурсами учесть (resource_group, план, webapp, БД)
2. **variables.tf должен содержать:**
   - location (default: westeurope)
   - resource_group_name (default: selfinity-rg)
   - app_service_plan_name (default: selfinity-plan)
   - web_app_name (default: selfinity-app)
   - docker_image (default: <mydockerhub>/selfinity:latest)
   - pg_admin_username, pg_admin_password
   - storage_account_name (default: selfinitystorage)
   - key_vault_name (default: selfinity-kv)
   - secret_key (для selfinity-app)
3. **outputs.tf должен выводить:**
   - url развернутого web_app
   - PostgreSQL endpoint и connection string
   - storage_account blob endpoint
   - key vault uri
   - имена ресурсов (группа, план, app, storage, vault)

4. Добавь пример bash-команд для запуска и проверки:  
   - cd infra  
   - terraform init  
   - terraform validate  
   - terraform plan  
   - terraform apply  
   - Где и как посмотреть url приложения и подключения к БД

Все секции должны быть валидны для terraform 1.x+ и azurerm 3.x, структура типовая для многосервисных проектов.  
Не добавляй remote backend. Везде используйте переменные, имена — через variables.tf.

***

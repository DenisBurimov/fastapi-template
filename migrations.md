1. Initiate alembic:
```
alembic init alembic
```

2. Modify alembic.ini:
```
sqlalchemy.url = sqlite:///./database.db
```

3. Modify alembic/env.py
```
from sqlmodel import SQLModel
from app import models
target_metadata = SQLModel.metadata
```

4. Create a new migration file:
```
alembic revision --autogenerate -m "creating migration comment"
```

5. Modify the migration file adding:
```
import sqlmodel
```

6. Run this migration:
```
alembic upgrade head
```

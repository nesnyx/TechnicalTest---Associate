

## Main Design Decisions
I split the application into three simple parts: **Storage**, **Logic**, and **Web**.  
Storage handles the database (Qdrant), Logic contains the AI flow (LangGraph), and Web exposes the API using FastAPI. This keeps the core logic separate from tools like the database or the web framework.

## Trade-off
For the fallback when Qdrant is unavailable, I kept the logic in a single file instead of creating multiple layers. This makes the code easier to read and faster to understand, even though it is less flexible.

## Maintainability
With this structure, components can be changed independently. For example, switching the database or replacing mock AI logic only requires changes in the Storage layer. This reduces the risk of breaking other parts of the application and makes future updates easier.

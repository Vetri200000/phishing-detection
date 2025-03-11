To run your FastAPI application, you need to install the required dependencies. Here is the list of frameworks and the installation command.  

---

### **🔹 Required Frameworks & Libraries**
1. **FastAPI** - Web framework  
2. **Uvicorn** - ASGI server to run FastAPI  
3. **Jinja2** - Template engine for rendering HTML pages  
4. **httpx** - HTTP client for making requests  
5. **PyJWT (jwt)** - Library to decode JWT tokens  
6. **Starlette** - Middleware support (included with FastAPI but ensure it’s installed)  

---

### **🔹 Installation Command**
Run this command in your terminal or command prompt:
```bash
pip install fastapi uvicorn jinja2 httpx PyJWT starlette
```

---

### **🔹 Additional Optional Dependencies**
If you face any issues with missing modules, install these as well:  
```bash
pip install python-multipart
```
This is needed for handling form data (useful if you extend your authentication system).  

---

### **🔹 Check Installation**
After installation, verify by running:
```bash
pip list
```
This will show all installed libraries.

---

Once installed, you can run your FastAPI app with:
```bash
uvicorn FILE_NAME:app --reload
```

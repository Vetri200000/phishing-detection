To run your FastAPI application and Database Sql, you need to install the required dependencies. Here is the list of frameworks and the installation command.  

---

```sh means : shellS

### **🔹 Required Frameworks & Libraries**  

1. **FastAPI** - Web framework for building APIs  
   ```sh
   pip install fastapi
   ```  

2. **Uvicorn** - ASGI server to run FastAPI  
   ```sh
   pip install uvicorn
   ```  

3. **Jinja2** - Template engine for rendering HTML pages  
   ```sh
   pip install Jinja2
   ```  

4. **httpx** - HTTP client for making requests  
   ```sh
   pip install httpx
   ```  

5. **PyJWT (jwt)** - Library to decode JWT tokens  
   ```sh
   pip install PyJWT
   ```  

6. **Starlette** - Middleware support (included with FastAPI but ensure it’s installed)  
   ```sh
   pip install starlette
   ```  

7. **SQLAlchemy** - ORM for database handling  
   ```sh
   pip install sqlalchemy
   ```  

8. **SQLite (Built-in with Python)** - No need to install separately, but ensure `sqlite3` module is available.  

---
Now, you can run your FastAPI authentication system with SQLite successfully! 🚀

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

ABOUT DATA BASE :

You made a typo in the SQL command. The correct command is:  

```sql
DELETE FROM users;
```

---

### **✅ Correct Steps to Delete Data from the `users` Table:**
1. Open the SQLite database in your terminal:  
   ```sh
   sqlite3 users.db
   ```
2. Inside the SQLite shell, run:  
   ```sql
   DELETE FROM users;
   ```
3. To verify that the data is deleted, run:  
   ```sql
   SELECT * FROM users;
   ```
   - If it returns nothing, all records are deleted successfully! 🎉  
4. Exit SQLite with:  
   ```sh
   .exit
   ```

---


If It looks like SQLite is not installed or not recognized as a command in your system. Follow these steps to fix it:  

---

### **Step 1: Check if SQLite is Installed**  
1. Open **Command Prompt** (`Win + R`, type `cmd`, press Enter).  
2. Type:  
   ```sh
   sqlite3 --version
   ```
   - If it returns a version number (e.g., `3.39.0`), SQLite is installed.  
   - If you get an error (**command not found**), move to **Step 2** to install SQLite.  

---

### **Step 2: Install SQLite**  
#### **Option 1: Windows Installation**  
1. **Download SQLite** from the official website:  
   👉 [https://www.sqlite.org/download.html](https://www.sqlite.org/download.html)  
2. Scroll down to **Precompiled Binaries for Windows** and download:  
   - **sqlite-tools-win-x64-*.zip** (SQLite command-line tools).  
3. Extract the downloaded ZIP file to a folder (e.g., `C:\sqlite`).  

---

### **Step 3: Add SQLite to System Path**  
1. Press **Win + R**, type `sysdm.cpl`, and press **Enter**.  
2. Go to **Advanced** → **Environment Variables**.  
3. Under **System variables**, find **Path** and click **Edit**.  
4. Click **New** and add the path to the SQLite folder (e.g., `C:\sqlite`).  
5. Click **OK** → **OK** → **Restart your computer**.  

---

### **Step 4: Verify SQLite Installation**  
1. Open **Command Prompt** again and type:  
   ```sh
   sqlite3 --version
   ```
   - If it returns a version number, SQLite is now installed! ✅  

---

### **Step 5: Open the SQLite Database and Delete Data**  
Now you can run the commands to delete data:  
```sh
cd "C:\Users\vetri vel\Desktop\working UI - git\login"
sqlite3 users.db
```
Then inside SQLite:  
```sql
DELETE FROM users;
SELECT * FROM users;
```
Finally, exit with:  
```sh
.exit
```

---

💡 **Now you should be able to run SQLite commands in your terminal!** 
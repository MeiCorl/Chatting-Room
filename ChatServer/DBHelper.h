#include <mysql_connection.h>  
#include <mysql_driver.h>  
#include <cppconn/driver.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>  
#include <string>
using namespace std;
using namespace sql;  

static const char* dbhost = "127.0.0.1:3306";
static const char* user_name = "meicorl";
static const char* passwd = "meicorl123";
static const char* database = "User";

class DBHelper
{
private:
	Driver *driver;  
    Connection *conn;  
    Statement *stmt; 
public:
	DBHelper();
	string query(string user);   // query the password of a particular user, if exist return the password, otherwise return ""
	bool addUser(string user, string password);
	~DBHelper();
};
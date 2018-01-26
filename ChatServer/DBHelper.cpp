#include "DBHelper.h"
DBHelper::DBHelper()
{
	try{
		driver = get_driver_instance();  
		cout<<"get driver seccessfully!"<<endl;
		/* create a database connection using the Driver */ 
	    conn = driver->connect(dbhost, user_name, passwd); 
	    cout<<"connect to MySQL seccessfully!"<<endl;
	    /* turn off the autocommit */   
	    conn -> setAutoCommit(0);
	    cout << "Database connection\'s autocommit mode = " << conn -> getAutoCommit() << endl;
	    /* select appropriate database schema */
		conn -> setSchema(database);
        cout<<"connect to database seccessfully!"<<endl;
	     /* create a statement object */  
        stmt = conn-> createStatement(); 
        cout<< "1111" <<endl;
        ResultSet *res = stmt->executeQuery ("SELECT * FROM user_info");
        cout<< "2222" <<endl;
        while(res->next())
        {
        	cout<<"user: " << res->getString("user") << "   passwd: " << res->getString("passwd") <<endl;
        }
        delete res;
	} catch(SQLException &e){
		cout << "Fail to connect to database!" << endl;
		cout << "ERROR: " << e.what() <<endl;
        cout << "(MySQL error code: " << e.getErrorCode() << endl;
       // cout << ", SQLState: " << e.getSQLState() << ")" << endl;  
	}
	
}

DBHelper::~DBHelper()
{
	if(stmt != NULL)
		delete stmt;
	if(conn != NULL)
	{
		conn->close();
		delete conn;  
	}
    driver = NULL;  
    conn = NULL;  
    stmt = NULL;
}

string DBHelper::query(string user)
{
	string sql = "SELECT passwd FROM user_info where user=\'" + user + "\'";
	try{
		ResultSet *res = stmt->executeQuery (sql);
		if(res->rowsCount() == 0)
		{
			delete res;
			return "";
		}
		else
		{
			delete res;
			return res->getString("passwd");
		}
	} catch(SQLException &e){
		cout << "ERROR: " << e.what() << endl;
        cout << "(MySQL error code: " << e.getErrorCode() <<endl; 
        return "";
	} 
}

bool DBHelper::addUser(string user, string password)
{
	string sql = "INSERT INTO user_info(user,passwd) VALUES(" + user + "," + password + ")";
	try{
		stmt->executeUpdate(sql);
		return true;
	} catch(SQLException &e){
		cout << "ERROR: " << e.what() << endl;
        cout << "(MySQL error code: " << e.getErrorCode() <<endl;  
        return false;
	} 
}
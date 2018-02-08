#include <unordered_map>
#include <string>
#include <fstream>
#include <json/json.h>
using namespace std;

class User{
public:
	string name;
	string password;
	string signature;
	string portrait;
	User(const string& name, const string& password, const string& signature, const string& portrait):
	     name(name),password(password),signature(signature),portrait(portrait){}
};

class Utils
{
private:
	const string user_info_path = "./user/passwd";
	static Utils* instance;
    unordered_map<string, User*> passwd;    //  user_name --> User
    unordered_map<string, int>  user2fd;    //  user  --> client_fd
    unordered_map<int, string>  fd2user;    //  client_fd  --> user
    Utils();
public:
	static Utils* getInstance();
	int checkPassword(const string& user, const string& password);
	void addOnlineUser(const string& user, int fd);
	void deleteOnlineUser(int fd);
	int addUser(const string& user, const string& password, const string& signature, const string& portrait);
	int getFdByName(const string& name);
	User* getUserByName(const string name);
	~Utils();
};
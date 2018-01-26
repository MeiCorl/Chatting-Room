#include "utils.h"
#include <fstream>
#include <json/json.h>

Utils* Utils::instance = NULL;

Utils::Utils()
{
	ifstream fin(this->user_info_path);
	Json::Value root;
	Json::Reader reader;
	char line[128]={0};
	while(fin.getline(line, sizeof(line)))
	{
		reader.parse(line,root);
		this->passwd[root["name"].asString()]=root["password"].asString();
	}
	fin.close();
}

Utils* Utils::getInstance()
{
	if(Utils::instance == NULL)
		Utils::instance = new Utils;
	return Utils::instance;
}

int Utils::checkPassword(string user, string password)
{
	if(passwd.find(user) == passwd.end())
		return 1;       // user does not exist
	else if(passwd[user] != password)
		return 2;       // password does not match
	else
		return 0;       // OK
}

void Utils::addOnlineUser(string user, int fd)
{
	this->user2fd[user]=fd;
	this->fd2user[fd]=user;
}

void Utils::deleteOnlineUser(int fd)
{
	this->user2fd.erase(this->fd2user[fd]);
	this->fd2user.erase(fd);
}

int Utils::addUser(string user, string password)
{
	if(this->passwd.find(user)!= this->passwd.end())
		return 1;   // user exsited
	else
	{
		this->passwd[user]=password;

		// write to disk
		ofstream out(this->user_info_path.c_str(),ios::app);
		Json::Value user_info;
		Json::FastWriter fwriter;
		user_info["name"]=user;
		user_info["password"]=password;
		string str = fwriter.write(user_info);
		out << str;
		out.close();
		return 0;   //  success to register
	}
}
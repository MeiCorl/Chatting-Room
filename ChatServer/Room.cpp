#include "Room.h"

int Room::getSize()
{
    return this->clients.size();
}

set<int>::iterator Room::begin()
{
	return this->clients.begin();
}

set<int>::iterator Room::end()
{
	return this->clients.end();
}

void Room::addClient(int client_fd)
{
    this->clients.insert(client_fd);
}

void Room::deleteClient(int client_fd)
{
    this->clients.erase(client_fd);
}

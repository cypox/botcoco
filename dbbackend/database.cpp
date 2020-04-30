#include <experimental/filesystem>
#include <fstream>
#include <regex>
#include "database.h"

Database::Database(std::string db_file)
{
  std::ifstream f(db_file.c_str());
  std::string line;
  while (std::getline(f, line))
  {
    User u(line);
    db_users[u.getUid()] = u;
    auto names = u.getNames();
    for (auto p : names)
    {
      inverse_db_users.insert(std::make_pair(p, u.getUid()));
    }
  }
  f.close();
}

Database::Database(std::string db_file, std::string zip_codes_file)
{
  std::ifstream z(zip_codes_file.c_str());
  std::string line;
  std::smatch res;
  std::regex rexp("([0-9]+)\\*([A-Z ]+)\\*");
  while (std::getline(z, line))
  {
    while (std::regex_search(line, res, rexp))
    {
      zip_codes[std::stoi(res[1])] = res[2];
      line = res.suffix();
    }
  }
  z.close();

  std::ifstream f(db_file.c_str());
  while (std::getline(f, line))
  {
    User u(line);
    db_users[u.getUid()] = u;
    auto names = u.getNames();
    for (auto p : names)
    {
      inverse_db_users.insert(std::make_pair(p, u.getUid()));
    }
  }
  f.close();
}

int Database::loadAvatars(std::string avatars_folder)
{
  int len = 0;
  std::smatch res;
  std::regex rexp("([0-9]{6})");
  for (const auto &entry : std::experimental::filesystem::directory_iterator(avatars_folder))
  {
    std::string filename = entry.path().filename();
    if (std::regex_search(filename, res, rexp))
    {
      int uid = std::stoi(res[1].str());
      auto it = db_users.find(uid);
      if (it != db_users.end())
      {
        it->second.addAvatar(filename);
        ++len;
      }
    }
  }
  return len;
}

void Database::reload()
{
}

User Database::findById(int uid)
{
  if (db_users.find(uid) != db_users.end())
    return db_users[uid];
  else
    return User();
}

std::vector<User> Database::findByName(std::string name)
{
  std::vector<User> users;
  typedef std::multimap<std::string, int>::iterator iter_t;
  std::pair<iter_t, iter_t> result = inverse_db_users.equal_range(name);
  for (auto i = result.first; i != result.second; ++i)
  {
    users.push_back(db_users[(*i).second]);
  }
  return users;
}

/*
// functor to compare with strings
// returns true if the string in the pair containis the other one
struct comp_contains
{
  bool operator()(const std::pair<std::string, int> &a, const std::string &b) const
  {
    return (a.first.find(b) == std::string::npos);
  }

  bool operator()(const std::string &a, const std::pair<std::string, int> &b) const
  {
    //return (b.first.find(a) == std::string::npos);
    return false;
  }
};
*/

#include <iostream>
std::vector<User*> Database::query(std::string name)
{
  std::vector<User*> users;
  for (auto i = inverse_db_users.begin(); i != inverse_db_users.end(); ++ i)
  {
    if (i->first.find(name) != std::string::npos)
      users.push_back(&db_users[i->second]);
  }
  return users;
}
